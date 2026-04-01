import { Clock, Trash2, Film, ChevronLeft, ChevronRight } from 'lucide-react';
import { ReelGeneration } from '@/types/reel';
import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';

interface Props {
  generations: ReelGeneration[];
  onSelect: (gen: ReelGeneration) => void;
  onClear: () => void;
  currentId?: string;
}

export function HistorySidebar({ generations, onSelect, onClear, currentId }: Props) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <motion.aside
      animate={{ width: collapsed ? 48 : 280 }}
      transition={{ duration: 0.2 }}
      className="h-full border-r border-border bg-card flex flex-col shrink-0 overflow-hidden"
    >
      <div className="flex items-center justify-between p-3 border-b border-border min-h-[52px]">
        {!collapsed && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex items-center gap-2">
            <Film className="h-4 w-4 text-primary" />
            <span className="text-sm font-display font-semibold text-foreground">History</span>
          </motion.div>
        )}
        <button onClick={() => setCollapsed(!collapsed)} className="h-7 w-7 flex items-center justify-center rounded-md hover:bg-secondary text-muted-foreground transition-colors">
          {collapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
        </button>
      </div>

      {!collapsed && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex-1 overflow-y-auto p-2 space-y-1">
          <AnimatePresence>
            {generations.length === 0 && (
              <p className="text-xs text-muted-foreground text-center py-8">No reels yet</p>
            )}
            {generations.map((gen) => (
              <motion.button
                key={gen.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0 }}
                onClick={() => onSelect(gen)}
                className={`w-full text-left p-2.5 rounded-lg transition-colors text-sm group ${
                  currentId === gen.id ? 'bg-primary/10 text-primary' : 'hover:bg-secondary text-foreground'
                }`}
              >
                <p className="truncate font-medium text-xs">{gen.prompt}</p>
                <div className="flex items-center gap-2 mt-1 text-muted-foreground">
                  <Clock className="h-3 w-3" />
                  <span className="text-[10px]">{gen.timestamp.toLocaleTimeString()}</span>
                  {gen.duration && <span className="text-[10px]">· {gen.duration}</span>}
                </div>
              </motion.button>
            ))}
          </AnimatePresence>
        </motion.div>
      )}

      {!collapsed && generations.length > 0 && (
        <div className="p-2 border-t border-border">
          <button
            onClick={onClear}
            className="w-full flex items-center justify-center gap-1.5 text-xs text-muted-foreground hover:text-destructive transition-colors py-2 rounded-md hover:bg-destructive/10"
          >
            <Trash2 className="h-3 w-3" /> Clear History
          </button>
        </div>
      )}
    </motion.aside>
  );
}
