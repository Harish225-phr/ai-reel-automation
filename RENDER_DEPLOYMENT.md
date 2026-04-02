# AI Reel Automation - Stable Production Ready

**Status**: ✅ Unified Repo - Backend + Frontend Combined  
**Architecture**: Python (BackEnd) + React/Vite (Frontend)  
**Ready for**: Render, Railway, Heroku deployment  

## 📁 Project Structure

```
ai-reel-automation/
├── Backend (Root Level)
│   ├── main_stable.py              # Entry point - stable reel generator
│   ├── api_server.py               # Flask API (port 5000)
│   ├── config.py                   # Configuration
│   ├── database.py                 # SQLite database
│   ├── requirements.txt            # Python dependencies
│   │
│   ├── engine/                     # Core modules
│   │   ├── script_engine.py
│   │   ├── video_engine_pro.py
│   │   ├── caption_engine.py
│   │   ├── image_engine.py
│   │   └── text_renderer.py
│   │
│   ├── Voice/Music/Video Engines
│   │   ├── script_engine_stable.py       # STABLE: Fixed templates
│   │   ├── video_engine_stable.py        # STABLE: Validation + fallbacks
│   │   ├── voice_engine_stable.py        # STABLE: Edge TTS + retries
│   │   ├── voice_engine.py
│   │   ├── music_engine.py
│   │   └── video_fetcher.py              # Pexels integration + caching
│   │
│   ├── assets/
│   │   ├── fonts/
│   │   └── music/
│   │       ├── music_motivational_270686.wav  # Default fallback
│   │       └── music_calm_482679.wav
│   │
│   ├── output/                     # Generated reels
│   └── ffmpeg/                     # Bundled FFmpeg
│
├── Frontend (React + Vite)
│   └── Frontend/reel-genius/       # React app
│       ├── src/
│       ├── public/
│       ├── package.json
│       ├── vite.config.js
│       └── .env.example            # API endpoint config
│
├── .gitignore                      # Excludes node_modules, venv, etc
├── Procfile                        # Render deployment process file
└── render.yaml                     # Render service configuration

---

## 🚀 Quick Deployment to Render

### Backend Deployment

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

2. **Create Backend Service on Render**:
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `ai-reel-automation` repo

3. **Configure Service**:
   - **Name**: `ai-reel-backend`
   - **Environment**: Python 3.11
   - **Build Command**: (automatic, uses Procfile)
   - **Start Command**: (automatic, uses Procfile)

4. **Add Environment Variables**:
   ```
   PIXABAY_API_KEY = 41652470-89fa37c975e9cffbf88627b9a
   PEXELS_API_KEY = WpFsET9nVh30a0g2qOErgaePd7GuA7D8HKfOUFcaeLTJr6C6xHGT7nFv
   HUGGINGFACEHUB_API_TOKEN = (your token)
   ```

5. **Deploy**: Click "Create Web Service"
   - Build will take 5-10 minutes
   - You'll get a URL: `https://ai-reel-backend.onrender.com`

### Frontend Configuration

1. **Update `.env.production`** in `Frontend/reel-genius/`:
   ```env
   VITE_API_URL=https://ai-reel-backend.onrender.com
   ```

2. **Commit and push**:
   ```bash
   git add Frontend/reel-genius/.env.production
   git commit -m "Update backend API URL for production"
   git push
   ```

3. **Frontend will auto-rebuild** on Render (if connected)
├── requirements.txt                # Backend Python deps
└── README.md                       # This file
```

## 🚀 Quick Start

### Local Development

**Backend:**
```bash
pip install -r requirements.txt
python main_stable.py "fitness motivation"
```

**Frontend:**
```bash
cd Frontend/reel-genius
npm install
npm run dev
```

**API Server:**
```bash
python api_server.py
# Runs on http://localhost:5000
```

**Frontend Dev Server:**
```bash
npm run dev
# Runs on http://localhost:5173 (or 8080)
```

## 📋 Requirements

### Backend Dependencies
```
Flask==3.0.0
flask-cors==4.0.0
MoviePy==1.0.3
edge-tts==6.1.12
requests==2.31.0
Pillow==10.1.0
pydub==0.25.1
```

### Frontend Dependencies
- Node.js 18+
- npm 9+

## 🌐 Deployment Options

### Option 1: Render with Separate Services

**Backend Service:**
- Build Command: `pip install -r requirements.txt`
- Start Command: `python api_server.py`
- Port: 5000
- Region: Singapore/Asia
- Environment Variables:
  ```
  PEXELS_API_KEY=<your_key>
  PIXABAY_API_KEY=<your_key>
  FREESOUND_API_KEY=<your_key>
  FLASK_ENV=production
  ```

**Frontend Service:**
- Build Command: `cd Frontend/reel-genius && npm install && npm run build`
- Start Command: `npm run preview` (from Frontend/reel-genius)  
- Port: 3000
- Environment Variables:
  ```
  VITE_API_URL=https://your-backend-service.onrender.com
  ```

### Option 2: Single Render Service (Full Stack)

```bash
# render.yaml
services:
  - type: web
    name: ai-reel-automation
    env: python
    buildCommand: |
      pip install -r requirements.txt
      cd Frontend/reel-genius && npm install && npm run build
    startCommand: |
      python api_server.py &
      cd Frontend/reel-genius && npm run preview
    port: 5000
