# 🎬 AI Automated Reel Generator - Complete System Documentation

**Fully Automated AI Video Generation System for YouTube Shorts & Instagram Reels**

Your keywords → Professional vertical video reels in seconds!

---

## ⚡ Quick Start

```bash
# Generate a single reel
python main.py "Neem tree benefits"

# With custom style
python main.py "Health tips" --style educational

# Custom duration and images
python main.py "Business mindset" --duration 30 --images 8

# Batch mode: Generate 5 reels
python main.py "Save the planet" --batch 5

# Validate system
python main.py --validate
```

---

## 🎯 What This System Does

Input a keyword → Get a professional 1080x1920 vertical video with:
- ✅ Engaging AI-generated script
- ✅ Auto-fetched relevant images
- ✅ Text-to-speech voiceover
- ✅ Ken Burns zoom effects
- ✅ Smooth transitions
- ✅ Hook text overlay
- ✅ Background music (15% volume)
- ✅ Contextual CTA message
- ✅ Ready to upload to any platform

**All in under 60 seconds!**

---

## 📚 System Modules

### **main.py** - CLI Interface & Orchestrator
- Command-line argument parsing
- Workflow management
- Batch processing
- Result summary

### **script_generator.py** - Content Generation
- 4 script styles (motivational, educational, entertaining, trending)
- AI-powered script templates
- Keyword-based content
- Auto hashtag generation

### **image_fetcher.py** - Image Acquisition
- Multi-source image fetching
- Automatic fallback system
- Retry logic on failure
- Integration with Pexels, Unsplash, Pixabay, DuckDuckGo

### **video_engine.py** - Professional Video Creation
- Ken Burns zoom effect
- Crossfade transitions
- Dynamic text overlays
- Audio mixing
- CTA generation
- 1080x1920 vertical format

### **voice.py** - Voice Generation
- Text-to-speech conversion
- MP3 output
- Script validation
- Audio file verification

### **video.py** - Legacy MoviePy Integration
- Core video composition
- Image to clip conversion
- Audio track management
- Video output processing

### **utils.py** - Utilities & Helpers
- Logging system
- Dependency checking
- Directory management
- File operations

---

## 💻 System Requirements

**Python:** 3.14+

**Core Dependencies:**
```
moviepy
Pillow (PIL)
pyttsx3
requests
```

**Optional:**
- ffmpeg (for advanced encoding)
- ImageMagick (for text effects)

**Installation:**
```bash
pip install moviepy Pillow pyttsx3 requests --upgrade
```

---

## 🎬 Usage Examples

### Example 1: Basic Single Reel
```bash
python main.py "Climate change solutions"
```
**Output:** `output/reel_YYMMDD_HHMMSS.mp4`

### Example 2: Educational Style
```bash
python main.py "Machine learning" --style educational --duration 25
```

### Example 3: Batch Content Creation
```bash
python main.py "Sustainability" --batch 10 --style motivational
```
**Output:** 10 reels generated with same keyword, unique scripts

### Example 4: Maximum Images
```bash
python main.py "Travel tips" --images 15 --style entertaining
```

### Example 5: Full Custom Setup
```bash
python main.py "Mental health awareness" \
    --style motivational \
    --duration 30 \
    --images 8 \
    --verbose
```

---

## 🎨 Script Generation Styles

### **Motivational** (Default)
Best for: Inspiration, motivation, call-to-action
```
"Stop wasting time! {keyword} does {benefit}. Check this out: {fact}. 
{insight}. Your life just changed. Share this with everyone!"
```

### **Educational**
Best for: Learning, tutorials, explanations
```
"Did you know? {keyword} has {feature}. Here's how: {fact}. 
{insight}. Understanding is essential. Learn more!"
```

### **Entertaining**
Best for: Viral content, funny facts
```
"POV: You just learned about {keyword}. {fact}. 
Reaction: {insight}. Your mind: BLOWN. Follow for surprises!"
```

### **Trending**
Best for: Current events, viral moments
```
"BREAKING: {keyword} news! {fact}. 
Why it matters: {insight}. This is HUGE. Stay updated!"
```

