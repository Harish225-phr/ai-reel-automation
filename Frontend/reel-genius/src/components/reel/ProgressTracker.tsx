import { Check, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { GenerationStep } from '@/types/reel';

interface Props {
  steps: GenerationStep[];
  prompt: string;
}

export function ProgressTracker({ steps, prompt }: Props) {
  const completedCount = steps.filter(s => s.status === 'complete').length;
  const progress = (completedCount / steps.length) * 100;
  const activeStep = steps.find(s => s.status === 'active');
  const estimatedRemaining = (steps.length - completedCount) * 2;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-lg mx-auto px-4"
    >
      <div className="text-center mb-6">
        <h3 className="text-lg font-display font-semibold text-foreground mb-1">Generating your reel</h3>
        <p className="text-xs text-muted-foreground truncate max-w-sm mx-auto">"{prompt}"</p>
      </div>

      {/* Progress bar */}
      <div className="h-1.5 bg-secondary rounded-full overflow-hidden mb-6">
        <motion.div
          className="h-full gradient-bg rounded-full"
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 0.5 }}
        />
      </div>

      <div className="space-y-3">
        {steps.map((step, i) => (
          <motion.div
            key={step.id}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.05 }}
            className={`flex items-center gap-3 py-2 px-3 rounded-lg text-sm transition-colors ${
              step.status === 'active' ? 'bg-primary/10 text-primary' :
              step.status === 'complete' ? 'text-muted-foreground' :
              'text-muted-foreground/40'
            }`}
          >
            <div className="w-5 h-5 flex items-center justify-center shrink-0">
              {step.status === 'complete' ? (
                <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }}>
                  <Check className="h-4 w-4 text-primary" />
                </motion.div>
              ) : step.status === 'active' ? (
                <Loader2 className="h-4 w-4 animate-spin text-primary" />
              ) : (
                <div className="h-2 w-2 rounded-full bg-muted-foreground/30" />
              )}
            </div>
            <span className={step.status === 'active' ? 'font-medium' : ''}>{step.label}</span>
          </motion.div>
        ))}
      </div>

      {estimatedRemaining > 0 && (
        <p className="text-center text-xs text-muted-foreground mt-4">
          ~{estimatedRemaining}s remaining
        </p>
      )}
    </motion.div>
  );
}
