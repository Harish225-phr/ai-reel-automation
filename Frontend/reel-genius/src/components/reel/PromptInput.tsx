import { useState } from 'react';
import { Sparkles, ChevronDown } from 'lucide-react';
import { motion } from 'framer-motion';

const EXAMPLE_PROMPTS = [
  { text: 'Create a motivational reel about productivity', lang: 'en' as const },
  { text: 'Generate a health tips reel for fitness enthusiasts', lang: 'en' as const },
  { text: 'Make a funny reel about Monday mornings', lang: 'en' as const },
  { text: 'प्रेरणादायक रील आत्मविश्वास के बारे में', lang: 'hi' as const },
  { text: 'स्वास्थ्य सुझाव रील व्यस्त पेशेवरों के लिए', lang: 'hi' as const },
  { text: 'योग लाभ के बारे में एक आध्यात्मिक रील', lang: 'hi' as const },
];

interface Props {
  onGenerate: (prompt: string, language: 'en' | 'hi') => void;
}

export function PromptInput({ onGenerate }: Props) {
  const [prompt, setPrompt] = useState('');
  const [language, setLanguage] = useState<'en' | 'hi'>('en');
  const [showLang, setShowLang] = useState(false);

  const handleSubmit = () => {
    if (!prompt.trim()) return;
    onGenerate(prompt.trim(), language);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
      className="w-full max-w-2xl mx-auto px-4"
    >
      <div className="text-center mb-10">
        <h2 className="text-3xl md:text-4xl font-display font-bold gradient-text mb-3">
          What reel do you want to create?
        </h2>
        <p className="text-muted-foreground text-sm">
          Describe your idea and we'll generate a short-form video for you
        </p>
      </div>

      <div className="gradient-border p-4 space-y-3">
        <textarea
          value={prompt}
          onChange={e => setPrompt(e.target.value)}
          placeholder="Generate a motivational reel about health..."
          rows={4}
          className="w-full bg-transparent resize-none text-foreground placeholder:text-muted-foreground focus:outline-none text-sm leading-relaxed"
          onKeyDown={e => {
            if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) handleSubmit();
          }}
        />

        <div className="flex items-center justify-between">
          <div className="relative">
            <button
              onClick={() => setShowLang(!showLang)}
              className="flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground transition-colors bg-secondary px-3 py-1.5 rounded-md"
            >
              {language === 'en' ? '🇬🇧 English' : '🇮🇳 हिंदी'}
              <ChevronDown className="h-3 w-3" />
            </button>
            {showLang && (
              <motion.div
                initial={{ opacity: 0, y: -5 }}
                animate={{ opacity: 1, y: 0 }}
                className="absolute top-full mt-1 left-0 bg-card border border-border rounded-lg shadow-lg overflow-hidden z-10"
              >
                {(['en', 'hi'] as const).map(l => (
                  <button
                    key={l}
                    onClick={() => { setLanguage(l); setShowLang(false); }}
                    className={`block w-full text-left px-4 py-2 text-xs hover:bg-secondary transition-colors ${language === l ? 'text-primary' : 'text-foreground'}`}
                  >
                    {l === 'en' ? '🇬🇧 English' : '🇮🇳 हिंदी'}
                  </button>
                ))}
              </motion.div>
            )}
          </div>

          <motion.button
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
            onClick={handleSubmit}
            disabled={!prompt.trim()}
            className="gradient-bg text-primary-foreground font-display font-semibold px-6 py-2.5 rounded-lg text-sm disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-2 glow-effect transition-shadow"
          >
            <Sparkles className="h-4 w-4" />
            Generate Reel
          </motion.button>
        </div>
      </div>

      <div className="mt-8 space-y-2">
        <p className="text-xs text-muted-foreground font-medium">Try an example:</p>
        <div className="flex flex-wrap gap-2">
          {EXAMPLE_PROMPTS.map((ex, i) => (
            <motion.button
              key={i}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 * i }}
              onClick={() => { setPrompt(ex.text); setLanguage(ex.lang); }}
              className="text-xs bg-secondary text-secondary-foreground px-3 py-1.5 rounded-full hover:bg-primary/10 hover:text-primary transition-colors max-w-[260px] truncate"
            >
              {ex.text}
            </motion.button>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