---

## 🖼️ Image Fetching System

**Multi-Source Fallback Architecture:**

```
Try Source 1: Unsplash → Success ✓ DONE
├─ If fail, Try Source 2: Pexels
│  ├─ If fail, Try Source 3: Pixabay
│  │  ├─ If fail, Try Source 4: DuckDuckGo
│  │  │  ├─ If fail, Retry with narrower keyword
│  │  │  │  ├─ If still fail, Use local images/ folder
│  │  │  │  └─ If no local, Use generic search
└─ Repeat until we have enough images
```

**Environment handling:**
- No API keys required (uses public endpoints)
- Graceful degradation if APIs unavailable
- Automatic retry with backoff
- Local fallback images
- Generic keyword broadening

---

## 🎥 Output Specifications

Each generated reel:
- **Resolution:** 1080 × 1920 pixels (9:16 aspect ratio)
- **FPS:** 24 frames per second
- **Format:** MP4 (H.264 + AAC)
- **Audio:** Mixed (voiceover + background music optional)
- **Duration:** Matches voiceover length (typically 6-10s)
- **File Size:** 1-3 MB (optimized for social media)
- **Upload Ready:** Direct upload to any platform

---

## 📁 Project Structure

```
ai-reel-automation/
│
├── 📄 main.py                 ← RUN THIS
├── script_generator.py        ← Script creation module
├── image_fetcher.py           ← Image downloading
├── video_engine.py            ← Video effects & creation
├── voice.py                   ← Voice generation
├── video.py                   ← MoviePy integration
├── utils.py                   ← Utilities
│
├── 📁 audio/                  ← Generated voice files
│   └── voice_reel_*.mp3
│
├── 📁 images/                 ← Downloaded/local images
│   └── reel_*.jpg
│
├── 📁 music/                  ← Background music (add your MP3s here)
│   └── background_*.mp3
│
├── 📁 output/                 ← Generated videos (DOWNLOAD THESE!)
│   └── reel_YYMMDD_HHMMSS.mp4
│
├── 📁 ffmpeg/                 ← Video encoding tools
├── topics.txt                 ← List of topics
├── captions.txt               ← Caption data
└── README.md                  ← Original readme
```

---

## 🎯 CTA (Call-to-Action) Messages

System automatically selects based on keyword:

| Keyword Match | CTA Message |
|---------------|-------------|
| tree, plant, environment | PLANT A TREE TODAY |
| health, fitness | START YOUR JOURNEY |
| business, money | FOLLOW FOR GROWTH |
| nature, eco | PROTECT NATURE |
| save, future | ACT NOW |
| *default* | FOLLOW FOR MORE |

---

## ⚙️ Advanced Configuration

### Batch Processing Strategy
```bash
# Generate 5 reels for content calendar
python main.py "Content idea" --batch 5

# Each reel gets:
# - Unique script (from template randomization)
# - Different images (auto-selected)
# - Same keyword (for consistency)
# - New timestamp (for organization)
```

### Music Management
Place MP3 files in `music/` folder:
```bash
music/
├── background1.mp3
├── upbeat.mp3
├── calm.mp3
└── trending.mp3
```
System will random select one for each reel.

### Image Library
Populate `images/` folder with your own:
```bash
images/
├── my_image1.jpg
├── my_image2.jpg
├── photo.png
└── ...
```
Used as fallback if API fetching fails.

---

## 🔍 Validation & Diagnostics

### Check System Status
```bash
python main.py --validate
```
Verifies:
- Python version
- All dependencies installed
- MoviePy compatibility
- Directory structure
- File permissions

### Debug Mode
```bash
python main.py "Keyword" --verbose
```
Shows detailed logging for troubleshooting

---

## 🚨 Troubleshooting

| Problem | Solution |
|---------|----------|
| No images fetching | Check internet; images/ fallback will be used |
| MoviePy errors | `pip install moviepy --upgrade` |
| Voice not generating | Install pyttsx3: `pip install pyttsx3` |
| Text overlay missing | Optional feature; skipped if ImageMagick unavailable |
| Slow generation | Normal for first run; images are cached after |
| API rate limits | System automatically retries; uses fallbacks |

