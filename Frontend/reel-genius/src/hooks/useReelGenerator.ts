import { useState, useCallback, useRef } from 'react';
import { ReelGeneration, DEFAULT_STEPS, GenerationStep } from '@/types/reel';
import { useToast } from '@/components/ui/use-toast';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export function useReelGenerator() {
  const [generations, setGenerations] = useState<ReelGeneration[]>([]);
  const [current, setCurrent] = useState<ReelGeneration | null>(null);
  const eventSourceRef = useRef<EventSource | null>(null);
  const { toast } = useToast();

  const generate = useCallback((prompt: string, language: 'en' | 'hi') => {
    // Initialize generation
    const steps: GenerationStep[] = DEFAULT_STEPS.map(s => ({ ...s, status: 'pending' as const }));
    steps[0].status = 'active';

    const gen: ReelGeneration = {
      id: crypto.randomUUID(),
      prompt,
      language,
      timestamp: new Date(),
      status: 'generating',
      steps,
    };

    setCurrent(gen);

    // Close any existing connection
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    // Make API call with fetch (not EventSource for better error handling)
    fetchWithEventStream(prompt, language, gen);
  }, []);

  const fetchWithEventStream = async (prompt: string, language: 'en' | 'hi', gen: ReelGeneration) => {
    try {
      const url = `${API_BASE_URL}/api/generate-reel`;
      console.log('[Frontend] API Base URL:', API_BASE_URL);
      console.log('[Frontend] Sending request to:', url);
      console.log('[Frontend] Payload:', { prompt, language });
      
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt, language }),
      });

      console.log('[Frontend] Response status:', response.status);
      console.log('[Frontend] Response OK:', response.ok);

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('No response body');
      }

      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');

        // Keep last incomplete line in buffer
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const message = JSON.parse(line.slice(6));
              handleProgressUpdate(message, gen);
            } catch (e) {
              console.error('Failed to parse message:', e);
            }
          }
        }
      }
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : 'Unknown error';
      console.error('Generation failed:', errorMsg);

      setCurrent(prev => {
        if (!prev) return null;
        return {
          ...prev,
          status: 'error',
          errorMessage: errorMsg,
          steps: prev.steps.map(s => ({
            ...s,
            status: s.status === 'complete' ? 'complete' : s.status === 'active' ? 'error' : 'pending'
          }))
        };
      });

      toast({
        title: 'Generation Failed',
        description: errorMsg,
        variant: 'destructive',
      });
    }
  };

  const handleProgressUpdate = (message: any, gen: ReelGeneration) => {
    const { step, status, video_file, duration, size } = message;

    console.log('[Frontend] Progress update:', {
      status,
      step,
      video_file,
      duration,
      size,
      full_message: message
    });

    if (status === 'success') {
      // Generation complete
      console.log('[Frontend] SUCCESS received!');
      console.log('[Frontend] video_file:', video_file);
      console.log('[Frontend] duration:', duration);
      console.log('[Frontend] size:', size);
      
      const videoUrl = video_file ? `${API_BASE_URL}/api/stream/${video_file}` : undefined;
      console.log('[Frontend] Constructed videoUrl:', videoUrl);
      
      // Update state with actual metadata from backend
      const final: ReelGeneration = {
        ...gen,
        status: 'complete',
        steps: gen.steps.map(s => ({ ...s, status: 'complete' as const })),
        videoUrl,
        duration: duration || '0:00',
        size: size || '0 MB',
      };

      setCurrent(final);
      setGenerations(prev => [final, ...prev].slice(0, 10));

      // Show success toast
      toast({
        title: 'Reel Generated!',
        description: `${size || '0 MB'} • ${duration || '0:00'}`,
      });
    } else if (status === 'error') {
      // Error occurred
      setCurrent(prev => {
        if (!prev) return null;
        return {
          ...prev,
          status: 'error',
          errorMessage: message.message,
          steps: prev.steps.map(s => ({
            ...s,
            status: s.status === 'complete' ? 'complete' : 'error'
          }))
        };
      });

      toast({
        title: 'Error Generating Reel',
        description: message.message,
        variant: 'destructive',
      });
    } else if (step) {
      // Update step status
      const stepId = step;
      const stepIndex = DEFAULT_STEPS.findIndex(s => s.id === stepId);

      if (stepIndex !== -1) {
        setCurrent(prev => {
          if (!prev) return null;

          const newSteps = [...prev.steps];

          // Mark previous steps as complete
          for (let i = 0; i < stepIndex; i++) {
            if (newSteps[i].status !== 'complete') {
              newSteps[i] = { ...newSteps[i], status: 'complete' as const };
            }
          }

          // Set current step to active
          newSteps[stepIndex] = {
            ...newSteps[stepIndex],
            status: status === 'active' ? 'active' : (status === 'complete' ? 'complete' : 'pending')
          };

          // Mark further steps as pending
          for (let i = stepIndex + 1; i < newSteps.length; i++) {
            if (newSteps[i].status !== 'complete') {
              newSteps[i] = { ...newSteps[i], status: 'pending' as const };
            }
          }

          return { ...prev, steps: newSteps };
        });
      }
    }
  };

  const reset = useCallback(() => setCurrent(null), []);

  const selectGeneration = useCallback((gen: ReelGeneration) => setCurrent(gen), []);

  const clearHistory = useCallback(() => {
    setGenerations([]);
    setCurrent(null);
  }, []);

  const loadVideoHistory = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/videos`);
      if (!response.ok) {
        throw new Error('Failed to load video history');
      }
      const data = await response.json();
      
      // Convert database records to ReelGeneration format
      const videos = data.videos.map((video: any) => ({
        id: video.id,
        prompt: video.prompt,
        language: video.language,
        timestamp: new Date(video.created_at),
        status: video.status === 'complete' ? 'complete' : video.status === 'processing' ? 'generating' : 'error',
        videoUrl: video.video_file ? `${API_BASE_URL}/api/stream/${video.video_file}` : undefined,
        duration: video.duration || '0:00',
        size: video.file_size || '0 MB',
        errorMessage: video.error_message,
        steps: DEFAULT_STEPS.map(s => ({
          ...s,
          status: (video.status === 'complete' ? 'complete' : video.status === 'error' ? 'error' : 'pending') as const
        }))
      }));

      setGenerations(videos);
    } catch (error) {
      console.error('Failed to load video history:', error);
      toast({
        title: 'Error Loading History',
        description: error instanceof Error ? error.message : 'Unknown error',
        variant: 'destructive',
      });
    }
  }, [toast]);

  return { current, generations, generate, reset, selectGeneration, clearHistory, loadVideoHistory };
}
