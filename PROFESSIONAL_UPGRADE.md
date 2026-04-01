# 🚀 AI REEL GENERATOR - Professional Upgrade Guide

## Overview

This is a complete professional-grade Instagram reel generator with:
- **HuggingFace AI** - Mistral-7B for non-repetitive scripts
- **Professional Subtitles** - Clean formatting with white text and black outline
- **Cinematic Effects** - Hook overlays, CTAs, zoom transitions
- **Pixabay Music** - Intelligent music fetching with fallback
- **Hindi + English** - Full bilingual support
- **Voice Synthesis** - Edge TTS with gender options
- **Production Ready** - 1080x1920, 30fps, H.264

## Architecture

### New Modules

1. **script_engine.py** - HuggingFace AI Script Generation
   - Uses Mistral-7B-Instruct-v0.2 for intelligent scripts
   - Structure: Hook + 3 Benefits + Emotion + CTA
   - Automatic repetition removal
   - Fallback template system

2. **music_engine.py** - Pixabay Music + Procedural Fallback
   - Searches Pixabay for cinematic/motivational music
   - Falls back to scipy procedural audio generation
   - Multiple music types: calm, spiritual, motivational, energetic, cinematic
   - Automatic looping and trimming

3. **video_engine.py** - Professional Video Composition
   - SubtitleSystem: Generates white text on black outline
   - HookText: 3-second intro with title
   - CTAText: 3-second outro with call-to-action
   - CinematicEffects: Zoom, transitions, composition
   - Full reel assembly with audio mixing

4. **voice_engine.py** - Edge TTS Voice Generation
   - Supports Hindi male/female, English male/female
   - Rate control: slow, normal, fast
   - Async generation with error handling

5. **main.py** - Complete Orchestrator
   - Natural language prompt parsing
   - Full 6-step pipeline
   - Debug logging and progress tracking
   - Error recovery and fallbacks

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Key packages:
- `transformers` - HuggingFace models
- `torch` - Deep learning framework
- `scipy` - Procedural audio
- `moviepy` - Video processing
- `edge-tts` - Voice synthesis
- `requests` - API calls

### 2. Set Up API Keys

**HuggingFace API Key** (set via environment variable):
```
set HUGGINGFACE_API_KEY=your_key_here
```

**Pixabay API Key** (optional, for music):
```bash
set PIXABAY_API_KEY=your_key_here
```

**Pexels API Key** (optional, for videos):
```bash
set PEXELS_API_KEY=your_key_here
```

## Quick Start

### Basic Usage

```bash
# Hindi reel about yoga
python main.py "Create a Hindi motivational reel about yoga benefits"

# English reel about meditation
python main.py "Generate English spiritual reel about meditation"

# Cinematic reel
python main.py "Create a cinematic reel about temple visit with epic music"
```

### Advanced Usage

```bash
# Specify everything
python main.py "Create an English funny reel about fitness with energetic music and female voice"

# Hindi version
python main.py "हिंदी में ऐक रील बनाओ temple के फायदों के बारे में"
```

## Pipeline Steps

### STEP 1: PARSE PROMPT (ReelPromptParser)
- Extracts keyword, language, mood, music type, voice type
- Detects Hindi/English automatically
- Identifies mood: motivational, emotional, spiritual, educational, funny
- Selects music type and voice gender

```
Input:  "Create a Hindi motivational reel about yoga"
Output: {
  keyword: "yoga",
  language: "hindi",
  mood: "motivational",
  music_type: "cinematic",
  voice_type: "male"
}
```

### STEP 2: GENERATE AI SCRIPT (HuggingFace)
- Uses Mistral-7B-Instruct model
- Structure:
  - Hook question (3-5 words)
  - Benefit 1 (8-12 words)
  - Benefit 2 (8-12 words)
  - Benefit 3 (8-12 words)
  - Emotional line (10-15 words)
  - CTA (5-8 words)
