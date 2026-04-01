"""
Flask API Server for AI Reel Generator
Provides /api/generate-reel endpoint with streaming progress updates
With SQLite database for history tracking
"""

from flask import Flask, request, jsonify, Response, send_from_directory, send_file
from flask_cors import CORS
import json
import subprocess
import os
import sys
from datetime import datetime
from pathlib import Path
import threading
import queue
import re
import time

# Import database module
from database import (
    init_database, create_video_record, update_video_status, 
    add_progress, get_video, get_all_videos, get_video_progress
)

app = Flask(
    __name__,
    static_folder=str(Path(__file__).parent / "Frontend/reel-genius/dist"),
    static_url_path=""
)
CORS(app)

# Initialize database on startup
init_database()

# Configuration
OUTPUT_DIR = Path(__file__).parent / "output"
VENV_PYTHON = Path(__file__).parent / ".venv" / "Scripts" / "python.exe"
FRONTEND_DIST = Path(__file__).parent / "Frontend/reel-genius/dist"

# Queue for streaming updates
progress_queue = queue.Queue()


def get_video_duration(filepath):
    """
    Get video duration in seconds using ffprobe or fallback to moviepy
    """
    try:
        # Try ffprobe first (fastest, most reliable)
        ffprobe_path = Path(__file__).parent / "ffmpeg" / "bin" / "ffprobe.exe"
        if ffprobe_path.exists():
            try:
                result = subprocess.run(
                    [str(ffprobe_path), '-v', 'quiet', '-print_format', 'json', '-show_format', str(filepath)],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.stdout.strip():
                    data = json.loads(result.stdout)
                    duration = float(data.get('format', {}).get('duration', '0'))
                    if duration > 0:  # Only return if valid
                        return duration
            except Exception as e:
                print(f"[API] ffprobe failed: {e}", flush=True)
        
        # Fallback to moviepy
        try:
            from moviepy.editor import VideoFileClip
            clip = VideoFileClip(str(filepath))
            duration = clip.duration
            clip.close()
            if duration > 0:
                return duration
        except Exception as e:
            print(f"[API] moviepy failed: {e}", flush=True)
        
        # Final fallback - estimate from file
        return 30.0  # Reasonable default
        
    except Exception as e:
        print(f"[API] Error getting duration: {e}", flush=True)
        return 30.0


def format_duration(seconds):
    """Format seconds to MM:SS"""
    try:
        seconds = float(seconds)
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"
    except:
        return "0:30"


def execute_reel_generation(prompt: str, language: str, request_id: str):
    """
    Execute main.py and stream progress updates
    """
    try:
        # Record request start time
        request_start_time = time.time()
        print(f"[API] Request started at: {request_start_time}", flush=True)
        
        # Create database record
        create_video_record(request_id, prompt, language)
        add_progress(request_id, 'parse', 'active', 'Parsing your prompt...')
        
        # Set environment variables
        env = os.environ.copy()
        env['PIXABAY_API_KEY'] = os.getenv('PIXABAY_API_KEY', '')
        env['HUGGINGFACEHUB_API_TOKEN'] = os.getenv('HUGGINGFACEHUB_API_TOKEN', '')
        env['PYTHONIOENCODING'] = 'utf-8'  # Force UTF-8 encoding

        # Run main_stable.py with prompt (STABILITY FIRST!)
        cmd = [
            str(VENV_PYTHON),
            str(Path(__file__).parent / "main_stable.py"),
            prompt
        ]

        # Start process with output capture
        # CRITICAL: Close stdin to prevent hung subprocess waiting for input
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL,  # Don't wait for stdin - this was causing 200s hang!
            text=True,
            encoding='utf-8',  # Ensure UTF-8 encoding
            env=env,
            cwd=str(Path(__file__).parent)
        )

        # Send initial status
        progress_queue.put({
            'request_id': request_id,
            'step': 'parse',
            'status': 'active',
            'message': 'Parsing your prompt...'
        })

        # Parse output and map to steps
        step_mapping = {
            '[PARSE]': 'parse',
            '[SCRIPT]': 'script',
            '[STEP 3]': 'clips',
            '[VOICE]': 'voice',
            '[MUSIC]': 'music',
            '[COMPOSE]': 'compose',
            '[SUCCESS]': 'complete',
        }

        current_step = 'parse'
        last_step = None
        video_file = None
        all_output = []

        # Read output line by line
        while True:
            line = process.stdout.readline()
            if not line:
                break

            line = line.strip()
            all_output.append(line)  # Keep all output for later
            print(f"[{request_id}] {line}", flush=True)

            # Check for step transitions
            for marker, step in step_mapping.items():
                if marker in line:
                    if step != last_step:
                        # Transition to next step
                        if last_step:
                            progress_queue.put({
                                'request_id': request_id,
                                'step': last_step,
                                'status': 'complete',
                                'message': f'✓ {step_mapping.get(last_step, "")} complete'
                            })

                        current_step = step
                        last_step = step

                        if step != 'complete':
                            progress_queue.put({
                                'request_id': request_id,
                                'step': step,
                                'status': 'active',
                                'message': line
                            })

                    break

            # Look for video file in output - multiple patterns
            if '[SUCCESS]' in line and '.mp4' in line:
                # Extract filename after "reel_" and before ".mp4"
                match = re.search(r'(reel_[^:\s]+\.mp4)', line)
                if match:
                    video_file = match.group(1)
                    print(f"[{request_id}] FOUND VIDEO FILE: {video_file}", flush=True)
        # Wait for process to complete
        returncode = process.wait()
        stderr = process.stderr.read()

        if returncode == 0:
            print(f"[API] Process completed with returncode 0", flush=True)
            print(f"[API] Looking for video file created after: {request_start_time}", flush=True)
            print(f"[API] Currently has video_file: {video_file}", flush=True)
            
            # Find latest video file created AFTER this request started
            if not video_file:
                print(f"[API] Video file not found in output, searching directory...", flush=True)
                try:
                    # Find videos modified AFTER request started
                    potential_videos = []
                    for vid in OUTPUT_DIR.glob('reel_*.mp4'):
                        mod_time = vid.stat().st_mtime
                        if mod_time > request_start_time:
                            potential_videos.append((mod_time, vid))
                    
                    if potential_videos:
                        # Sort by modification time, newest first
                        potential_videos.sort(reverse=True)
                        video_file = potential_videos[0][1].name
                        print(f"[API] ✓ Found video created in this request: {video_file}", flush=True)
                    else:
                        print(f"[API] No videos found created after request start", flush=True)
                        # Last resort: get the absolute newest
                        all_videos = sorted(
                            OUTPUT_DIR.glob('reel_*.mp4'),
                            key=lambda x: x.stat().st_mtime,
                            reverse=True
                        )
                        if all_videos:
                            video_file = all_videos[0].name
                            print(f"[API] Using latest video as fallback: {video_file}", flush=True)
                except Exception as e:
                    print(f"[API] Error searching for video: {e}", flush=True)
                    import traceback
                    traceback.print_exc()

            # ⚠️ CRITICAL: Wait for file to be fully written to disk
            if video_file:
                filepath = OUTPUT_DIR / video_file
                max_retries = 30  # Wait up to 30 seconds
                file_exists = False
                
                print(f"[API] Verifying file exists: {filepath}", flush=True)
                
                for attempt in range(max_retries):
                    if filepath.exists():
                        # File exists - check if it's still being written
                        try:
                            file_size = filepath.stat().st_size
                            if file_size > 50000:  # At least 50KB (not empty)
                                # Wait a bit more to ensure write is complete
                                time.sleep(0.5)
                                
                                # Verify size didn't change (write complete)
                                new_size = filepath.stat().st_size
                                if new_size == file_size:
                                    file_exists = True
                                    print(f"[API] ✓ Video file ready: {video_file} ({file_size} bytes)", flush=True)
                                    break
                            else:
                                print(f"[API] File too small ({file_size} bytes), waiting...", flush=True)
                        except Exception as e:
                            print(f"[API] Error checking file: {e}", flush=True)
                    else:
                        if attempt == 0:
                            print(f"[API] File not found yet, retrying...", flush=True)
                    
                    if attempt < max_retries - 1:
                        time.sleep(0.5)
                
                if not file_exists:
                    print(f"[API] ✗ File verification failed", flush=True)
                    video_file = None

            progress_queue.put({
                'request_id': request_id,
                'step': 'compose',
                'status': 'complete',
                'message': 'Composing final reel...'
            })

            # Extract video metadata
            video_duration = '0:30'
            video_size = '0 MB'
            
            print(f"[API] VIDEO_FILE for metadata: {video_file}", flush=True)
            
            if video_file:
                try:
                    filepath = OUTPUT_DIR / video_file
                    print(f"[API] Checking: {filepath}", flush=True)
                    print(f"[API] Exists: {filepath.exists()}", flush=True)
                    
                    if filepath.exists():
                        # Get file size
                        file_size_bytes = filepath.stat().st_size
                        video_size = f"{file_size_bytes / (1024 * 1024):.1f} MB"
                        print(f"[API] ✓ File size: {video_size}", flush=True)
                        
                        # Get video duration
                        duration_sec = get_video_duration(str(filepath))
                        video_duration = format_duration(duration_sec)
                        print(f"[API] ✓ Duration: {video_duration}", flush=True)
                    else:
                        print(f"[API] ✗ File does not exist!", flush=True)
                except Exception as e:
                    print(f"[API] ✗ ERROR extracting metadata: {e}", flush=True)
                    import traceback
                    traceback.print_exc()
            else:
                print(f"[API] ✗ No video_file, using defaults", flush=True)

            print(f"[API] SUCCESS RESPONSE:", flush=True)
            print(f"[API]   video_file: {video_file}", flush=True)
            print(f"[API]   duration: {video_duration}", flush=True)
            print(f"[API]   size: {video_size}", flush=True)
            
            progress_queue.put({
                'request_id': request_id,
                'status': 'success',
                'video_file': video_file,
                'duration': video_duration,
                'size': video_size,
                'message': 'Reel generated successfully!'
            })
            
            # Update database with success
            update_video_status(request_id, 'complete', video_file, video_duration, video_size)
            
            print(f"[API] ✓ SUCCESS message queued", flush=True)
        else:
            error_msg = stderr if stderr else f"Process exited with code {returncode}"
            progress_queue.put({
                'request_id': request_id,
                'status': 'error',
                'message': f'Error: {error_msg}'
            })
            
            # Update database with error
            update_video_status(request_id, 'error', error_message=error_msg)

    except Exception as e:
        progress_queue.put({
            'request_id': request_id,
            'status': 'error',
            'message': f'Exception: {str(e)}'
        })
        
        # Update database with exception
        update_video_status(request_id, 'error', error_message=str(e))


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    print("[API] Health check received!", flush=True)
    return jsonify({'status': 'ok', 'service': 'ai-reel-generator'}), 200