```

### Option 3: Railway.app

Similar to Render - push to GitHub, connect Railway, configure environment variables.

## 🔑 API Endpoints

### Generate Reel
```bash
POST /api/generate-reel
{
  "prompt": "fitness motivation",
  "language": "en"
}

Response:
{
  "video_id": "reel_20260401_223153",
  "status": "generating",
  "output_path": "output/reel_stable_english_fitness_20260401_223153.mp4"
}
```

### Video History
```bash
GET /api/videos
# Returns all generated reels

GET /api/videos/{id}
# Returns specific reel info

GET /api/videos/{id}/progress
# Returns generation progress
```

### Stream Reel
```bash
GET /api/stream/{filename}
# Download reel MP4
```

## 🎨 Frontend Configuration

In `Frontend/reel-genius/.env`:
```
VITE_API_URL=http://localhost:5000  # Local
# or
VITE_API_URL=https://your-backend.onrender.com  # Production
```

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Video Quality
VIDEO_FPS = 20              # Faster (18) or slower (24)
VIDEO_WIDTH = 1080          # Instagram Reel standard
VIDEO_HEIGHT = 1920

# Performance
PEXELS_VIDEO_COUNT = 4      # Videos per reel
ENCODING_PRESET = 'superfast'  # ultrafast/superfast/faster

# Features
ENABLE_ZOOM = False         # Disable for stability
ENABLE_CROSSFADE = False    # Disable for stability
ENABLE_HOOK_TEXT = False    # Disable for stability
ENABLE_CTA_OVERLAY = False  # Disable for stability
```

## 📊 Performance

- **First Generation**: 85-90 seconds (includes video download)
- **Cached Generation**: 60-70 seconds (cached videos)
- **Components**:
  - Parse + Script: 1-2 sec
  - Video download: 20-30 sec
  - Voice generation: 5-10 sec
  - Music: 1-2 sec
  - Compositing: 5-10 sec
  - MP4 encoding: 40-50 sec

## 🐛 Troubleshooting

### Edge TTS fails
```
[ERROR] No audio received
[DEBUG] Retrying with alternative voice...
```
**Fix**: Automatic retry (3 attempts), uses fallback voices

### Insufficient video clips
```
[ERROR] Only 2 clips found, minimum 3 required
```
**Fix**: Check Pexels API key validity, clips will never use black screen fallback

### Music missing
```
[WARNING] Music file not found
[DEBUG] Using default fallback
```
**Fix**: Uses default music (assets/music/music_motivational_270686.wav)

## 🎯 Stability Features

1. **Fixed Scripts** - No AI model dependency
2. **Minimum Validation** - Stops if < 3 clips
3. **Default Fallbacks** - Music always available
4. **Retry Logic** - Voice/API auto-retries
5. **Comprehensive Logging** - Debug every step
6. **No Black Screens** - Enforced validation

## 📝 Database

SQLite database (`reel_generator.db`) stores:
- Video generation history
- Progress tracking
- Generation metadata

Created automatically on first run.

## 🚀 GitHub Push

```bash
# All files already staged and committed locally
git push -u origin main
# Follow GitHub's SSH key setup if needed
```

## 📱 Frontend Features

✅ Video history list  
✅ Generation progress tracking  
✅ Reel preview/streaming  
✅ Download generated reels  
✅ API integration ready  

## 🔐 Environment Variables Required

```
PEXELS_API_KEY=<your_key>        # Stock video API
PIXABAY_API_KEY=<your_key>       # Fallback video
FREESOUND_API_KEY=<your_key>     # Audio generation
FLASK_ENV=production             # For Render
```

## 📞 Support

For issues:
1. Check debug output (all steps logged)
2. Review error messages in console
3. Check .gitignore for what's tracked
4. Verify all environment variables set

---

**Status**: Production Ready ✅  
**Last Updated**: April 1, 2026  
**Unified Repo**: Backend + Frontend in one repository
