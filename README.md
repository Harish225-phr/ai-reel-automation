# 🎬 AI Reel Automation System

A complete, production-level Python automation system for generating AI-powered vertical video reels with automatic voice generation, image sequencing, music mixing, and text overlays.

## 📋 Features

### Core Features
- ✅ **Automatic Topic Selection** - Randomly picks topics from `topics.txt`
- ✅ **Text-to-Speech Generation** - Uses Google TTS (gTTS) for natural voice
- ✅ **Dynamic Script Generation** - Combines topic with engaging scripts
- ✅ **Random Image Selection** - Picks images from your `images/` folder
- ✅ **Vertical Video Format** - Perfect 1080x1920 reel size (9:16 aspect ratio)
- ✅ **Image Processing** - Auto-blurs backgrounds for non-vertical images
- ✅ **Smooth Transitions** - Fade in/out effects between images
- ✅ **Background Music** - Randomly selects and mixes background music
- ✅ **Audio Mixing** - Perfectly balances voice and music volumes
- ✅ **Text Overlays** - Bold white text with topic title at bottom
- ✅ **Auto Captions** - Generates captions and hashtags

### Advanced Features
- 🔧 **Modular Architecture** - Clean separation of concerns
- 📝 **Comprehensive Logging** - Full logging to file and console
- 🛡️ **Error Handling** - Robust error handling and validation
- 💾 **File Management** - Auto-creates and manages directories
- 🔍 **Dependency Checking** - Validates all required packages
- 📦 **Batch Processing** - Generate multiple reels at once
- 🌐 **Upload Automation** - Optional Selenium-based YouTube upload
- 📊 **Progress Tracking** - Real-time progress information

## 📦 Installation

### 1. Clone/Setup Project
```bash
cd d:\Python\ai-reel-automation
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg (Required by moviepy)

**Windows:**
```bash
# Option 1: Using chocolatey
choco install ffmpeg

# Option 2: Download from https://ffmpeg.org/download.html
# Add ffmpeg/bin to your system PATH
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

### 4. Verify Installation
```bash
python main.py --validate
```

## 📁 Project Structure

```
ai-reel-automation/
├── main.py              # Main orchestration script
├── voice.py             # Voice generation module
├── video.py             # Video creation module
├── utils.py             # Helper functions & utilities
├── upload.py            # Upload automation (optional)
│
├── requirements.txt     # Python dependencies
├── README.md            # This file
│
├── topics.txt           # List of video topics
├── captions.txt         # Available captions (optional)
│
├── audio/               # Generated voice files (output)
├── images/              # Source images (input)
├── music/               # Background music (input)
├── output/              # Final video files (output)
├── scripts/             # Scripts folder (for future features)
│
└── reel_generator.log   # Generated log file
```

## 🎯 Quick Start

### Generate a Single Reel
```bash
python main.py
```

### Generate with Specific Topic
```bash
python main.py --topic "Save environment"
```

### Generate without Music
```bash
python main.py --no-music
```

### Use Specific Number of Images
```bash
python main.py --images 8
```

### Batch Generate (5 Reels)
```bash
python main.py --batch 5
```

### Validate Setup
```bash
python main.py --validate
```

## 📝 Configuration

### topics.txt
Add your desired topics, one per line:
```
Benefits of trees
Save environment
Plant neem tree
Nature motivation
Tree business ideas
```

### Add Images
- Place image files in the `images/` folder
- Supported formats: JPG, PNG, BMP, GIF, WebP
- Recommended: 1080x1920 or at least vertical orientation
- System auto-fits non-vertical images with blur background

### Add Music
- Place music files in the `music/` folder
- Supported formats: MP3, WAV, AAC, M4A, FLAC
- Music volume is automatically set to 30% to mix with voice

## 🎨 Output

Each generation produces:
- **Video File**: `output/reel_YYYYMMDD_HHMMSS.mp4`
- **Voice File**: `audio/voice_YYYYMMDD_HHMMSS.mp3`
- **Console Output**: Topic, script, and captions
- **Log File**: `reel_generator.log` (all details)

