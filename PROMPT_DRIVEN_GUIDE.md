# Prompt-Driven Reel Engine - User Guide

## Overview

The AI Reel Generator now supports **PROMPT-DRIVEN natural language interface**. Users can describe reels in natural language, and the system automatically understands and generates them.

### What Changed?

**Old Way (Still Works):**
```bash
python main.py --keyword "temple benefits" --style motivational --voice male
```

**New Way (RECOMMENDED):**
```bash
python main.py "Create a Hindi motivational reel about temple benefits with calm music"
```

The system automatically parses your natural language description and generates the perfect reel!

---

## Prompt Parser Understanding

The prompt parser extracts these parameters from your natural language:

### 1. **Keyword/Topic** (REQUIRED)
User describes the main topic naturally:
- "temple benefits"
- "meditation practice"
- "fitness workout"
- "spiritual growth"

Parser looks for:
- "about <topic>"
- "regarding <topic>"
- "reel <topic>"

### 2. **Language** (OPTIONAL - Default: English)
Parser detects:
- "hindi" / "hin" → Hindi
- "english" / "eng" → English

**Example:** "Hindi motivational reel" → Language = Hindi

### 3. **Voice Gender** (OPTIONAL - Default: Female)
Parser detects:
- "male" / "man" / "guy" → Male voice
- "female" / "woman" / "girl" → Female voice

**Example:** "Use male narrator" → Voice = Male

### 4. **Mood/Tone** (OPTIONAL - Default: Motivational)
Parser detects 5 moods:

| Mood | Keywords | Script Style |
|------|----------|--------------|
| **motivational** | motivational, inspiring, pump up, energetic | Encouraging, action-oriented |
| **emotional** | emotional, touching, calm, peaceful, serene | Heart-touching, poignant |
| **spiritual** | spiritual, divine, meditation, devotional | Sacred, elevated, tranquil |
| **educational** | educational, informative, learn, knowledge | Factual, explanatory |
| **funny** | funny, hilarious, comedy, humorous | Witty, entertaining |

**Example:** "Create emotional reel" → Mood = emotional

### 5. **Music Type** (OPTIONAL - Default: Motivational)
Parser detects:
- "calm" / "peaceful" → Calm background music
- "motivational" / "cinematic" / "epic" → Energetic music
- "spiritual" / "meditation" → Devotional music
- "upbeat" / "happy" / "cheerful" → Upbeat music

**Example:** "with calm devotional music" → Music = calm

### 6. **Video Theme** (OPTIONAL - Default: Motivation)
Parser detects:
- "temple" → Temple/prayer videos
- "nature" → Forest/green/landscape videos
- "success" / "achievement" → Sunrise/mountain videos
- "meditation" → Peaceful/calm videos
- "fitness" / "workout" → Exercise/gym videos
- "daily life" / "lifestyle" → Daily routine videos

**Example:** "Use peaceful temple videos" → Theme = temple

### 7. **Duration** (OPTIONAL - Default: 30 seconds)
Parser detects time patterns:
- "25 second", "25 sec", "25s" → 25 seconds
- "2 minutes", "2 min", "2m" → 120 seconds

**Example:** "Create a 45 second reel" → Duration = 45s

### 8. **Style** (OPTIONAL - Default: Cinematic)
Parser detects:
- "cinematic" → Professional cinema style
- "fast paced" → Quick cuts
- "slow" → Leisurely pacing
- "documentary" → Doc style

---

## Smart Script Generation

Scripts are **mood-matched** and generated for your topic:

### Motivational Scripts
- Opening: "Did you know...?" hooks
- Body: Powerful benefits
- Closing: Call-to-action for change

**Example:**
```
"Did you know that temple daily visit could transform your life? 
Let me share the most powerful benefits...

First, spiritual peace and inner calm. This changes how you approach life.
Second, connection to something greater than yourself. This is the game changer.
..."
```

### Emotional Scripts
- Opening: Soft, touching hooks
- Body: Heart-touching benefits
- Closing: Deeply personal messages

**Example:**
```
"There's a beauty in meditation that touches the soul...
Let me share something deeply personal about this sacred practice...

When we embrace inner peace, something beautiful happens.
Feel the grace of connection in every fiber of your being..."
```

### Spiritual Scripts
- Opening: Ancient wisdom references
- Body: Transcendent truth
- Closing: Divine connection

### Educational Scripts
- Opening: Factual hooks
- Body: Research-backed benefits
- Closing: Knowledge-driven conclusions

### Funny Scripts
- Opening: Witty hooks
- Body: Humorous takes
- Closing: Punchlines

