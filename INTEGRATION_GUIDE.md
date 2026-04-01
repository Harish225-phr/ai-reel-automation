# AI Reel Generator - Full Stack Integration Guide

## Overview

Your AI Reel Generator is now fully integrated with a professional React frontend! 

- **Backend**: Flask API server running on `http://localhost:5000`
- **Frontend**: React UI running on `http://localhost:8080`

---

## Quick Start (Windows)

### Option 1: One-Click Start (Easiest)

1. **Double-click** `START_FULL_SYSTEM.bat`
2. Wait for both servers to start
3. Open browser to `http://localhost:8080`
4. Done! ✅

### Option 2: Manual Start

#### Terminal 1 - Backend API Server:
```powershell
# Activate venv
.\.venv\Scripts\Activate.ps1

# Install Flask dependencies (first time only)
pip install flask==2.3.3 flask-cors==4.0.0 python-dotenv==1.0.0

# Start API server
python api_server.py
# Output: "Listening on http://localhost:5000"
```

#### Terminal 2 - React Frontend:
```powershell
cd Frontend\reel-genius
npm run dev
# Output: "http://localhost:8080"
```

3. Open browser to `http://localhost:8080`

---

## Quick Start (Mac/Linux)

```bash
chmod +x start_full_system.sh
./start_full_system.sh
```

---

## Environment Setup

### 1. Install Dependencies (First Time Only)

```powershell
# Windows
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd Frontend\reel-genius
npm install
cd ../..
```

### 2. Set API Keys

Create a `.env` file in project root:

```env
PIXABAY_API_KEY=your_pixabay_key_here
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
```

Or set in PowerShell before running:
```powershell
$env:PIXABAY_API_KEY='your_key'
$env:HUGGINGFACEHUB_API_TOKEN='your_token'
```

---

## File Structure

```
ai-reel-automation/
├── api_server.py              # ← Flask API (NEW)
├── main.py                    # Existing orchestrator
├── voice.py, video.py, etc    # Existing engines
├── requirements.txt           # Updated with Flask deps
│
├── Frontend/reel-genius/
│   ├── src/
│   │   ├── hooks/
│   │   │   └── useReelGenerator.ts  # ← Updated with real API calls
│   │   ├── components/
│   │   │   └── reel/
│   │   │       ├── PromptInput.tsx
│   │   │       ├── ProgressTracker.tsx
│   │   │       └── ResultView.tsx
│   │   ├── pages/
│   │   │   └── Index.tsx
│   │   └── types/
│   │       └── reel.ts
│   │
│   ├── .env.local            # ← Frontend environment
│   ├── package.json
│   └── vite.config.ts
│
├── START_FULL_SYSTEM.bat     # ← Windows start script (NEW)
└── start_full_system.sh      # ← Mac/Linux start script (NEW)
```

---

## API Endpoints

### POST `/api/generate-reel`

Generate a new reel from a prompt.

**Request:**
```json
{
  "prompt": "Create a motivational reel about fitness",
  "language": "en"  // or "hi" for Hindi
}
```

**Response:** Server-Sent Events stream with real-time progress:
```json
{
  "request_id": "reel_20260401_150000",
  "step": "parse",
  "status": "active",
  "message": "Parsing your prompt..."
}
```

Steps generated: `parse` → `script` → `clips` → `voice` → `music` → `compose`

Final response:
```json
{
  "request_id": "reel_20260401_150000",
  "status": "success",
  "video_file": "reel_english_fitness_20260401_150000.mp4",
  "message": "Reel generated successfully!"
}
```

### GET `/api/download/<filename>`

Get metadata for a generated video.

**Response:**
```json
{
  "file": "/path/to/reel_english_fitness_20260401_150000.mp4",
  "size": 5242880,
  "url": "/api/stream/reel_english_fitness_20260401_150000.mp4"
}
```

### GET `/api/stream/<filename>`

Stream a video file for playback.

**Response:** Video file with `video/mp4` MIME type

### GET `/api/history`

List all generated videos.

**Response:**
```json
{
  "videos": [
    {
      "name": "reel_english_fitness_20260401_150000.mp4",
      "size": 5242880,
      "created": "2026-04-01T15:00:00"
    }
  ]
}
```

### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "service": "ai-reel-generator"
}
```

---

## How It Works

### 1. User Enters Prompt

User types a prompt in the React frontend:
- Example: "Create a motivational reel about fitness"
- Selects language: English or Hindi

### 2. Frontend Sends to Backend

The `useReelGenerator` hook sends POST request to `/api/generate-reel`:
```javascript
fetch('http://localhost:5000/api/generate-reel', {
  method: 'POST',
  body: JSON.stringify({
    prompt: "Create a motivational reel about fitness",
    language: "en"
  })
})
```

### 3. Backend Processes Request

`api_server.py` receives request and:
1. Starts a background thread running `main.py`
2. Captures output from main.py
3. Maps logs to generation steps
4. Sends Server-Sent Events with progress updates

### 4. Real-Time Progress Shown

Frontend receives SSE stream:
- ✓ Parsing your prompt...
- ✓ Generating script...
- ✓ Finding video clips...
- ✓ Creating voice-over...
- ✓ Adding background music...
- ✓ Composing final reel...

### 5. Video Ready to Download

When complete, user can:
- Preview video in browser
- Download MP4 file
- Generate another reel
- View generation history in sidebar

---

## Troubleshooting

### Frontend can't connect to API

**Problem**: "Failed to connect to http://localhost:5000"

**Solution**:
```powershell
# Make sure API server is running in another terminal
python api_server.py

# Check if port is in use
netstat -ano | findstr :5000

# If port 5000 is busy, kill it
lsof -ti:5000 | xargs kill -9  # Mac/Linux
taskkill /PID <pid> /F         # Windows
```

### API server can't find main.py

**Problem**: "No such file or directory: main.py"

**Solution**:
```powershell
# Make sure you're in the right directory
cd d:\Python\ai-reel-automation
python api_server.py
```

### React won't start

**Problem**: "npm: command not found"

**Solution**:
```powershell
# Install Node.js from https://nodejs.org/
# Then in Frontend/reel-genius:
npm install
npm run dev
```

### Video doesn't play in browser

**Problem**: Black screen or no playback

**Solution**:
- Ensure browser supports MP4 (H.264 codec)
- Check browser console for errors
- Verify video file exists in `output/` directory

### Generation stuck or very slow

**Problem**: Progress not updating, taking too long

**Solution**:
```powershell
# HuggingFace model is slow (14.5GB download)
# Check if model is being downloaded:
# Look for activity in "Transformers cache" folder

# For faster testing, disable HuggingFace in main.py:
# Set: HAS_HUGGINGFACE = False
# This uses template-based fallback (instant)

# Regenerate manually:
python main.py "Your prompt here"
```

---

## Advanced Configuration

### Change Frontend Port

Edit `Frontend/reel-genius/vite.config.ts`:
```typescript
server: {
  port: 3000,  // Change from 8080
}
```

### Change API Server Port

Edit `api_server.py`:
```python
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,  # Change from 5000
    )
```

Update `.env.local` to match:
```
VITE_API_URL=http://localhost:8000
```

### Enable Debug Logging

Edit `.env.local`:
```
VITE_DEBUG=true
```

And check browser console for detailed logs.

### Disable CORS (Not Recommended)

If deploying to different domain, update `api_server.py`:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

---

## Deployment

### Production Deployment

For production, you'll want:

1. **Backend**: Deploy Flask to Heroku, AWS, DigitalOcean, etc.
   - Use Gunicorn: `gunicorn -w 4 api_server:app`
   - Set environment variables for API keys

2. **Frontend**: Deploy to Vercel, Netlify, AWS S3, etc.
   - Build: `npm run build`
   - Set `VITE_API_URL` to production backend URL

3. **Video Storage**: Use cloud storage (AWS S3, Google Cloud Storage)
   - Update Output directory path in `api_server.py`

---

## Next Steps

1. ✅ Run `START_FULL_SYSTEM.bat`
2. ✅ Open `http://localhost:8080`
3. ✅ Enter a prompt and click "Generate Reel"
4. ✅ Watch real-time progress
5. ✅ Download your generated video!

---

## Support

If you have issues:

1. Check the troubleshooting section above
2. Check browser console (F12) for frontend errors
3. Check terminal output for backend errors
4. Verify API keys are set correctly
5. Verify ports 5000 and 8080 are available

Enjoy! 🎬✨
