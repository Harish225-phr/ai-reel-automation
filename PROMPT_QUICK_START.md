# Prompt-Driven AI Reel Generator - Quick Start

## Installation

1. **Install requirements:**
```bash
pip install -r requirements.txt
```

2. **Verify system:**
```bash
python main.py --validate
```

## Usage - 3 Easy Ways

### Method 1: Simple Prompt (RECOMMENDED)
```bash
python main.py "Create a Hindi motivational reel about temple daily benefits"
```

### Method 2: Detailed Prompt
```bash
python main.py "Create a 30 second Hindi spiritual reel about temple benefits with calm devotional music, peaceful temple videos, male voice, and emotional tone"
```

### Method 3: Legacy Keyword Mode
```bash
python main.py --keyword "temple" --style motivational --voice male
```

---

## What Gets Generated

When you run a prompt, the system automatically creates:

✅ **Script**: Mood-matched, perfectly toned narration
✅ **Voice**: AI voice in correct language + gender + mood
✅ **Videos**: 4-6 themed stock videos (Pexels API)
✅ **Music**: Perfect background music (Freesound API + fallback)
✅ **Text**: Hook (opening) + Synced captions + CTA (closing)
✅ **Format**: 1080x1920 MP4 (Instagram Reels ready)

**Output file**: `output/reel_prompt_YYYYMMDD_HHMMSS.mp4`

---

## Prompt Examples

### 1. Hindu Spiritual Reel
```bash
python main.py "Create a 25 second Hindi spiritual reel about benefits of temple daily visit. Use calm devotional music. Use peaceful temple videos. Use male Hindi voice. Add emotional tone. Include subtitles and hook text."
```

**System will generate:**
- Language: Hindi
- Voice: Male (hi-IN-MadhurNeural)
- Mood: Spiritual/Emotional
- Music: Calm devotional
- Videos: Temple, prayer, worship clips
- Duration: ~25 seconds

### 2. English Fitness Motivation
```bash
python main.py "Generate a motivational fitness reel with workout videos and upbeat music. Use female narrator. 30 seconds."
```

**System will generate:**
- Language: English
- Voice: Female (en-US-JennyNeural)
- Mood: Motivational
- Music: Upbeat, energetic
- Videos: Gym, workout, exercise
- Duration: ~30 seconds

### 3. Meditation & Mindfulness
```bash
python main.py "Create calm peaceful meditation reel with spiritual music. Educational tone. Include beautiful nature videos."
```

**System will generate:**
- Language: English
- Voice: Female
- Mood: Educational
- Music: Spiritual/calm
- Videos: Nature, meditation, peaceful
- Duration: 30s (default)

### 4. Success & Achievement  
```bash
python main.py "Make motivational success content with sunrise and mountain videos. Male voice. Cinematic style."
```

**System will generate:**
- Language: English
- Voice: Male (en-US-GuyNeural)
- Mood: Motivational
- Music: Motivational/cinematic
- Videos: Success, sunrise, mountain
- Duration: 30s

---

## Supported Languages & Voices

### Hindi
```
Male:   hi-IN-MadhurNeural
Female: hi-IN-SwaraNeural
```

### English
```
Male:   en-US-GuyNeural
Female: en-US-JennyNeural
```

---

## Supported Moods

| Mood | Best For | Script Style |
|------|----------|--------------|
| **Motivational** | Success, achievement, goals | Powerful, action-oriented |
| **Emotional** | Stories, heartfelt, spiritual | Touching, soul-stirring |
| **Spiritual** | Prayer, devotion, meditation | Sacred, elevated |
| **Educational** | Learning, information, facts | Factual, explanatory |
| **Funny** | Entertainment, comedy | Witty, entertaining |

---

## Prompt Keywords Cheat Sheet

### Language
- Hindi: "hindi", "hin"
- English: "english", "eng"

### Voice
- Male: "male", "man", "guy", "masculine"
- Female: "female", "woman", "girl", "feminine"

### Mood
- Motivational: "motivational", "inspiring", "energetic"
- Emotional: "emotional", "touching", "calm", "peaceful"
- Spiritual: "spiritual", "divine", "meditation", "devotional"
- Educational: "educational", "informative", "learn"
- Funny: "funny", "humorous", "comedy"