---

## Voice Selection

Voices are automatically selected based on **Language + Gender + Mood**:

### Hindi Voices
| Gender | Mood | Voice ID |
|--------|------|----------|
| Male | Any | hi-IN-MadhurNeural |
| Female | Any | hi-IN-SwaraNeural |

### English Voices
| Gender | Mood | Voice ID |
|--------|------|----------|
| Male | Motivational | en-US-GuyNeural |
| Male | Emotional | en-US-AmberNeural |
| Female | Motivational | en-US-JennyNeural |
| Female | Emotional | en-US-JennyNeural |

Natural voice selection - no manual voice picking needed!

---

## Video Selection Logic

Videos are selected based on **Theme + Keyword**:

### Theme → Search Queries Mapping

| Theme | Search Queries |
|-------|----------------|
| **temple** | temple, prayer, meditation, worship |
| **nature** | forest, nature, landscape, green |
| **success** | sunrise, mountain, achievement, goal |
| **motivation** | motivation, inspire, goal, ambitious |
| **fitness** | workout, exercise, gym, fitness |
| **meditation** | meditation, peaceful, calm, relaxing |
| **daily_life** | lifestyle, morning, routine, daily |

**System fetches 4-6 videos**, splits script to sentences, and **1 sentence = 1 video clip** with synchronized timing.

---

## Music Selection Logic

Music is fetched based on **Music Type + Keyword**:

| Music Type | Search Query |
|-----------|--------------|
| **calm** | calm peaceful relaxing background music |
| **motivational** | cinematic motivational inspirational music |
| **spiritual** | meditation spiritual devotional music |
| **upbeat** | happy cheerful upbeat background music |

If Freesound fails → Falls back to local music library.

---

## Complete Example Walkthroughs

### Example 1: Hindi Spiritual Reel

**User Input:**
```bash
python main.py "Create a 30 second Hindi spiritual reel about daily temple benefits with calm devotional music and peaceful temple videos. Use male voice. Add emotional tone. Include hook and subtitles."
```

**Parsing Output:**
```
✓ Keyword: temple daily benefits
✓ Language: hindi
✓ Voice: male
✓ Mood: emotional
✓ Music: calm
✓ Theme: temple
✓ Duration: 30s
✓ Style: cinematic
→ Selected Voice: hi-IN-MadhurNeural
→ Music Search: calm spiritual devotional music temple benefits
→ Video Queries: temple by daily benefits, prayer by daily benefits, meditation by daily benefits...
```

**Script Generated:**
```
"There's a sacredness in visiting temples daily that touches your soul...
When you embrace ritual and prayer, your spirit awakens.
The divine connection through daily temple visits brings peace beyond measure.
Feel the grace of devotion transform your inner world...
[etc - 6 sentences matching emotional tone]"
```

**Reel Generated:**
- Format: 1080x1920 MP4
- Voice: Hindi male (emotional tone)
- Videos: 4-6 temple/prayer/worship clips (Pexels)
- Music: Devotional calm background
- Duration: ~30 seconds
- Hook Text: "Temple Daily Benefits" (large, 3s)
- Subtitles: One per video clip (synced to audio)
- CTA: "Follow For More Wisdom" (last 3s)

---

### Example 2: English Motivational Reel

**User Input:**
```bash
python main.py "Generate a 25 second English motivational reel about morning fitness with upbeat energetic music. Use female narrator."
```

**Parsing Output:**
```
✓ Keyword: morning fitness
✓ Language: english
✓ Voice: female
✓ Mood: motivational (default)
✓ Music: upbeat
✓ Theme: fitness
✓ Duration: 25s
→ Selected Voice: en-US-JennyNeural
→ Music Search: happy cheerful upbeat background music
→ Video Queries: morning fitness, workout exercise, gym fitness...
```

**Script Generated:**
```
"What if I told you morning fitness could transform your entire day?
Here's the secret...

First, energized body and focused mind. This is the game changer.
Second, confidence that carries through your whole day.
Third, lasting health and strength...
[etc - motivational, action-oriented tone]"
```

**Reel:**
- Voice: English female, energetic tone
- Videos: Workout/gym/fitness clips
- Music: Upbeat, energetic
- Duration: ~25s
- Cinematic zoom effects on each clip
- Professional H.264 export

---

### Example 3: Educational Reel

**User Input:**
```bash
python main.py "Create an educational reel about neem tree medicinal benefits"
```

