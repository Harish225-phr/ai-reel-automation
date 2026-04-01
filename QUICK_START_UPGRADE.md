# 🎬 AI Reel Generator - Quick Reference

## ⚡ Quick Start (30 seconds)

```bash
# Install dependencies (if needed)
pip install requests edge-tts

# Generate a reel
python main.py "Your keyword"
```

## 📝 Usage Examples

```bash
# Basic
python main.py "Motivation"

# Educational style
python main.py "Motivation" --style educational

# Male voice
python main.py "Motivation" --voice male

# Batch (5 reels)
python main.py "Motivation" --batch 5

# Specific style
python main.py "Motivation" --style trending
```

## 📂 Output Location

```
output/reel_YYYYMMDD_HHMMSS.mp4
```

## 🎯 What Gets Downloaded

### Videos (Pexels API)
```
content/videos/
├── motivation_1.mp4
├── motivation_2.mp4
├── motivation_3.mp4
├── motivation_4.mp4
└── motivation_5.mp4
```

### Music (Freesound API)
```
assets/music/
└── motivational_music.mp3
```

### Voice (Edge TTS)
```
audio/
└── voice_20240331_123456.wav
```

## 🔧 System Workflow

```
Input Keyword
    ↓
ScriptEngine → Generate script + hook
    ↓
Voice Engine → Edge TTS voice (master timeline)
    ↓
PexelsMediaFetcher → Download 5 HD vertical videos
    ↓
FreesoundMusicFetcher → Download background music
    ↓
VideoEngine → Compose:
    • Crop to 1080x1920
    • Apply zoom effects
    • Crossfade transitions
    • Mix audio (voice 100% + music 15%)
    • Add captions
    • Add hook (0-3s)
    • Add CTA (last 3s)
    ↓
Export MP4 (H264, 24fps)
    ↓
output/reel_*.mp4
```

## 📊 Output Specs

| Property | Value |
|----------|-------|
| Resolution | 1080x1920 (vertical) |
| Format | MP4 H.264 |
| Frame Rate | 24 fps |
| Typical Duration | 20-30 seconds |
| File Size | 40-60 MB |
| Audio | Voice (100%) + Music (15%) |
| Compatible | Instagram Reels, YouTube Shorts, TikTok |

## 🎨 Text Overlays

| Element | Timing | Font Size | Position |
|---------|--------|-----------|----------|
| Hook | 0-3s | 120px | Center |
| Captions | Synced | 60px | Bottom Center |
| CTA | Last 3s | 80px | Bottom Center |

## 🎬 Video Effects

| Effect | Enabled | Parameters |
|--------|---------|------------|
| Zoom | ✓ | 1.1x (Ken Burns) |
| Crossfade | ✓ | 0.3s duration |
| Captions | ✓ | Synced to voice |
| Hook Text | ✓ | First sentence |
| CTA Text | ✓ | "FOLLOW FOR MORE" |

## 🔊 Audio Mixing

| Component | Volume | Purpose |
|-----------|--------|---------|
| Voice | 100% | Main narration (master timeline) |
| Music | 15% | Subtle background |

## 📥 Downloads

| Source | Type | Quantity | Saved To |
|--------|------|----------|----------|
| Pexels | HD Videos | 3-5 | content/videos/ |
| Freesound | MP3 Music | 1 | assets/music/ |
| Edge TTS | Voice WAV | 1 | audio/ |

## ⚙️ Configuration (config.py)

```python
# API Keys
PEXELS_API_KEY = "WpFsET9nVh30a0g2qOErgaePd7GuA7D8HKfOUFcaeLTJr6C6xHGT7nFv"
FREESOUND_API_KEY = "ul0LhS7Nji1TiF5EAxSwIrNkSMpjfTjFsVKSDeSI"

# Enable/Disable APIs
ENABLE_PEXELS_API = True
ENABLE_FREESOUND_API = True

# Video Format
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 24

# Audio Mixing
VOICE_VOLUME = 1.0      # 100%
MUSIC_VOLUME = 0.15     # 15%

# Effects
ENABLE_ZOOM = True
ZOOM_FACTOR = 1.1
ENABLE_CROSSFADE = True
CROSSFADE_DURATION = 0.3

# Text
HOOK_DURATION = 3.0
HOOK_FONT_SIZE = 120
CAPTION_FONT_SIZE = 60
CTA_FONT_SIZE = 80
```