### Music
- Calm: "calm", "peaceful", "soothing"
- Motivational: "motivational", "epic", "cinematic"
- Spiritual: "spiritual", "devotional", "meditation"
- Upbeat: "upbeat", "happy", "cheerful"

### Video Themes
- Temple: "temple", "prayer", "worship"
- Nature: "nature", "forest", "green", "landscape"
- Success: "success", "achievement", "sunrise", "mountain"
- Fitness: "fitness", "workout", "exercise", "gym"
- Meditation: "meditation", "peaceful", "calm"
- Daily Life: "lifestyle", "routine", "morning"

### Duration
- "25 second", "30 sec", "45s", "2 minutes"

---

## Advanced Usage

### Batch Generation (Multiple Reels)
```bash
python main.py --keyword "success" --batch 5
```
Generates 5 different reels from same keyword.

### Custom Video Count
```bash
python main.py "Fitness reel" --videos 8
```
Downloads 8 videos instead of default 5.

### Validation Only
```bash
python main.py --validate
```
Checks system setup without generating.

---

## Output File Location

All generated reels are saved in:
```
d:\Python\ai-reel-automation\output\reel_prompt_YYYYMMDD_HHMMSS.mp4
```

**Size**: Typically 15-25 MB
**Duration**: 25-35 seconds
**Format**: 1080x1920 MP4 (Instagram Reels optimized)

---

## Troubleshooting

### Q: Script is in English, I wanted Hindi?
A: Add "hindi" to your prompt:
```bash
python main.py "Create Hindi reel about meditation"
```

### Q: Voice doesn't match my preference?
A: Specify clearly:
```bash
python main.py "Motivational reel with male narrator"
```

### Q: Music not playing?
A: Falls back to voice-only automatically. Can still add by:
```bash
python main.py "Reel with upbeat music"
```

### Q: Videos are showing or black screen?
A: System has 3-layer fallback:
1. Pexels API (primary)
2. Pixabay API (secondary)
3. Local fallback (tertiary)

Always generates valid video.

### Q: Voices sound weird?
A: Try matching mood:
- Motivational: Use "motivational reel"
- Calm: Use "peaceful meditation reel"
- Spiritual: Use "spiritual devotional reel"

---

## Performance

Typical reel generation timeline:

```
1. Parsing prompt:           ~1 second
2. Generating script:        ~2 seconds
3. Creating voice:           ~15 seconds
4. Fetching videos:          ~30 seconds
5. Fetching music:           ~10 seconds
6. Compositing & encoding:   ~120-180 seconds (depends on system)

TOTAL: ~3-5 minutes per reel
```

---

## Features

✅ **Automatic Parsing**: Understands natural language completely
✅ **Mood Detection**: Matches script tone to your request
✅ **Smart Voice Selection**: Picks perfect voice based on language + mood
✅ **Theme-based Videos**: Fetches relevant stock videos
✅ **Music Integration**: Thoughtful background music selection
✅ **Cinematic Effects**: Zoom, crossfade, professional transitions
✅ **Auto Subtitles**: Synced to speech automatically
✅ **Hook + CTA**: Opening and closing text
✅ **Instagram Ready**: Perfect 1080x1920 format
✅ **Self-Healing**: Handles errors gracefully
✅ **Backward Compatible**: Old keyword mode still works

---

## Next Steps

1. **Generate your first reel:**
   ```bash
   python main.py "Create a motivational reel about meditation"
   ```

2. **Check output:**
   - Look in `output/` folder
   - Download the MP4 file
   - Upload to Instagram Reels

3. **Customize:**
   - Add language: "Hindi reel..."
   - Add voice: "Male narrator..."
   - Add mood: "Spiritual content..."
   - Add music: "With calm music..."
   - Add duration: "45 second reel..."

---

## Pro Tips

✅ **Be specific but natural**: "Create a spiritual Hindi reel about temple benefits" works great
✅ **Mention mood**: "Emotional" scripts are more touching than generic ones
✅ **Include language**: Helps select better voice
✅ **Add duration if planning**: Helps control pacing
✅ **Let system choose**: If unsure, it defaults to safe "motivational" style

---

## Questions?

See **PROMPT_DRIVEN_GUIDE.md** for complete documentation.

**Your reels are waiting! Start generating! 🚀**
