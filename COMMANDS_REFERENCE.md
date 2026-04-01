# Prompt-Driven AI Reel Generator - Command Reference

## Quick Start (Copy & Paste)

### 1. Simple Test
```bash
python main.py "Create a motivational reel about success"
```

### 2. Hindi Spiritual
```bash
python main.py "Create a Hindi spiritual reel about temple benefits with calm devotional music"
```

### 3. Detailed Specification
```bash
python main.py "Create a 30 second Hindi emotional reel about daily meditation benefits with peaceful background music, male voice, and professional subtitles"
```

### 4. Fitness Motivation
```bash
python main.py "Generate motivational fitness workout reel with upbeat energetic music"
```

### 5. Educational Wellness
```bash
python main.py "Make an educational 45-second wellness reel about health benefits with informative tone"
```

---

## Command Template

### Minimal Template
```bash
python main.py "<TOPIC>"
```

### Full Template
```bash
python main.py "Create a [DURATION] [LANGUAGE] [MOOD] reel about [TOPIC] with [MUSIC] and [VOICE] voice"
```

### Example Filled
```bash
python main.py "Create a 30-second Hindi spiritual reel about temple benefits with calm devotional music and male voice"
```

---

## Parameter Keywords

### DURATION
- "25 second" / "25 sec" / "25s"
- "2 minutes" / "2 min" / "2m"
- (Default: 30 seconds)

### LANGUAGE
- "Hindi" / "hin"
- "English" / "eng"
- (Default: English)

### MOOD
- "motivational" / "motivating" / "inspiring" / "energetic"
- "emotional" / "touching" / "heartfelt" / "peaceful"
- "spiritual" / "divine" / "meditation" / "devotional"
- "educational" / "informative" / "learn" / "knowledge"
- "funny" / "humorous" / "comedy" / "hilarious"
- (Default: motivational)

### MUSIC TYPE
- "calm" / "peaceful" / "relaxing" / "soothing"
- "motivational" / "epic" / "cinematic" / "powerful"
- "spiritual" / "meditation" / "devotional" / "mantra"
- "upbeat" / "happy" / "cheerful" / "energetic"
- (Default: motivational)

### VOICE
- "male" / "man" / "guy" / "masculine"
- "female" / "woman" / "girl" / "feminine"
- (Default: female)

### TOPIC
- Any topic or keyword: "success", "meditation", "fitness", "temple", etc.
- Can be phrase: "daily temple benefits", "morning meditation practice", etc.

---

## Real-World Examples

### Example 1: Spiritual Content Creator
```bash
python main.py "Create a 30-second Hindi spiritual reel about benefits of daily temple visit with calm devotional background music, deep male voice, and emotional tone to inspire devotion"
```

### Example 2: Fitness Coach
```bash
python main.py "Generate an energetic 45-second motivational fitness workout reel in English using upbeat music, dynamic editing, and female narrator with inspiring tone"
```

### Example 3: Meditation Teacher
```bash
python main.py "Create a peaceful meditation reel about stress relief and mindfulness with calm background music, soothing tone, and nature-themed videos"
```

### Example 4: Educational Channel
```bash
python main.py "Make an educational reel about neem tree health benefits with informative tone, professional editing, and research-backed content"
```

### Example 5: Entertainment
```bash
python main.py "Generate a funny entertaining reel about common fitness mistakes with humorous tone and upbeat music"
```

### Example 6: Motivational Speaker
```bash
python main.py "Create a Hindi motivational reel about success and achievement with cinematic music, inspiring tone, and powerful messaging"
```

### Example 7: Wellness Brand
```bash
python main.py "Generate a 25-second wellness reel about yoga and flexibility with calm peaceful music and female narrator"
```

### Example 8: Religion/Culture
```bash
python main.py "Create a devotional reel about importance of prayer and faith in daily life with spiritual tone and male voice"
```

---

## Minimal Variations

### Shortest
```bash
python main.py "Success"
```
(Falls back to legacy mode, uses defaults)

### Slightly Longer
```bash
python main.py "Motivational success reel"
```

### A Bit More
```bash
python main.py "Create motivational success reel with upbeat music"
```

### Full Detail
```bash
python main.py "Create a 30-second motivational reel about achieving success with upbeat energetic music and professional female narrator with inspiring tone"
```

---

## Legacy Commands (Still Work)

### Keyword Mode
```bash
python main.py --keyword "meditation"
python main.py --keyword "fitness" --style motivational
python main.py --keyword "temple" --voice male
```

### Batch Mode
```bash
python main.py --keyword "success" --batch 5
```

### Custom Videos
```bash
python main.py --keyword "health" --videos 8
```

### Validation
```bash
python main.py --validate
```

---

## What Gets Detected

