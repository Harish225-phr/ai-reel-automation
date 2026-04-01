# AI Reel Automation - Professional Update Guide

## 🎬 NEW FEATURES - Pexels API & Freesound Integration

Your AI reel generator has been upgraded with professional stock media APIs:

### ✨ What's New

1. **Pexels API Integration** - HD Stock Videos
   - Automatic search and download of vertical videos
   - Filters: height ≥ 1280px, width ≥ 720px
   - 3-5 professional stock videos per reel
   - Saved to: `content/videos/`

2. **Freesound API Integration** - Royalty-Free Music
   - Automatic background music selection
   - Searches: motivational, cinematic, nature themes
   - MP3 format, auto-looped to match voice duration
   - Saved to: `assets/music/`

3. **Enhanced Video Quality**
   - Crossfade transitions between clips (0.3s)
   - Ken Burns zoom effect (1.1x)
   - Proper vertical format handling (1080x1920)
   - H264 codec, 24fps export

4. **Improved Audio Mixing**
   - Voice: 100% volume
   - Music: 15% volume (background)
   - Automatic music looping to match voice duration
   - CompositeAudioClip for professional mixing

5. **Better Text Overlays**
   - Hook text: 0-3 seconds (BIG FONT, center)
   - Captions: Bottom center, synced to voice
   - CTA: Last 3 seconds (FOLLOW FOR MORE)

---

## 🚀 Quick Start

### Installation

```bash
# Install new dependencies
pip install requests edge-tts

# Or install all requirements
pip install -r requirements.txt
```

### Configuration

API keys are already configured in `config.py`:

```python
PEXELS_API_KEY = "WpFsET9nVh30a0g2qOErgaePd7GuA7D8HKfOUFcaeLTJr6C6xHGT7nFv"
FREESOUND_API_KEY = "ul0LhS7Nji1TiF5EAxSwIrNkSMpjfTjFsVKSDeSI"
```

### Generate a Reel

```bash
# Simple usage
python main.py "Neem tree benefits"

# With style
python main.py "Neem tree benefits" --style educational

# Male narrator
python main.py "Neem tree benefits" --voice male

# Batch mode (5 reels)
python main.py "Neem tree benefits" --batch 5
```

---

## 📁 New Files Created

### 1. `media_fetcher.py` - Pexels API Integration
Handles stock video fetching from Pexels API.

**Key Classes:**
- `PexelsMediaFetcher`: Main fetcher class
- `get_fallback_videos()`: Local fallback

**Methods:**
- `search_videos(query, per_page=5)`: Search Pexels
- `filter_videos(videos, min_width=720, min_height=1280)`: Filter by size
- `get_best_video_url(video_data)`: Extract HD URL
- `download_video(url, filename)`: Download MP4
- `search_and_download(keyword, count=5)`: Full pipeline with retry

**Example:**
```python
from media_fetcher import PexelsMediaFetcher

fetcher = PexelsMediaFetcher()
videos = fetcher.search_and_download("motivation", count=5)
# Returns: ['/path/to/video1.mp4', '/path/to/video2.mp4', ...]
```

### 2. `music_fetcher.py` - Freesound API Integration
Handles background music fetching from Freesound API.

**Key Classes:**
- `FreesoundMusicFetcher`: Main fetcher class
- `get_fallback_music()`: Local fallback

**Methods:**
- `search_sounds(query, limit=15)`: Search Freesound
- `filter_sounds_by_license(sounds)`: Filter royalty-free
- `filter_by_duration(sounds, max_duration=180)`: Filter by length
- `get_download_url(sound_data)`: Extract MP3 URL
- `download_music(url, filename)`: Download MP3
- `search_and_download(keywords, count=1)`: Full pipeline with retry

**Example:**
```python
from music_fetcher import FreesoundMusicFetcher

fetcher = FreesoundMusicFetcher()
music = fetcher.search_and_download(count=1)
# Returns: ['/path/to/music.mp3']
```

---

## 🔧 Updated Files

