import { Download, RefreshCw, Copy, Clock, HardDrive, Languages, Check } from 'lucide-react';
import { motion } from 'framer-motion';
import { ReelGeneration } from '@/types/reel';
import { useState } from 'react';

interface Props {
  generation: ReelGeneration;
  onReset: () => void;
}

export function ResultView({ generation, onReset }: Props) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (generation.videoUrl) {
      navigator.clipboard.writeText(generation.videoUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-2xl mx-auto px-4 flex flex-col md:flex-row gap-6 items-start"
    >
      {/* Video Preview */}
      <div className="gradient-border p-1 mx-auto md:mx-0 shrink-0">
        <div className="w-[200px] h-[356px] md:w-[240px] md:h-[427px] rounded-[calc(var(--radius)-2px)] overflow-hidden bg-background">
          <video
            src={generation.videoUrl}
            controls
            className="w-full h-full object-cover"
            poster=""
          />
        </div>
      </div>

      {/* Info & Actions */}
      <div className="flex-1 space-y-5 min-w-0 w-full">
        <div>
          <h3 className="text-lg font-display font-semibold text-foreground mb-1">Your reel is ready!</h3>
          <p className="text-sm text-muted-foreground truncate">"{generation.prompt}"</p>
        </div>

        {/* Metadata */}
        <div className="flex flex-wrap gap-3">
          {generation.duration && (
            <div className="flex items-center gap-1.5 text-xs text-muted-foreground bg-secondary px-3 py-1.5 rounded-md">
              <Clock className="h-3 w-3" /> {generation.duration}
            </div>
          )}
          {generation.size && (
            <div className="flex items-center gap-1.5 text-xs text-muted-foreground bg-secondary px-3 py-1.5 rounded-md">
              <HardDrive className="h-3 w-3" /> {generation.size}
            </div>
          )}
          <div className="flex items-center gap-1.5 text-xs text-muted-foreground bg-secondary px-3 py-1.5 rounded-md">
            <Languages className="h-3 w-3" /> {generation.language === 'en' ? 'English' : 'हिंदी'}
          </div>
        </div>

        {/* Actions */}
        <div className="flex flex-wrap gap-2">
          <motion.a
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            href={generation.videoUrl}
            download
            className="gradient-bg text-primary-foreground font-display font-semibold px-5 py-2.5 rounded-lg text-sm flex items-center gap-2 glow-effect"
          >
            <Download className="h-4 w-4" /> Download Video
          </motion.a>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onReset}
            className="bg-secondary text-secondary-foreground font-medium px-5 py-2.5 rounded-lg text-sm flex items-center gap-2 hover:bg-secondary/80 transition-colors"
          >
            <RefreshCw className="h-4 w-4" /> Generate Another
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handleCopy}
            className="bg-secondary text-secondary-foreground font-medium px-4 py-2.5 rounded-lg text-sm flex items-center gap-2 hover:bg-secondary/80 transition-colors"
          >
            {copied ? <Check className="h-4 w-4 text-primary" /> : <Copy className="h-4 w-4" />}
            {copied ? 'Copied!' : 'Copy Link'}
          </motion.button>
        </div>
      </div>
    </motion.div>
  );
}