### Example Output Summary
```
╔════════════════════════════════════════════════════════════════╗
║                    REEL GENERATION SUMMARY                     ║
╚════════════════════════════════════════════════════════════════╝

📌 TOPIC
   Save environment

📝 SCRIPT
   Save environment. This is an amazing fact that everyone...

🎥 VIDEO
   Location: output/reel_20240101_120000.mp4
   Duration: 28.5 seconds
   Images: 5
   File Size: 12.45 MB
   
🔊 VOICE
   Path: audio/voice_20240101_120000.mp3
   Duration: 28.5 seconds

📱 CAPTIONS
   Save environment. This is an amazing fact...

#️⃣  HASHTAGS
   #SaveEnvironment #Motivation #Amazing #Facts...
```

## 📤 Uploading Videos

### Manual Upload (Recommended for Beginners)

1. **YouTube Shorts**
   - Go to https://www.youtube.com/upload
   - Upload video from `output/` folder
   - Copy caption from console output
   - Add hashtags
   - Publish!

2. **Instagram Reels**
   - Open Instagram → Create
   - Select "Reels"
   - Upload from `output/` folder
   - Add caption and hashtags
   - Share!

3. **TikTok**
   - Open TikTok → Create (+)
   - "Upload a video"
   - Choose from `output/` folder
   - Add caption and effects
   - Post!

### Automated Upload (Advanced)
```bash
python upload.py
# Follow the guide for YouTube automated upload
```

## 🔍 Troubleshooting

### Issue: "FFmpeg not found"
**Solution:**
```bash
# Install FFmpeg and add to PATH
# Then verify:
ffmpeg -version
```

### Issue: "No images found"
**Solution:**
- Add image files to `images/` folder
- Supported: JPG, PNG, BMP, GIF, WebP
- Ensure files have correct extensions

### Issue: "Audio file too small"
**Solution:**
- This means gTTS couldn't generate audio
- Check internet connection
- Try different topic
- Check gTTS limits (may be rate-limited)

### Issue: "Video creation is slow"
**Solution:**
- First time takes longer (FFmpeg setup)
- Reduce image count: `--images 3`
- Disable music: `--no-music`
- Use SSD instead of HDD

### Issue: "Memory error"
**Solution:**
- Close other applications
- Reduce image count
- Generate one reel at a time instead of batch

## 📊 Module Documentation

### main.py
- **`generate_complete_reel()`** - Main function to generate a complete reel
- **`batch_generate_reels()`** - Generate multiple reels sequentially
- **`generate_captions()`** - Create captions and hashtags
- **`generate_hashtags()`** - Auto-generate relevant hashtags

### voice.py
- **`generate_voice_from_topic()`** - Generate voice from topic
- **`validate_audio_file()`** - Check audio file integrity
- **`get_voice_duration()`** - Get audio duration in seconds
- **`generate_multiple_voices()`** - Batch voice generation

### video.py
- **`create_video_from_images()`** - Create video with effects
- **`prepare_image_for_reel()`** - Pre-process images
- **`generate_reel()`** - Quick video generation helper

### utils.py
- **`setup_logger()`** - Configure logging system
- **`ensure_directories()`** - Create required folders
- **`read_topics()`** - Load topics from file
- **`get_random_images()`** - Select random images
- **`get_random_music()`** - Select random music
- **`check_dependencies()`** - Validate all packages

## 🚀 Advanced Usage

### Custom Configuration
```python
from main import generate_complete_reel

reel = generate_complete_reel(
    topic="Custom Topic",
    num_images=8,
    include_music=True
)

print(f"Generated: {reel['video_path']}")
print(f"Duration: {reel['video_duration']}s")
```

### Batch Processing with Logging
```python
from main import batch_generate_reels
from utils import logger

reels = batch_generate_reels(count=10, include_music=True)

for reel in reels:
    logger.info(f"✓ {reel['topic']} - {reel['video_path']}")
```