### 1. `config.py`
Added API configuration:
```python
PEXELS_API_KEY = "..."
FREESOUND_API_KEY = "..."
CONTENT_VIDEOS_DIR = 'content/videos'
CONTENT_IMAGES_DIR = 'content/images'
ENABLE_PEXELS_API = True
ENABLE_FREESOUND_API = True
CROSSFADE_DURATION = 0.3  # New
```

### 2. `engine/video_engine_pro.py`
Improved video handling:
- Better crossfade transitions
- Improved zoom effect application
- Video cropping for vertical format
- Better duration matching
- Enhanced logging

Key improvements:
```python
# Crossfade between clips for smooth transitions
@staticmethod
def apply_crossfade(clip, duration=0.3):
    return clip.crossfadeout(duration).crossfadein(duration)

# Take middle portion of videos for better content
if video.duration > clip_duration:
    start = (video.duration - clip_duration) / 2
    video = video.subclip(start, start + clip_duration)
```

### 3. `main.py`
Integrated new API fetcher imports and updated workflow:

**Old Workflow:**
```
generate_script → generate_voice → fetch_videos (legacy) → 
select_music (local) → create_reel
```

**New Workflow:**
```
generate_script → generate_voice → fetch_videos (Pexels API) → 
fetch_music (Freesound API) → create_reel
```

### 4. `requirements.txt`
Added dependencies:
```
requests==2.31.0
edge-tts==6.1.6
```

---

## 📊 System Architecture

```
┌─────────────────────────────────────┐
│         User Input (Keyword)        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│     ScriptEngine (Text Generation)   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Voice Engine (Edge TTS)            │
│   ⭐ Master Timeline Control         │
└──────────────┬──────────────────────┘
               │
      ┌────────┴────────┐
      │                 │
      ▼                 ▼
PexelsMediaFetcher  FreesoundMusicFetcher
(HD Vertical)        (Royalty-Free)
      │                 │
      └────────┬────────┘
               │
               ▼
┌─────────────────────────────────────┐
│    VideoEngine (Composition)        │
│ • Crossfade transitions             │
│ • Zoom effects                      │
│ • Audio mixing (voice+music)        │
│ • Caption overlay                  │
│ • Hook & CTA text                  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Professional Reel (1080x1920)      │
│  MP4 H264 @ 24fps                   │
└─────────────────────────────────────┘
```

---

## ⚙️ Configuration Reference

### Video Format (Instagram Reels)
```python
VIDEO_WIDTH = 1080          # Vertical reel width
VIDEO_HEIGHT = 1920         # Vertical reel height
VIDEO_FPS = 24              # Frame rate
VIDEO_CODEC = 'libx264'     # H.264 codec
```

### Audio Mixing
```python
VOICE_VOLUME = 1.0          # 100%
MUSIC_VOLUME = 0.15         # 15%
FADE_DURATION = 0.5         # Fade in/out
```

### Video Effects
```python
ENABLE_ZOOM = True
ZOOM_FACTOR = 1.1           # 1.1x zoom
ENABLE_CROSSFADE = True
CROSSFADE_DURATION = 0.3    # 300ms transitions
```

### Text & Overlays
```python
HOOK_DURATION = 3.0         # First 3 seconds
HOOK_FONT_SIZE = 120        # BIG FONT
CAPTION_FONT_SIZE = 60      # Subtitles
CTA_FONT_SIZE = 80          # Call-to-action
```

### Pexels Filtering
```python
# Fetches videos with:
# - Height >= 1280px
# - Width >= 720px
# - Highest quality available
# - Vertical orientation
```

### Freesound Filtering
```python
# Downloads music with:
# - Creative Commons license
# - Duration: 5-180 seconds
# - Highest rated results
# - Quality MP3 format
```

---

## 🎯 Complete Workflow Example

### Step 1: Run the system
```bash
python main.py "Productivity tips"
```

### Step 2: What happens internally