---

## 📊 Performance Metrics

Typical generation times:
- **Script generation:** 0.1s
- **Image fetching:** 5-30s (first run, then cached)
- **Voice generation:** 5-10s
- **Video creation:** 10-30s
- **Total:** 20-70s per reel

Batch efficiency:
- **Single reel:** ~45s
- **5 reels:** ~3-4 minutes (images cached)
- **10 reels:** ~6-8 minutes

---

## 💡 Tips & Best Practices

1. **Content Quality:** More specific keywords generate better scripts
   - ❌ "nature"
   - ✅ "sustainable farming practices"

2. **Batch Generation:** Create weekly content batches
   ```bash
   python main.py "Weekly topic" --batch 7
   ```

3. **Style Mixing:** Test all styles to see what works
   ```bash
   for style in motivational educational entertaining trending; do
     python main.py "Topic" --style $style
   done
   ```

4. **Music Addition:** Always add background music to music/ folder for better output

5. **Local Images:** For consistent branding, populate images/ with your own images

---

## 🔄 Workflow at a Glance

```
User Input (Keyword + Style)
        ↓
    [Script Generator]
        ↓
    [Image Fetcher] (Multi-source with fallback)
        ↓
    [Voice Generator]
        ↓
    [Music Selector]
        ↓
    [Video Engine]
        ├─ Ken Burns effects
        ├─ Transitions
        ├─ Text overlays
        ├─ Audio mixing
        └─ CTA addition
        ↓
    [Output] MP4 file
        ↓
    Ready for upload to:
    - YouTube Shorts
    - Instagram Reels
    - TikTok
    - Facebook
    - Any 9:16 platform
```

---

## 📈 Scaling & Automation

### Daily Automation (Cron/Task Scheduler)
```bash
# Daily reel generation at 8 AM
# Windows Task Scheduler / crontab:
0 8 * * * cd /path/to/ai-reel-automation && python main.py "Daily topic" --batch 3
```

### Weekly Content Creation
```bash
# Generate 21 reels every Sunday
python main.py "Weekly series" --batch 21
```

---

## 🎬 Platform-Specific Notes

### YouTube Shorts
- Format: Perfect (1080×1920, 60fps max)
- Duration: 15-60 seconds (our videos are 6-10s)
- Upload: Direct MP4, auto-optimized

### Instagram Reels
- Format: Perfect match
- Duration: 3-90 seconds
- Upload: Direct MP4 or use IGTV

### TikTok
- Format: Excellent
- Duration: 3-10 minutes (ours are 6-10s)
- Upload: Direct MP4, auto-optimized

### Facebook/Meta
- Format: Optimized
- Duration: Recommended under 60s
- Upload: Direct MP4

---

## 📞 Support & Debugging

### Check Logs
```bash
tail -f reel_generator.log
```

### Enable Verbose Mode
```bash
python main.py "Topic" --verbose
```

### Force Rebuild
```bash
rm -rf audio/ images/ output/  # Clear caches
python main.py "Topic"  # Regenerate everything
```

---

## 🏆 Use Cases

1. **Content Creators:** Generate weekly content library
2. **Marketing:** Create product/service promotion videos
3. **Education:** Generate tutorial/learning content
4. **Entertainment:** Viral facts and interesting content
5. **Business:** LinkedIn/social media marketing
6. **Community:** Environmental/social awareness campaigns
7. **Personal Brand:** Growing social media presence

---

## 📝 Version Info

- **Version:** 2.0 (Automated Generator)
- **Python:** 3.14+
- **Release:** March 31, 2026
- **Status:** Production Ready ✅

---

## 🎓 Next Steps

1. Run: `python main.py --validate`
2. Test: `python main.py "Your first keyword"`
3. Explore: Try different `--style` options
4. Batch: Generate multiple with `--batch 5`
5. Upload: Videos in `output/` are ready!

---

**Happy creating! 🎬✨**
