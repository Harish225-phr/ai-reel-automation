# 📋 Command Reference Guide

## Installation (One-Time Setup)

```bash
# Install Python packages
pip install -r requirements.txt

# Install FFmpeg
# Windows: choco install ffmpeg
# macOS: brew install ffmpeg
# Linux: sudo apt-get install ffmpeg

# Verify setup
python main.py --validate
```

## Basic Commands

### Generate Single Reel
```bash
python main.py
```
Generates one reel with random topic from topics.txt

### Generate with Specific Topic
```bash
python main.py --topic "Save environment"
```
Generate reel with your chosen topic

### Generate Multiple Reels (Batch)
```bash
python main.py --batch 5
```
Generate 5 reels consecutively

### Remove Background Music
```bash
python main.py --no-music
```
Faster generation without background music

### Adjust Number of Images
```bash
python main.py --images 8
```
Use 8 images instead of default 5

## Combined Options

### Specific topic with 8 images:
```bash
python main.py --topic "Nature facts" --images 8
```

### Batch of 10 reels without music:
```bash
python main.py --batch 10 --no-music
```

### Specific topic, no music, 3 images (fastest):
```bash
python main.py --topic "Quick tip" --no-music --images 3
```

## Utility Commands

### Validate Your Setup
```bash
python main.py --validate
```
Check if all dependencies and files are ready

### Show Help
```bash
python main.py --help
```
Display all available options with descriptions

### Test Individual Modules

#### Test Voice Generation
```bash
python voice.py
```
Generate test voice and show audio properties

#### Test Video Creation
```bash
python video.py
```
Show video module documentation

#### Test Upload Module
```bash
python upload.py
```
Show upload guide and instructions

## Module Usage (Python Code)

### In Python Script or Interactive Shell

#### Single Reel Generation
```python
from main import generate_complete_reel

reel = generate_complete_reel()
print(f"Video: {reel['video_path']}")
print(f"Duration: {reel['video_duration']}s")
print(f"Topic: {reel['topic']}")
```

#### Batch Generation
```python
from main import batch_generate_reels

reels = batch_generate_reels(count=5, include_music=True)
print(f"Generated {len(reels)} reels")
```

#### Custom Voice Generation
```python
from voice import generate_voice_from_topic

voice = generate_voice_from_topic(
    topic="Your topic",
    language='en'
)
print(f"Audio: {voice['audio_path']}")
print(f"Script: {voice['script']}")
```

#### Custom Video Creation
```python
from video import generate_reel

result = generate_reel(
    audio_path="audio/voice_123.mp3",
    topic="My Video",
    num_images=10,
    include_music=True
)
print(f"Video: {result['video_path']}")
```

## Output Files

### Video Location
```
output/
├── reel_20240101_120000.mp4
├── reel_20240101_120015.mp4
└── ... (one per generation)
```

### Audio Location
```
audio/
├── voice_20240101_120000.mp3
├── voice_20240101_120015.mp3
└── ... (one per generation)
```

### Logs
```
reel_generator.log  (accumulates, updated with each run)
```

## File Management

### Clear Old Logs
```bash
del reel_generator.log  # Windows
rm reel_generator.log   # macOS/Linux
```

### Clean Temporary Files
The system auto-cleans temporary files, but to manually remove:
```bash
del audio\*_prepared.jpg  # Windows
rm audio/*_prepared.jpg   # macOS/Linux
```

## Troubleshooting Commands

### Check Python Version
```bash
python --version  # Should be 3.8 or higher
```

### Check FFmpeg
```bash
ffmpeg -version
```

### Check Installed Packages
```bash
pip list | findstr moviepy  # Windows
pip list | grep moviepy      # macOS/Linux
```

### Reinstall Specific Package
```bash
pip install --upgrade moviepy
pip install --upgrade gtts
pip install --upgrade Pillow
```

### Test Internet Connection (for gTTS)
```bash
python -c "from gtts import gTTS; print('✓ gTTS OK')"
```

## Advanced Flags

### Future Flag Examples (when implemented)
```bash
# Quality settings (if added)
python main.py --quality high

# Output format (if added)
python main.py --format mkv

# Watermark (if added)
python main.py --watermark "MyBrand"

# Language (if expanded)
python main.py --language es  # Spanish
```

## Performance Tips

### Fastest Generation
```bash
python main.py --images 3 --no-music
```
Time: ~1-2 minutes

### Balanced Generation
```bash
python main.py --images 5 --no-music
```
Time: ~2-3 minutes

### Best Quality
```bash
python main.py --images 10
```
Time: ~5-8 minutes

### Batch Production (10 reels at once)
```bash
python main.py --batch 10 --no-music
```
Time: ~15-25 minutes total

## Uploading

### YouTube Shorts
1. Generate reel: `python main.py`
2. Go to https://www.youtube.com/upload
3. Upload from `output/` folder
4. Copy captions from console
5. Publish!

### Instagram Reels
1. Generate reel: `python main.py`
2. Open Instagram → Create
3. Select "Reels"
4. Upload from `output/` folder
5. Share!

### TikTok
1. Generate reel: `python main.py`
2. Open TikTok → Create
3. "Upload a video"
4. Select from `output/` folder
5. Post!

## Scripting Examples

### Scheduled Generation (Windows Task Scheduler)
Create batch file: `generate_reel.bat`
```batch
@echo off
cd D:\Python\ai-reel-automation
python main.py
```

### Automated Daily Generation (using Python)
```python
import schedule
import time
import subprocess

def generate_daily():
    subprocess.run(["python", "main.py"])

schedule.every().day.at("10:00").do(generate_daily)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Environment Variables (Optional)

### Custom Topics File
```bash
set TOPICS_FILE=my_topics.txt
python main.py
```

### Custom Output Directory
```bash
set OUTPUT_DIR=D:\Videos
python main.py
```

## One-Liners

### Generate and report success
```bash
python main.py && echo ✓ Reel generated!
```

### Generate multiple times
```bash
for /L %i in (1,1,5) do python main.py  # Windows
for i in {1..5}; do python main.py; done # macOS/Linux
```

### Quick batch (no music, fewer images)
```bash
python main.py --batch 3 --no-music --images 3
```

## Performance Benchmarks

| Command | Time | Output |
|---------|------|--------|
| `python main.py --images 3 --no-music` | ~1m 30s | Quick test video |
| `python main.py --images 5` | ~3-4m | Balanced quality |
| `python main.py --images 10` | ~6-8m | High quality |
| `python main.py --batch 5 --no-music` | ~8-10m | 5 videos quick |
| `python main.py --batch 5` | ~15-20m | 5 videos with music |

## Getting Help

### Check Logs
```bash
tail -f reel_generator.log        # macOS/Linux (live view)
Get-Content reel_generator.log -Tail 20  # Windows (last 20 lines)
```

### Validate Setup
```bash
python main.py --validate
```

### Show All Options
```bash
python main.py --help
```

---

**Quick Start:**
```bash
pip install -r requirements.txt
python main.py --validate
python main.py
```

**Next Upload:**
Open `output/` folder and upload your MP4 to YouTube/Instagram/TikTok!