```
[STEP 1] Generate script from keyword
  → "Productivity tips" 
  → Hook: "Start your day right"
  → Script: ~400 words

[STEP 2] Generate voice using Edge TTS
  → Duration: 25 seconds (MASTER TIMELINE)
  → Saves: audio/voice_20240331_123456.wav

[STEP 3] Fetch Pexels videos
  → Search: "productivity tips"
  → Filter: height>=1280, width>=720
  → Download: 5 HD vertical videos
  → Saves: content/videos/productivity_tips_*.mp4

[STEP 4] Fetch Freesound music
  → Search: ["motivational music", "cinematic background", ...]
  → Filter: CC license, 5-180s
  → Download: Best match
  → Saves: assets/music/music.mp3

[STEP 5] Create professional reel
  ✓ Load videos, crop to 1080x1920
  ✓ Apply zoom Ken Burns effects
  ✓ Add crossfade transitions (0.3s)
  ✓ Mix audio: voice (100%) + music (15%)
  ✓ Add hook text (0-3s)
  ✓ Add captions synced to voice
  ✓ Add CTA (last 3s)
  ✓ Export: 1080x1920 MP4 H264 @ 24fps
  → Output: output/reel_20240331_123456.mp4
```

### Step 3: Output
```
File: output/reel_20240331_123456.mp4
Size: 45.2 MB
Duration: 25 seconds
Format: 1080x1920 MP4 H264

Ready for:
  ✓ Instagram Reels
  ✓ YouTube Shorts
  ✓ TikTok
```

---

## 🐛 Error Handling

### If Pexels API fails:
1. Retries with related keywords
2. Falls back to local videos in `content/videos/`
3. Falls back to images
4. Falls back to black background

### If Freesound API fails:
1. Looks for local music in `assets/music/`
2. Falls back to voice-only reel
3. Logs warning but continues

### If APIs are disabled:
Set in `config.py`:
```python
ENABLE_PEXELS_API = False    # Use local/fallback
ENABLE_FREESOUND_API = False # Use local/fallback
```

---

## 📝 API Documentation Links

- **Pexels API**: https://www.pexels.com/api/
  - Videos endpoint: `/videos/search`
  - Filter by dimensions in app

- **Freesound API**: https://freesound.org/api/
  - Search endpoint: `/search/text/`
  - CC license filtering built-in

---

## 🎓 Best Practices

### For Best Results:

1. **Keyword selection**
   - Use specific, searchable keywords
   - Example: "yoga meditation" (Good) vs "zen" (Less specific)

2. **Video composition**
   - Videos auto-scale to 1080x1920
   - Crossfade creates smooth transitions
   - Zoom effect adds cinematic feel

3. **Audio mixing**
   - Voice at 100% ensures clarity (master timeline)
   - Music at 15% provides background without overwhelming
   - Duration automatically synced

4. **Text overlays**
   - Hook (first 3s) catches attention
   - Captions sync to voice (~2.5s each)
   - CTA (last 3s) drives action

---

## 🚨 Troubleshooting

### "PEXELS_API_KEY not configured"
→ Check that API key is correctly set in `config.py`

### "No videos found"
→ Try a simpler keyword or check your internet connection

### "No royalty-free music"
→ System will voice-only mode, or check `assets/music/` for local files

### "Video too large"
→ Normal - reels are typically 40-60 MB for 24-30s at 1080x1920

### "Crossfade not working"
→ Set `ENABLE_CROSSFADE = True` in `config.py`

---

## 📞 Support

For issues:
1. Check API keys in `config.py`
2. Verify internet connection
3. Check terminal logs for detailed errors
4. Ensure all directories exist:
   - `content/videos/`
   - `assets/music/`
   - `audio/`
   - `output/`

---

## 🎉 Summary

Your system now features:
- ✅ Automatic Pexels API video fetching
- ✅ Automatic Freesound API music fetching
- ✅ Professional crossfade transitions
- ✅ Ken Burns zoom effects
- ✅ Perfect audio mixing (voice + music)
- ✅ Synchronized captions
- ✅ Professional Instagram Reel format
- ✅ Error handling with fallbacks

**Ready to generate professional reels!**

```bash
python main.py "Your keyword"
```