### Custom Video Parameters
```python
from video import create_video_from_images

result = create_video_from_images(
    image_paths=image_list,
    audio_path="audio/voice.mp3",
    topic="Custom Title",
    music_path="music/background.mp3",
    image_duration=5,  # 5 seconds per image
    font_size=100,     # Larger text
    output_path="output/custom_reel.mp4"
)
```

## 📋 System Requirements

- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 500MB free space
- **Internet**: Required for gTTS voice generation
- **GPU**: Optional (speeds up video processing)
- **FFmpeg**: Required system package

## 📝 Code Quality

### Features
- ✅ Complete type hints
- ✅ Comprehensive docstrings
- ✅ Error handling for all operations
- ✅ Modular and reusable functions
- ✅ Production-level logging
- ✅ Input validation
- ✅ Resource cleanup

### Testing
Each module includes `if __name__ == "__main__"` tests:
```bash
python voice.py   # Test voice generation
python video.py   # Test video creation
python main.py    # Full workflow test
```

## 🔒 Safety & Best Practices

### File Handling
- Auto-creates missing directories
- Validates file existence before processing
- Cleans up temporary files
- Logs all file operations

### Error Handling
- Try-catch blocks for all I/O operations
- Descriptive error messages
- Graceful degradation
- User-friendly error reporting

### Logging
- All events logged to file and console
- Separate levels: DEBUG, INFO, WARNING, ERROR
- Timestamps for all entries
- Searchable log format

## 🎓 Learning Resources

### MoviePy
- Docs: https://zulko.github.io/moviepy/
- GitHub: https://github.com/Zulko/moviepy

### gTTS
- Docs: https://gtts.readthedocs.io/
- GitHub: https://github.com/pndurette/gTTS

### Selenium
- Docs: https://www.selenium.dev/documentation/
- WebDriver Manager: https://github.com/SergeyPirogov/webdriver_manager

## 📞 Support

### Debug Mode
```bash
python main.py --help  # Show all options
```

### Check Logs
```bash
tail -f reel_generator.log  # View live logs
```

### Validate Setup
```bash
python main.py --validate  # Check all systems
```

## 🎬 Example Workflows

### Workflow 1: Single Reel Generation
```bash
# Generate one reel with random topic
python main.py

# Check output/
# Upload manually to YouTube/Instagram/TikTok
```

### Workflow 2: Batch Auto-Generation
```bash
# Generate 10 reels
python main.py --batch 10

# All videos ready in output/
# Manually upload or schedule uploads
```

### Workflow 3: Specific Topic with Custom Settings
```bash
# Generate 8-image reel about trees without music
python main.py --topic "Benefits of trees" --images 8 --no-music

# Perfect for specific marketing campaigns
```

## 🛠️ Customization

### Add Custom Script Templates
Edit `voice.py` and add to `SCRIPT_TEMPLATES`:
```python
SCRIPT_TEMPLATES = [
    # ... existing templates ...
    "{topic}. Your custom template here!"
]
```

### Add Custom Hashtags
Edit `main.py` and expand `generate_hashtags()` function:
```python
if 'your_keyword' in topic_lower:
    topic_specific = ["#YourTag1", "#YourTag2"]
```

### Change Video Dimensions
Edit `video.py` constants:
```python
REEL_WIDTH = 1080
REEL_HEIGHT = 1920  # or 1080 for square videos
```

## ⚖️ License & Attribution

This project uses:
- MoviePy (MIT License)
- gTTS (MIT License)
- Selenium (Apache License 2.0)

## 🤝 Contributing

Feel free to fork, modify, and improve this system for your needs!

## 🎯 Future Enhancements

Potential features to add:
- [ ] Instagram Story automation
- [ ] TikTok direct upload
- [ ] Custom watermarks
- [ ] Multiple language support
- [ ] AI-generated images from prompts
- [ ] Video format presets for different platforms
- [ ] Analytics tracking
- [ ] Caption translation

---

**Made with ❤️ for content creators**

For issues or questions, check `reel_generator.log` or review the documentation above.

Last Updated: March 2024
Version: 1.0.0