**Parsing Output:**
```
✓ Keyword: neem tree medicinal benefits
✓ Language: english (default)
✓ Voice: female (default)
✓ Mood: educational
✓ Music: motivational (default)
✓ Theme: nature
**System knows "neem" = Indian context, considers relevance
→ Selected Voice: en-US-JennyNeural
→ Video Search: neem tree, medicinal plants, nature green...
```

**Script Generated:**
```
"Let's explore the fascinating world of neem tree medicinal benefits...

Research shows that neem leaves have powerful healing properties.
Studies confirm that neem improves skin health significantly.
Evidence demonstrates that neem supports immunity and wellness...
[etc - factual, research-driven tone]"
```

---

### Example 4: Simple Keyword (Falls Back to Legacy Mode)

**User Input:**
```bash
python main.py "Meditation"
```

**System Detection:**
- Input too short (under 20 chars)
- No action verbs (create, make, generate)
- Treated as KEYWORD

**Behavior:**
Falls back to legacy keyword-based mode:
```
→ Keyword: Meditation
→ Style: motivational (default)
→ Voice: female (default)
→ Uses existing ScriptEngine
```

---

## Fallback Mechanisms

### If Video Fails
- Retries with alternative keywords
- Falls back to local video library
- Continues without causing errors

### If Music Fails
- Tries local fallback music
- Generates voice-only reel
- Never creates silent videos

### If Voice/Parsing Fails
- Defaults to safe values
- Generates reel with sensible defaults
- Logs warnings, not errors

---

## Feature Comparison

| Feature | Prompt-Driven | Legacy |
|---------|---|---|
| Natural Language | ✓ | ✗ |
| Mood Detection | ✓ | Manual |
| Language Detection | ✓ | English only |
| Smart Voice Selection | ✓ | Limited |
| Theme-based Videos | ✓ | Keyword-based |
| Mood-matched Scripts | ✓ | Generic |
| Music Type Selection | ✓ | Random |
| Duration Parsing | ✓ | N/A |
| Batch Mode | ✓ | ✓ |
| Backward Compatible | ✓ | ✓ |

---

## Command Variations

### All VALID and understood:

```bash
# Prompt-driven (NEW):
python main.py "Hindi motivational reel about temple"
python main.py "Create emotional meditation content"
python main.py "Generate funny fitness workout video"
python main.py "Make a 45-second spiritual reel with calm music"
python main.py "Build educational content about health with male narrator"

# Legacy (still works):
python main.py --keyword "temple" --style motivational
python main.py --keyword "meditation" --voice male
python main.py --keyword "fitness" --batch 5
```

---

## Tips for Best Results

1. **Be Descriptive (But Natural)**
   - ❌ "temple"
   - ✓ "Create a spiritual reel about temple visit benefits"

2. **Include Mood if Important**
   - ❌ "reel about success"
   - ✓ "motivational reel about success"

3. **Mention Music if Specific**
   - ❌ "reel about meditation"
   - ✓ "meditation reel with calm peaceful music"

4. **Specify Voice for Personality**
   - ❌ "fitness reel"
   - ✓ "motivational fitness reel with male narrator"

5. **Add Duration for Pacing**
   - ❌ "health reel"
   - ✓ "30 second health and wellness reel"

---

## Output Format

**All reels generated with:**
- ✓ 1080x1920 vertical (Instagram Reels)
- ✓ 30 FPS
- ✓ H.264 codec
- ✓ AAC audio
- ✓ 15-25 MB typical size
- ✓ Voice duration = master timeline
- ✓ Synced subtitles
- ✓ Hook text (3s opening)
- ✓ CTA (3s closing)
- ✓ Cinematic effects (zoom, crossfade)

---

## Error Handling

System is **self-healing**:
- ✓ Failed video download? Retries automatically
- ✓ Music API down? Uses local fallback
- ✓ Script too long? Trims intelligently
- ✓ Video too short? Extends duration
- ✓ Voice unavailable? Picks similar alternative

**Never creates broken/empty reels** ✓

---

## Architecture

```
User Prompt
    ↓
PromptParser (extracts parameters)
    ↓
SmartScriptGenerator (creates mood-matched script)
    ↓
Voice Selection (language + gender + mood)
    ↓
Video Search (theme + keyword)
    ↓
Music Search (music_type + keyword)
    ↓
InstagramReelEngine (composition)
    ↓
Final Reel (1080x1920 MP4)
```

---

## Conclusion

**The system now understands natural language and generates perfect reels automatically!**

Just describe what you want, and the system handles:
- Script generation matching your mood
- Voice selection with appropriate tone
- Video fetching with relevant themes
- Music selection matching your preference
- Professional reel creation

**One prompt. Complete reel. Automatic excellence.**
