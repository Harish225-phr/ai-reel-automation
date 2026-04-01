# 🚀 Quick Start Guide - 5 Minutes

## Installation (First Time Only)

```bash
cd d:\Python\ai-reel-automation
pip install moviepy Pillow pyttsx3 requests --upgrade
```

## Usage

### Single Reel
```bash
python main.py "Your keyword here"
```
Example:
```bash
python main.py "Benefits of meditation"
```
✅ Output: `output/reel_YYMMDD_HHMMSS.mp4`

### With Custom Style
```bash
python main.py "Your keyword" --style educational
```
Styles: `motivational`, `educational`, `entertaining`, `trending`

### With Custom Duration
```bash
python main.py "Your keyword" --duration 30
```

### Multiple Images
```bash
python main.py "Your keyword" --images 8
```

### Batch Mode (Generate 5 Reels)
```bash
python main.py "Your keyword" --batch 5
```

### Validate System
```bash
python main.py --validate
```

## Full Command Reference

```bash
# Single reel with all options
python main.py "Keyword" --style motivational --duration 20 --images 5

# Educational batch
python main.py "Learning topic" --style educational --batch 10

# Trending content
python main.py "Hot topic" --style trending --duration 15 --images 6

# Test setup
python main.py --validate
```

## Common Commands

| Goal | Command |
|------|---------|
| Quick video | `python main.py "Topic"` |
| Motivational | `python main.py "Topic" --style motivational` |
| Educational | `python main.py "Topic" --style educational` |
| Entertaining | `python main.py "Topic" --style entertaining` |
| Trending | `python main.py "Topic" --style trending` |
| Longer video | `python main.py "Topic" --duration 30` |
| More images | `python main.py "Topic" --images 10` |
| Batch (5x) | `python main.py "Topic" --batch 5` |
| Batch (10x) | `python main.py "Topic" --batch 10` |
| Verbose/Debug | `python main.py "Topic" --verbose` |

## Output Location

All generated videos are saved in:
```
output/reel_YYMMDD_HHMMSS.mp4
```

Example:
```
output/reel_20260331_003030.mp4
```

## File Format

- **Resolution:** 1080×1920 (vertical)
- **Duration:** 6-10 seconds (auto-adapted to voice)
- **Size:** 1-3 MB
- **ready for:** YouTube Shorts, Instagram Reels, TikTok, Facebook

## What Happens Automatically

Each reel generation includes:

1. ✅ **Script Generation** - AI creates engaging text from keyword
2. ✅ **Image Fetching** - Downloads relevant images
3. ✅ **Voice Generation** - Converts script to speech
4. ✅ **Video Creation** - Makes video with effects
5. ✅ **Music Selection** - Adds background music (if available)
6. ✅ **Export** - Saves as MP4

**Total Time:** 30-60 seconds

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "ModuleNotFoundError" | Run: `pip install moviepy --upgrade` |
| No images | Add images to `images/` folder |
| No output | Check `output/` folder |
| Slow generation | First run is slower; future runs use cache |
| API errors | System auto-fallbacks to local images |

## Tips

- **Specific keywords work better** than generic ones
- **Batch mode** generates unique content from same keyword  
- **Different styles** create different vibes - test all!
- **Add background music** to `music/` folder to include it
- **Add images** to `images/` folder for custom content

## Next Steps

1. **Try it:** `python main.py "Neem tree benefits"`
2. **Check output:** Look in `output/` folder
3. **Try styles:** Test all 4 style options
4. **Batch mode:** Generate multiple at once
5. **Upload:** Video is ready for any platform!

---

**Generate your first reel in 30 seconds!**

```bash
python main.py "Your keyword"
```

Done! Check `output/` folder for your video. 🎬✨
