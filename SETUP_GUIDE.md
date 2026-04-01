# 🚀 SETUP & QUICK START GUIDE

## Step 1: Install Python Dependencies

### Windows PowerShell:
```powershell
pip install -r requirements.txt
```

### If you get permission errors:
```powershell
pip install --user -r requirements.txt
```

### If moviepy fails to install:
```powershell
pip install moviepy==1.0.3 --no-cache-dir
```

## Step 2: Install FFmpeg (REQUIRED)

### Windows - Using Chocolatey (Recommended):
```powershell
choco install ffmpeg
```

### Windows - Manual Download:
1. Download from: https://ffmpeg.org/download.html
2. Extract to a folder (e.g., `C:\ffmpeg`)
3. Add to Windows PATH:
   - Press `Win + X` → System
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Click "Path" → "Edit"
   - Click "New" and add: `C:\ffmpeg\bin`
   - Click OK → OK → Restart your computer

### Verify FFmpeg:
```powershell
ffmpeg -version
```

## Step 3: Prepare Your Content

### Add Topics (topics.txt)
Open `topics.txt` and add your topics (one per line):
```
Benefits of trees
Save environment
Plant neem tree
Nature motivation
Tree business ideas
Sustainable development
Climate change facts
```

### Add Images (images/ folder)
1. Create or collect vertical images (1080x1920 recommended)
2. Supported formats: JPG, PNG, BMP, GIF, WebP
3. Place them in the `images/` folder
4. Recommended: At least 20-30 images for variety

### Add Music (music/ folder - OPTIONAL)
1. Add background music files to `music/` folder
2. Supported formats: MP3, WAV, AAC, M4A, FLAC
3. Recommended: 30 seconds to 2 minutes per song
4. If empty, system works without background music

## Step 4: Validate Your Setup

Run this to verify everything is working:
```powershell
python main.py --validate
```

You should see:
```
✓ All dependencies installed
✓ Directory 'audio' ready
✓ Directory 'images' ready
✓ Directory 'music' ready
✓ Directory 'output' ready
✓ Directory 'scripts' ready
✓ All validations passed!
```

## Step 5: Generate Your First Reel

### Simple Mode (Random Topic):
```powershell
python main.py
```

### With Specific Topic:
```powershell
python main.py --topic "Save environment"
```

### Without Background Music:
```powershell
python main.py --no-music
```

### With Custom Number of Images:
```powershell
python main.py --images 8
```

### Combined Options:
```powershell
python main.py --topic "Your Topic" --images 5 --no-music
```

## Step 6: Find Your Generated Video

1. Open the `output/` folder
2. Look for `reel_YYYYMMDD_HHMMSS.mp4`
3. This is your finished video!

## Step 7: Upload & Share

Choose your platform:

### YouTube Shorts:
1. Go to https://www.youtube.com/upload
2. Upload the MP4 file
3. Copy the captions from console output
4. Add hashtags
5. Publish!

### Instagram Reels:
1. Open Instagram → Create
2. Select "Reels"
3. Upload your video
4. Add captions and hashtags
5. Share!

### TikTok:
1. Open TikTok → Create (+)
2. "Upload a video"
3. Select your MP4
4. Add effects and music
5. Post!

## 📊 What Gets Generated

For each reel, you get:

1. **Video File**: `output/reel_*.mp4` (1080x1920)
2. **Voice File**: `audio/voice_*.mp3` (reusable)
3. **Console Output**: 
   - Topic
   - Generated script
   - Captions (copy-paste ready)
   - Hashtags (copy-paste ready)
4. **Log File**: `reel_generator.log` (for debugging)

## ⚡ Quick Command Reference

```powershell
# Generate one reel with random topic
python main.py

# Generate with specific topic
python main.py --topic "Your topic"

# Change number of images (3-15 recommended)
python main.py --images 5

# Generate without music
python main.py --no-music

# Generate 5 reels in batch
python main.py --batch 5

# Validate setup
python main.py --validate

# Show all options
python main.py --help
```

## 🔧 Troubleshooting

### Error: "FFmpeg not found"
**Fix**: Make sure FFmpeg is installed and in PATH
```powershell
ffmpeg -version  # Should show version info
```

### Error: "No images found in images folder"
**Fix**: Add at least one image to `images/` folder

### Error: "No topics found in topics.txt"
**Fix**: Add topics to `topics.txt` (one per line)

### Error: "ModuleNotFoundError: No module named 'moviepy'"
**Fix**: Reinstall dependencies
```powershell
pip install --upgrade --force-reinstall moviepy
```

### Video is slow or fails mid-generation
**Fix**: 
- Close other applications
- Reduce image count: `--images 3`
- Use `--no-music` option
- Check disk space (need ~500MB free)

### Audio not heard in video
**Fix**: Check that audio file was created
```powershell
ls audio/  # Should show voice_*.mp3 file
```

## 📝 Customization Examples

### Generate 10 images with specific topic:
```powershell
python main.py --topic "Nature facts" --images 10
```

### Batch generate without music (faster):
```powershell
python main.py --batch 5 --no-music
```

### Use fewer images (faster generation):
```powershell
python main.py --images 3
```

## 📂 Folder Structure After First Run

```
ai-reel-automation/
├── audio/
│   └── voice_20240101_120000.mp3     ← Generated voice
├── images/
│   ├── image1.jpg                    ← Your images
│   ├── image2.png
│   └── ...
├── music/
│   └── background.mp3                ← Your music (optional)
├── output/
│   └── reel_20240101_120000.mp4      ← Your finished video!
└── reel_generator.log                ← Detailed logs
```

## 🎯 Success Checklist

✅ Python 3.8+ installed
✅ Dependencies installed (`pip install -r requirements.txt`)
✅ FFmpeg installed and in PATH
✅ At least one topic in `topics.txt`
✅ At least one image in `images/` folder
✅ Validation passes (`python main.py --validate`)
✅ Generated one test reel successfully
✅ Video found in `output/` folder
✅ Ready to upload and share!

## 🚀 Next Level: Batch Production

Once you're comfortable, generate multiple reels:

```powershell
# Generate 20 reels for a week's worth of content
python main.py --batch 20

# All videos will be in output/ folder
# Ready to schedule uploads!
```

## 📞 Need Help?

1. Check the console output for error messages
2. Look at `reel_generator.log` for detailed logs
3. Run `python main.py --validate` to check setup
4. Ensure all prerequisites are installed

## 🎬 You're Ready!

You now have everything needed to:
- Generate professional AI-powered reels
- Mix voice and music perfectly
- Create 1080x1920 vertical videos
- Auto-generate captions and hashtags
- Upload to any social platform

**Start generating reels now:**
```powershell
python main.py
```

Enjoy! 🎉
