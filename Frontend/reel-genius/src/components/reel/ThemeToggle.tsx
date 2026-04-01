import { Moon, Sun } from 'lucide-react';
import { motion } from 'framer-motion';

interface Props {
  isDark: boolean;
  toggle: () => void;
}

export function ThemeToggle({ isDark, toggle }: Props) {
  return (
    <button
      onClick={toggle}
      className="relative h-9 w-9 rounded-lg bg-secondary flex items-center justify-center text-muted-foreground hover:text-foreground transition-colors"
      aria-label="Toggle theme"
    >
      <motion.div
        key={isDark ? 'dark' : 'light'}
        initial={{ rotate: -90, opacity: 0 }}
        animate={{ rotate: 0, opacity: 1 }}
        transition={{ duration: 0.2 }}
      >
        {isDark ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
      </motion.div>
    </button>
  );
}
