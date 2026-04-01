import { Film } from 'lucide-react';
import { useEffect } from 'react';
import { ThemeToggle } from '@/components/reel/ThemeToggle';
import { HistorySidebar } from '@/components/reel/HistorySidebar';
import { PromptInput } from '@/components/reel/PromptInput';
import { ProgressTracker } from '@/components/reel/ProgressTracker';
import { ResultView } from '@/components/reel/ResultView';
import { useTheme } from '@/hooks/useTheme';
import { useReelGenerator } from '@/hooks/useReelGenerator';

export default function Index() {
  const { isDark, toggle } = useTheme();
  const { current, generations, generate, reset, selectGeneration, clearHistory, loadVideoHistory } = useReelGenerator();

  // Load video history on mount
  useEffect(() => {
    loadVideoHistory();
  }, [loadVideoHistory]);

  const showInput = !current;
  const showProgress = current?.status === 'generating';
  const showResult = current?.status === 'complete';

  return (
    <div className="h-screen flex flex-col bg-background">
      {/* Header */}
      <header className="h-13 border-b border-border flex items-center justify-between px-4 shrink-0">
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 gradient-bg rounded-lg flex items-center justify-center">
            <Film className="h-4 w-4 text-primary-foreground" />
          </div>
          <h1 className="font-display font-bold text-foreground text-base">
            AI Reel Generator
          </h1>
        </div>
        <ThemeToggle isDark={isDark} toggle={toggle} />
      </header>

      {/* Body */}
      <div className="flex-1 flex min-h-0">
        {/* Sidebar - hidden on mobile */}
        <div className="hidden md:block">
          <HistorySidebar
            generations={generations}
            onSelect={selectGeneration}
            onClear={clearHistory}
            currentId={current?.id}
          />
        </div>

        {/* Main Content */}
        <main className="flex-1 flex items-center justify-center overflow-y-auto py-8">
          {showInput && <PromptInput onGenerate={generate} />}
          {showProgress && current && <ProgressTracker steps={current.steps} prompt={current.prompt} />}
          {showResult && current && <ResultView generation={current} onReset={reset} />}
        </main>
      </div>

      {/* Footer */}
      <footer className="h-10 border-t border-border flex items-center justify-center shrink-0">
        <p className="text-[11px] text-muted-foreground">Powered by AI ✨</p>
      </footer>
    </div>
  );
}
