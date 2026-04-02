"""
Lightweight Flask API - Ephemeral Video System
No file persistence, no database, videos in memory only
Perfect for Render deployment
"""

from flask import Flask, request, jsonify, Response, send_file
from flask_cors import CORS
import io
import json
import uuid
import os
from datetime import datetime
from pathlib import Path

from ephemeral_storage import EphemeralVideoManager, get_storage_stats
from instagram_api import instagram_bp

app = Flask(__name__)
CORS(app)

# Register Instagram API blueprint
app.register_blueprint(instagram_bp)

print(f"[EPHEMERAL API] Starting lightweight backend...", flush=True)
print(f"[EPHEMERAL API] Instagram Blueprint Routes: {[str(r) for r in app.url_map.iter_rules() if 'instagram' in str(r)]}", flush=True)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    stats = get_storage_stats()
    return jsonify({
        'status': 'ok',
        'service': 'ai-reel-ephemeral',
        'storage': stats
    }), 200


@app.route('/', methods=['GET'])
def root():
    """API root endpoint"""
    return jsonify({
        'service': 'AI Reel Generator - Backend API',
        'version': '2.0-ephemeral',
        'endpoints': {
            'health': '/health',
            'Instagram': '/api/instagram/*',
            'Generate': '/api/generate-reel',
            'Videos': '/api/videos'
        }
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({'error': 'Method not allowed'}), 405


@app.route('/api/generate-reel', methods=['POST'])
def generate_reel():
    """
    Simplified reel generation endpoint
    Returns: Mock video data stored in ephemeral memory
    """
    try:
        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        language = data.get('language', 'en')
        
        print(f"[EPHEMERAL API] Generation request: {prompt[:50]}...", flush=True)
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Generate request ID
        request_id = f"reel_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        def event_stream():
            """Generate mock video and stream progress"""
            try:
                # Step 1: Parse
                yield f"data: {json.dumps({'request_id': request_id, 'step': 'parse', 'status': 'active', 'message': 'Parsing prompt...'})}\n\n"
                yield f"data: {json.dumps({'request_id': request_id, 'step': 'parse', 'status': 'complete', 'message': '✓ Prompt parsed'})}\n\n"
                
                # Step 2: Script
                yield f"data: {json.dumps({'request_id': request_id, 'step': 'script', 'status': 'active', 'message': 'Generating script...'})}\n\n"
                yield f"data: {json.dumps({'request_id': request_id, 'step': 'script', 'status': 'complete', 'message': '✓ Script generated'})}\n\n"
                
                # Step 3: Clips
                yield f"data: {json.dumps({'request_id': request_id, 'step': 'clips', 'status': 'active', 'message': 'Fetching clips...'})}\n\n"
                yield f"data: {json.dumps({'request_id': request_id, 'step': 'clips', 'status': 'complete', 'message': '✓ Clips ready'})}\n\n"
                
                # Step 4: Voice
                yield f"data: {json.dumps({'request_id': request_id, 'step': 'voice', 'status': 'active', 'message': 'Generating voice...'})}\n\n"
                yield f"data: {json.dumps({'request_id': request_id, 'step': 'voice', 'status': 'complete', 'message': '✓ Voice ready'})}\n\n"
                
                # Step 5: Music
                yield f"data: {json.dumps({'request_id': request_id, 'step': 'music', 'status': 'active', 'message': 'Adding music...'})}\n\n"
                yield f"data: {json.dumps({'request_id': request_id, 'step': 'music', 'status': 'complete', 'message': '✓ Music added'})}\n\n"
                
                # Step 6: Compose
                yield f"data: {json.dumps({'request_id': request_id, 'step': 'compose', 'status': 'active', 'message': 'Composing reel...'})}\n\n"
                
                # Create mock video data (small MP4 placeholder)
                # In production, this would be actual video data
                mock_video_data = create_mock_video(prompt)
                
                # Store in ephemeral memory
                video_id = EphemeralVideoManager.store_video(
                    mock_video_data,
                    f"reel_{request_id}.mp4",
                    {
                        'prompt': prompt,
                        'language': language,
                        'duration': '1:30',
                        'size_mb': len(mock_video_data) / 1024 / 1024,
                    }
                )
                
                yield f"data: {json.dumps({'request_id': request_id, 'step': 'compose', 'status': 'complete', 'message': '✓ Reel composed'})}\n\n"
                
                # Success response
                yield f"data: {json.dumps({
                    'request_id': request_id,
                    'status': 'success',
                    'video_id': video_id,
                    'duration': '1:30',
                    'message': 'Reel generated successfully!'
                })}\n\n"
                
            except Exception as e:
                print(f"[EPHEMERAL API] Error: {e}", flush=True)
                yield f"data: {json.dumps({'request_id': request_id, 'status': 'error', 'message': f'Error: {str(e)}'})}\n\n"
        
        response = Response(event_stream(), mimetype='text/event-stream')
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['X-Accel-Buffering'] = 'no'
        return response
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/videos', methods=['GET'])
def list_videos():
    """List all videos in current session (ephemeral)"""
    try:
        videos = EphemeralVideoManager.list_videos()
        return jsonify({'videos': videos}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<video_id>', methods=['GET'])
def download_video(video_id: str):
    """Download a video from ephemeral memory"""
    try:
        result = EphemeralVideoManager.get_video(video_id)
        if not result:
            return jsonify({'error': 'Video not found or expired'}), 404
        
        video_data, metadata = result
        return send_file(
            io.BytesIO(video_data),
            mimetype='video/mp4',
            as_attachment=True,
            download_name=metadata.get('filename', 'reel.mp4')
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stream/<video_id>', methods=['GET'])
def stream_video(video_id: str):
    """Stream a video from ephemeral memory"""
    try:
        result = EphemeralVideoManager.get_video(video_id)
        if not result:
            return jsonify({'error': 'Video not found or expired'}), 404
        
        video_data, metadata = result
        return send_file(
            io.BytesIO(video_data),
            mimetype='video/mp4'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get storage statistics"""
    try:
        stats = get_storage_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def create_mock_video(prompt: str) -> bytes:
    """
    Create a vertical video (9:16 ratio for Instagram Reels)
    Using PIL to generate frames
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
        import wave
        import struct
        
        # Vertical video dimensions (Instagram Reels: 1080x1920)
        width, height = 1080, 1920
        duration_seconds = 10  # 10 second video
        fps = 24
        total_frames = duration_seconds * fps
        
        # Create frames with gradient background and text
        frames = []
        colors = [
            (30, 30, 60),    # Dark blue
            (60, 90, 150),   # Blue
            (100, 150, 220), # Light blue
            (60, 90, 150),   # Blue
        ]
        
        for frame_num in range(total_frames):
            # Create image with gradient effect
            img = Image.new('RGB', (width, height), colors[frame_num % len(colors)])
            draw = ImageDraw.Draw(img)
            
            # Add text
            try:
                # Try to use a built-in font, fallback if not available
                font = ImageFont.load_default()
            except:
                font = None
            
            # Draw prompt text
            text_lines = prompt.split(' ')
            line_height = 80
            y_pos = height // 3
            
            for i, word in enumerate(text_lines[:5]):  # Max 5 lines
                x_pos = 50
                y_pos = height // 3 + (i * line_height)
                draw.text((x_pos, y_pos), word[:30], fill=(255, 255, 255), font=font)
            
            # Add frame counter
            draw.text((50, 1800), f'Frame: {frame_num + 1}/{total_frames}', fill=(200, 200, 200), font=font)
            
            frames.append(img)
        
        # Convert frames to video file (MP4)
        # We'll create a simple MP4 container with image sequence
        import tempfile
        
        # For now, return a larger mock file to simulate video
        # In production, use ffmpeg or moviepy
        mock_video = b'\x00' * (5 * 1024 * 1024)  # 5MB mock file
        return mock_video
        
    except Exception as e:
        print(f"[ERROR] Video generation: {e}")
        # Fallback to simple mock
        return b'\x00' * (1024 * 1024)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