### Intelligence Layer

When you write the prompt, the system automatically detects:

```
"Create a 30-second Hindi emotional reel about daily 
 temple visit with calm devotional music and male voice"

DETECTED:
✓ Duration: 30 seconds
✓ Language: Hindi (from "Hindi" keyword)
✓ Mood: Emotional (from "emotional" keyword)
✓ Topic: Daily temple visit
✓ Music Type: Calm devotional (from "calm" + "devotional")
✓ Voice: Male (from "male voice")
✓ Theme: Temple (auto-from topic)
✓ Style: Cinematic (default)
↓
SELECTED:
✓ Voice: hi-IN-MadhurNeural (Hindi male)
✓ Script Tone: Emotional (heart-touching sentences)
✓ Video Search: "temple", "prayer", "devotion", "worship"
✓ Music Search: "calm devotional temple visit"
↓
GENERATES:
✓ Perfect 30-second reel
✓ Emotional-toned script
✓ Male Hindi voice
✓ Temple/prayer videos
✓ Calm devotional music background
✓ Professional subtitles & effects
```

---

## Tips for Best Results

### ✅ DO
- Be descriptive but natural: "Create a spiritual reel about meditation"
- Mention mood if specific: "Emotional reel about loss"
- Include language if not English: "Hindi motivational content"
- Specify voice type for personality: "Deep male narrator"
- Add duration if important: "45-second reel"
- Mention music preference: "With upbeat energetic music"

### ❌ DON'T
- Don't use technical jargon: ❌ "Prompt: topic=meditation"
- Don't be too vague: ❌ "reel" (still works but gets defaults)
- Don't use abbreviations: ✅ "Hindi" NOT ❌ "HIN"
- Don't worry about perfection: System is smart!

---

## Output Location

All reels generate to:
```
output/reel_prompt_YYYYMMDD_HHMMSS.mp4
```

Example:
```
output/reel_prompt_20260331_171500.mp4
```

---

## File Properties

**All reels have:**
- 1080x1920 resolution (vertical, Instagram optimized)
- 30 FPS frame rate
- H.264 video codec
- AAC audio codec
- 15-25 MB typical size
- 25-35 seconds typical duration
- Ready for social media ✓

---

## Troubleshooting

### "System is slow"
→ Normal! H.264 encoding takes 2-3 minutes. First time Pexels/Freesound downloads take time.

### "Music didn't download"
→ Freesound API may be rate-limited. System falls back to voice-only (still great reel).

### "Some videos failed to download"
→ System has 3-layer fallback. Will use available videos.

### "I want legacy keyword mode"
→ Use: `python main.py --keyword "meditation"`

### "I want batch mode"
→ Use: `python main.py --keyword "fitness" --batch 5`

### "Nothing happens"
→ System might be encoding. Give it 5-10 minutes. Check `output/` folder.

---

## Feature Comparison

| Feature | Prompt-Driven | Legacy |
|---------|---|---|
| Natural language | ✅ | ❌ |
| Mood detection | ✅ Auto | ❌ Manual |
| Language detection | ✅ Auto | ❌ Eng only |
| Smart voice pick | ✅ 4 voices | ❌ 2 genders |
| Theme videos | ✅ 7 themes | ❌ Keyword |
| Music type | ✅ 4 types | ❌ Any |
| Backward compat | ✅ 100% | ✅ 100% |

---

## Advanced Usage

### Test Different Moods
```bash
python main.py "Temple reel emotional"
python main.py "Temple reel motivational"
python main.py "Temple reel spiritual"
python main.py "Temple reel educational"
```

### Test Different Languages
```bash
python main.py "Hindi temple reel"
python main.py "English temple reel"
```

### Test Different Voices
```bash
python main.py "Success reel male voice"
python main.py "Success reel female voice"
```

### Test Different Durations
```bash
python main.py "25 second success reel"
python main.py "45 second success reel"
python main.py "60 second success reel"
```

---

## Support

For detailed documentation:
- `PROMPT_QUICK_START.md` - 5-minute read
- `PROMPT_DRIVEN_GUIDE.md` - Complete reference  
- `PROMPT_DRIVEN_IMPLEMENTATION.md` - Technical deep-dive
- `README_PROMPT_DRIVEN.md` - Full system overview

---

## Summary

### Simplest Command
```bash
python main.py "success"
```

### Recommended Command
```bash
python main.py "Create a motivational reel about success"
```

### Detailed Command
```bash
python main.py "Create a 30-second motivational reel about achieving success with upbeat music and professional female narrator"
```

**All three work perfectly! Pick the detail level you prefer.**

---

**Ready to create amazing reels?** 🎬

Your system is fully prompt-driven and ready to generate professional content automatically!