@app.route('/', methods=['GET'])
def serve_root():
    """Serve React frontend at root"""
    dist_path = FRONTEND_DIST / 'index.html'
    if dist_path.exists():
        return send_file(str(dist_path))
    return jsonify({'error': 'Frontend not found. Check if build exists at Frontend/reel-genius/dist'}), 404


@app.route('/<path:path>', methods=['GET'])
def serve_static(path):
    """Serve static files from dist folder, fallback to index.html for SPA routing"""
    # Don't intercept API routes
    if path.startswith('api/'):
        return jsonify({'error': f'API endpoint not found: /{path}'}), 404
    
    dist_path = FRONTEND_DIST / path
    
    # Check if file exists in dist
    if dist_path.exists() and dist_path.is_file():
        return send_file(str(dist_path))
    
    # For SPA routing - serve index.html for any unknown routes
    index_path = FRONTEND_DIST / 'index.html'
    if index_path.exists():
        return send_file(str(index_path))
    
    return jsonify({'error': f'Not found: {path}'}), 404


@app.route('/api/generate-reel', methods=['POST'])
def generate_reel():
    """
    Generate a reel from a prompt
    
    Request JSON:
    {
        "prompt": "your prompt here",
        "language": "en" or "hi"
    }
    
    Returns: EventStream with progress updates
    """
    try:
        print(f"\n{'='*60}", flush=True)
        print(f"[API] Received request from frontend!", flush=True)
        print(f"[API] URL: {request.url}", flush=True)
        print(f"[API] Method: {request.method}", flush=True)
        print(f"[API] Headers: {dict(request.headers)}", flush=True)
        
        data = request.get_json()
        print(f"[API] Request body: {data}", flush=True)
        
        prompt = data.get('prompt', '').strip()
        language = data.get('language', 'en')
        
        print(f"[API] Prompt: {prompt}", flush=True)
        print(f"[API] Language: {language}", flush=True)
        print(f"{'='*60}\n", flush=True)

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        # Generate request ID
        request_id = f"reel_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Start generation in background thread
        thread = threading.Thread(
            target=execute_reel_generation,
            args=(prompt, language, request_id),
            daemon=True
        )
        thread.start()

        # Return Server-Sent Events stream
        def event_stream():
            sent_complete = False
            while not sent_complete:
                try:
                    # Get message from queue with timeout
                    message = progress_queue.get(timeout=60)

                    # Only send messages for this request
                    if message.get('request_id') == request_id:
                        # Send as SSE
                        yield f"data: {json.dumps(message)}\n\n"

                        # Check if generation is complete
                        if message.get('status') in ['success', 'error']:
                            sent_complete = True

                except queue.Empty:
                    # Send keep-alive
                    yield f": keep-alive\n\n"

        response = Response(event_stream(), mimetype='text/event-stream')
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['X-Accel-Buffering'] = 'no'
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<filename>', methods=['GET'])
def download_video(filename: str):
    """
    Download a generated video file
    """
    try:
        # Security: only allow reel_*.mp4 files
        if not filename.startswith('reel_') or not filename.endswith('.mp4'):
            return jsonify({'error': 'Invalid filename'}), 400

        filepath = OUTPUT_DIR / filename

        if not filepath.exists():
            return jsonify({'error': 'File not found'}), 404

        # Return file with proper headers
        return {
            'file': str(filepath),
            'size': filepath.stat().st_size,
            'url': f'/api/stream/{filename}'
        }

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stream/<filename>', methods=['GET'])
def stream_video(filename: str):
    """
    Stream a video file
    """
    try:
        if not filename.startswith('reel_') or not filename.endswith('.mp4'):
            return jsonify({'error': 'Invalid filename'}), 400

        filepath = OUTPUT_DIR / filename

        if not filepath.exists():
            return jsonify({'error': 'File not found'}), 404

        def generate():
            with open(filepath, 'rb') as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    yield chunk

        return Response(generate(), mimetype='video/mp4')

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history', methods=['GET'])
def list_videos():
    """
    List all generated videos
    """
    try:
        videos = []
        if OUTPUT_DIR.exists():
            for video_file in sorted(
                OUTPUT_DIR.glob('reel_*.mp4'),
                key=os.path.getctime,
                reverse=True
            )[:20]:  # Last 20 videos
                stat = video_file.stat()
                videos.append({
                    'name': video_file.name,
                    'size': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                })

        return jsonify({'videos': videos}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/videos', methods=['GET'])
def get_videos():
    """
    Get all generated videos from the database
    """
    try:
        from database import get_all_videos
        videos = get_all_videos()
        return jsonify({'videos': videos}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/videos/<video_id>', methods=['GET'])
def get_video(video_id: str):
    """
    Get a specific video from the database
    """
    try:
        from database import get_video as db_get_video
        video = db_get_video(video_id)
        if not video:
            return jsonify({'error': 'Video not found'}), 404
        return jsonify({'video': video}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/videos/<video_id>/progress', methods=['GET'])
def get_video_progress(video_id: str):
    """
    Get generation progress for a video
    """
    try:
        from database import get_video_progress
        progress = get_video_progress(video_id)
        return jsonify({'progress': progress}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)

    print(f"Starting AI Reel Generator API Server", flush=True)
    print(f"Output directory: {OUTPUT_DIR}", flush=True)
    print(f"Python executable: {VENV_PYTHON}", flush=True)
    print(f"Listening on http://localhost:5000", flush=True)

    # Development server - use 0.0.0.0 to accept external connections
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,
        threaded=True
    )