## 🧪 Test the APIs

```bash
# Test Pexels
python -c "from media_fetcher import PexelsMediaFetcher; PexelsMediaFetcher().search_and_download('nature', count=1)"

# Test Freesound
python -c "from music_fetcher import FreesoundMusicFetcher; FreesoundMusicFetcher().search_and_download(count=1)"

# Full test
python main.py "Test"
```

## 🐛 Quick Troubleshooting

| Issue | Fix |
|-------|-----|
| "API key not found" | Check config.py |
| "No videos" | Try simpler keyword |
| "No music" | Check internet connection |
| "Video too large" | Normal (40-60 MB) |
| "Slow export" | Use ENCODING_PRESET='fast' |

## 📁 Directory Structure

```
ai-reel-automation/
├── main.py                    # Entry point
├── config.py                  # Configuration
├── media_fetcher.py          # Pexels API
├── music_fetcher.py          # Freesound API
├── content/videos/           # Downloaded videos
├── assets/music/             # Downloaded music
├── audio/                    # Generated voice
└── output/                   # Final reels
```

## 🎓 Styles Available

```
--style motivational     # Motivational content
--style educational      # Educational content
--style entertaining     # Entertainment content
--style trending         # Trending/viral content
```

## 👤 Voice Options

```
--voice female    # Female narrator (default)
--voice male      # Male narrator
```

## 📱 Platform Requirements

| Platform | Resolution | Format | Status |
|----------|------------|--------|--------|
| Instagram Reels | 1080x1920 | MP4 | ✓ Ready |
| YouTube Shorts | 1080x1920 | MP4 | ✓ Ready |
| TikTok | 1080x1920 | MP4 | ✓ Ready |
| Facebook Stories | 1080x1920 | MP4 | ✓ Ready |

## 🚀 Performance Metrics

| Metric | Value |
|--------|-------|
| Reel generation time | ~2-3 minutes |
| Video download time | ~30-60 seconds |
| Music download time | ~10-20 seconds |
| Voice generation time | ~5-10 seconds |
| Video composition time | ~60-120 seconds |
| Export time | ~30-60 seconds |

## 💾 Disk Space Requirements

| Component | Size |
|-----------|------|
| Single reel | 40-60 MB |
| Videos cache | 100-200 MB |
| Music cache | 5-10 MB |
| Audio files | 1-2 MB |
| Total per keyword | ~150-300 MB |

## 🔄 Batch Generation

```bash
# Generate 5 reels
python main.py "Motivation" --batch 5

# Output:
output/reel_20240331_123456.mp4
output/reel_20240331_123523.mp4
output/reel_20240331_123645.mp4
output/reel_20240331_123756.mp4
output/reel_20240331_123821.mp4
```

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README.md | General overview |
| PEXELS_FREESOUND_UPGRADE.md | Full upgrade guide |
| IMPLEMENTATION_GUIDE.md | Technical details |
| QUICK_START.md | This quick reference |

## 🎯 Success Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] API keys configured in `config.py`
- [ ] Directories created (content/videos/, assets/music/, etc.)
- [ ] First reel generated successfully
- [ ] Video plays on Instagram Reels
- [ ] Audio is clear and properly mixed
- [ ] Captions sync with narration
- [ ] Output file size reasonable (40-60 MB)

## 🔗 API Documentation

- **Pexels**: https://www.pexels.com/api/
- **Freesound**: https://freesound.org/api/documentation/

## 📞 Support

For issues, check:
1. `PEXELS_FREESOUND_UPGRADE.md` - Full documentation
2. `IMPLEMENTATION_GUIDE.md` - Technical details
3. Terminal output for error messages
4. `config.py` for API keys

---

## 🎉 You're All Set!

Your AI reel generator is ready to create professional Instagram reels with:
- ✅ Automatic Pexels video fetching
- ✅ Automatic Freesound music fetching
- ✅ Professional video composition
- ✅ Audio mixing and synchronization
- ✅ Synchronized captions and text overlays

**Generate your first reel:**
```bash
python main.py "Your keyword"
```

**Check the output:**
```
output/reel_YYYYMMDD_HHMMSS.mp4
```

**Enjoy! 🚀**