- Total: 5-6 sentences, non-repetitive
- Fallback: Template-based generation if HF unavailable

```
Example Hindi Output:
"क्या आप जानते हैं कि yoga आपके जीवन को बदल सकता है?
आपका शरीर मजबूत, लचकदार और स्वस्थ हो जाता है।
तनाव और चिंता दूर हो जाती है हर सांस के साथ।
मन शांति और स्पष्टता पाता है।
लेकिन याद रखें, सच्चा फायदा पाने के लिए निरंतरता जरूरी है।
तो अभी शुरू करें।"
```

### STEP 3: FETCH VIDEO CLIPS (Pexels)
- Searches for 10 video clips matching keyword
- Minimum 3 clips required
- Fallback search with mood keywords
- Each clip auto-trimmed to sentence duration

### STEP 4: GENERATE VOICE (Edge TTS)
- Uses neural voices:
  - Hindi: MadhurNeural (male), SwaraNeural (female)
  - English: BrianNeural (male), JessicaNeural (female)
- Async generation for speed
- Output: MP3 file with duration metadata

### STEP 5: FETCH BACKGROUND MUSIC (Pixabay)
- Searches for cinematic/motivational music
- Falls back to procedural audio generation (scipy)
- Music types:
  - Calm: Ambient pads with peaceful frequencies
  - Spiritual: Devotional frequencies
  - Motivational: Uplifting nature sounds
  - Energetic: Dynamic filtered noise
  - Cinematic: Epic ambient combinations

### STEP 6: CREATE PROFESSIONAL REEL (VideoEngine)
- Duration allocation:
  - Hook: 3 seconds (title overlay)
  - Content: remaining voice duration
  - CTA: 3 seconds (follow call overlay)
- Subtitles: One per sentence, white on black outline
- Audio mixing:
  - Voice: 100% volume
  - Music: 12% volume
- Final export: 1080x1920, 30fps, H.264, AAC

## Output Structure

```
output/
├── reel_hindi_yoga_20260401_120000.mp4     ← Final reel
├── (other reels...)
```

Each reel includes:
- ✓ 3-second hook with title
- ✓ 5-6 sentence content with synced subtitles
- ✓ 3-second CTA with follow-up message
- ✓ Background music at 12% volume
- ✓ Voice at 100% volume
- ✓ Professional 1080x1920 dimensions

## Subtitle System

