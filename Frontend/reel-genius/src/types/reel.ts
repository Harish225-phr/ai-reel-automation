export interface GenerationStep {
  id: string;
  label: string;
  status: 'pending' | 'active' | 'complete' | 'error';
}

export interface ReelGeneration {
  id: string;
  prompt: string;
  language: 'en' | 'hi';
  timestamp: Date;
  status: 'generating' | 'complete' | 'error';
  steps: GenerationStep[];
  videoUrl?: string;
  duration?: string;
  size?: string;
  errorMessage?: string;
}

export const DEFAULT_STEPS: Omit<GenerationStep, 'status'>[] = [
  { id: 'parse', label: 'Parsing your prompt...' },
  { id: 'script', label: 'Generating script...' },
  { id: 'clips', label: 'Finding video clips...' },
  { id: 'voice', label: 'Creating voice-over...' },
  { id: 'music', label: 'Adding background music...' },
  { id: 'compose', label: 'Composing final reel...' },
];