### Text Formatting
- **Font**: Arial Bold (size 50)
- **Color**: White (#FFFFFF)
- **Outline**: Black (width 3px)
- **Position**: Bottom center
- **Max width**: 80% of video width
- **Auto wrap**: Intelligent word boundaries

### Generation Process
1. Split script into sentences
2. Create one image per sentence
3. Each image: 1080x1920 transparent PNG
4. Text centered with automatic line wrapping
5. Black outline for readability on any video

## Hook System

### First 3 Seconds
- Large title text (size 80, gold color)
- Format: "Benefits Of [KEYWORD]" (English)
- Format: "[KEYWORD] के फायदे" (Hindi)
- Semi-transparent black background
- Centered on screen

## CTA System

### Last 3 Seconds
- Follow call text (size 60, white)
- English: "Follow for More Knowledge\nDon't Miss Out!"
- Hindi: "और सीखने के लिए Follow करें!"
- Semi-transparent black background
- Bottom center position

## Debug Output

The system prints detailed logs:
```
[PARSE] Analyzing prompt...
[PARSE] Detected language: HINDI
[PARSE] Keyword: yoga
[SCRIPT] Generated 6 sentences
[VIDEO] Processing 10 video clips
[VOICE] Generated voice audio
[MUSIC] Music acquired
[VIDEO] Creating professional reel
[VIDEO] ✓✓✓ REEL COMPLETE
```

## Error Handling & Fallbacks

### Script Generation
- Primary: HuggingFace Mistral-7B
- Fallback: Template-based generation

### Music Fetching
- Primary: Pixabay API
- Fallback: Procedural audio (scipy)
- Final: Voice-only if no music available

### Video Clips
- Requirement: Minimum 3 clips
- Auto-retry on load failure
- Speed adjustment if clip too short

### Voice Generation
- Primary: Edge TTS neural voices
- Supports: Hindi, English, Male, Female

## Performance

- **Script Generation**: ~15-30 seconds (HuggingFace)
- **Video Fetching**: ~30-60 seconds (Pexels)
- **Voice Generation**: ~10-20 seconds (Edge TTS)
- **Music Fetching**: ~10-30 seconds (Pixabay)
- **Reel Creation**: ~2-5 minutes (video encoding)
- **Total Time**: ~5-10 minutes per reel

## Troubleshooting

### Issue: "No videos found"
- Check Pexels API key
- Try different keywords
- System will fall back to alternative searches

### Issue: "Music not applied"
- Pixabay API key may be missing
- System will generate procedural audio fallback
- Check if scipy is installed

### Issue: "Voice generation failed"
- Verify internet connection
- Check Edge TTS availability
- Restart process

### Issue: "Low quality subtitles"
- Check font availability on system
  - Windows: C:\Windows\Fonts\arial.ttf
  - Linux: /usr/share/fonts/truetype/dejavu/
- Increase font size in SubtitleSystem

## Advanced Configuration

In `main.py`, modify `CONFIG` dict:

```python
CONFIG = {
    'output_dir': 'output',           # Output directory
    'audio_dir': 'audio',              # Voice audio
    'music_dir': 'music',              # Background music
    'video_width': 1080,               # Reel width
    'video_height': 1920,              # Reel height
    'video_fps': 30,                   # Frame rate
    'voice_rate': 'normal',            # Voice speed
    'music_volume': 0.12,              # Music mix volume
}
```

## Examples

### Example 1: Hindi Yoga Reel
```bash
python main.py "Create a Hindi motivational reel about yoga benefits"
```
**Output**:
- Script in Hindi with yoga benefits
- Yoga videos from Pexels
- Hindi male voice (Madhur)
- Cinematic music from Pixabay
- Professional subtitles
- Hook: "YOGA के फायदे"
- CTA: "और सीखने के लिए Follow करें!"

### Example 2: English Meditation Reel
```bash
python main.py "Generate spiritual reel about meditation with calm music"
```
**Output**:
- Script in English about meditation
- Meditation videos
- English male voice (Brian)
- Calm procedural music
- White subtitles on black outline
- Hook: "Benefits Of Meditation"
- CTA: "Follow for More Knowledge"

### Example 3: English Temple Reel
```bash
python main.py "Create cinematic reel about temple visit with epic background music"
```
**Output**:
- Script structured for temple benefits
- Temple/spiritual videos
- Cinematic music
- Professional composition
- All elements synced

## Important Notes

1. **First Run**: HuggingFace model downloads (~2.8GB), takes 1-2 minutes
2. **GPU Recommended**: For faster script generation (optional)
3. **Internet Required**: For Pexels, Pixabay, HuggingFace APIs
4. **Font Support**: Ensure Arial or DejaVu fonts available for subtitles
5. **Storage**: Each reel ~10-20MB, budget disk space accordingly

## Next Steps

1. Install requirements: `pip install -r requirements.txt`
2. Set environment variables (optional): `PIXABAY_API_KEY`, `PEXELS_API_KEY`
3. Test with: `python main.py "Create a motivational reel about success"`
4. Monitor output in `output/` directory

## Support

For issues:
1. Check logs in terminal output
2. Verify API keys set correctly
3. Ensure all dependencies installed
4. Check internet connectivity
5. Try with simple prompt first

---

**Created**: April 1, 2026
**Version**: 2.0 Professional
**Status**: Production Ready ✅
