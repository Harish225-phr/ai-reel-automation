"""
Instagram Integration API
Endpoints for uploading generated reels to Instagram
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from pathlib import Path
import os
from instagram_uploader import InstagramUploader, InstagramScheduler

# Create blueprint
instagram_bp = Blueprint('instagram', __name__, url_prefix='/api/instagram')


@instagram_bp.route('/config', methods=['POST'])
def configure_instagram():
    """
    Configure Instagram credentials
    
    Request JSON:
    {
        "business_account_id": "YOUR_BUSINESS_ACCOUNT_ID",
        "access_token": "YOUR_ACCESS_TOKEN"
    }
    """
    try:
        data = request.get_json()
        business_account_id = data.get('business_account_id')
        access_token = data.get('access_token')
        
        if not business_account_id or not access_token:
            return jsonify({'error': 'Missing credentials'}), 400
        
        # Store in environment or session
        os.environ['INSTAGRAM_BUSINESS_ACCOUNT_ID'] = business_account_id
        os.environ['INSTAGRAM_ACCESS_TOKEN'] = access_token
        
        # Verify credentials
        uploader = InstagramUploader(business_account_id, access_token)
        account_info = uploader.get_account_info()
        
        if 'error' in account_info:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        return jsonify({
            'status': 'configured',
            'account': account_info.get('username'),
            'followers': account_info.get('followers_count', 0)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@instagram_bp.route('/upload', methods=['POST'])
def upload_to_instagram():
    """
    Upload generated reel to Instagram
    
    Request JSON:
    {
        "video_id": "reel_id_from_generation",
        "caption": "Your reel caption",
        "hashtags": ["#reel", "#shorts"],
        "schedule_at": "2026-04-02T14:30:00" (optional, ISO format)
    }
    """
    try:
        data = request.get_json()
        video_id = data.get('video_id')
        caption = data.get('caption', '')
        hashtags = data.get('hashtags', [])
        schedule_at_str = data.get('schedule_at')
        
        # Get credentials
        business_account_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
        access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        
        if not business_account_id or not access_token:
            return jsonify({'error': 'Instagram not configured'}), 400
        
        # Find video file
        output_dir = Path(__file__).parent / "output"
        video_path = None
        
        for f in output_dir.glob(f"{video_id}*"):
            if f.suffix == '.mp4':
                video_path = f
                break
        
        if not video_path or not video_path.exists():
            return jsonify({'error': f'Video not found: {video_id}'}), 404
        
        # Parse schedule time if provided
        schedule_at = None
        if schedule_at_str:
            try:
                schedule_at = datetime.fromisoformat(schedule_at_str)
            except:
                return jsonify({'error': 'Invalid schedule time format'}), 400
        
        # Upload to Instagram
        uploader = InstagramUploader(business_account_id, access_token)
        
        result = uploader.upload_reel(
            video_path=str(video_path),
            caption=caption,
            hashtags=hashtags,
            schedule_at=schedule_at
        )
        
        if result['success']:
            return jsonify({
                'status': 'success',
                'reel_id': result.get('reel_id'),
                'url': result.get('url'),
                'publish_time': result.get('publish_time'),
                'message': f"Reel {'scheduled' if schedule_at else 'published'} successfully!"
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'error': result.get('error')
            }), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@instagram_bp.route('/schedule', methods=['POST'])
def schedule_uploads():
    """
    Schedule multiple reel uploads
    
    Request JSON:
    {
        "uploads": [
            {
                "video_id": "reel_id_1",
                "caption": "Caption 1",
                "schedule_at": "2026-04-02T14:00:00"
            },
            {
                "video_id": "reel_id_2",
                "caption": "Caption 2",
                "schedule_at": "2026-04-02T15:00:00"
            }
        ]
    }
    """
    try:
        data = request.get_json()
        uploads = data.get('uploads', [])
        
        if not uploads:
            return jsonify({'error': 'No uploads specified'}), 400
        
        # Get credentials
        business_account_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
        access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        
        if not business_account_id or not access_token:
            return jsonify({'error': 'Instagram not configured'}), 400
        
        # Schedule uploads
        uploader = InstagramUploader(business_account_id, access_token)
        scheduler = InstagramScheduler(uploader)
        output_dir = Path(__file__).parent / "output"
        
        for upload in uploads:
            video_id = upload.get('video_id')
            caption = upload.get('caption', '')
            schedule_at_str = upload.get('schedule_at')
            hashtags = upload.get('hashtags', [])
            
            # Find video
            video_path = None
            for f in output_dir.glob(f"{video_id}*"):
                if f.suffix == '.mp4':
                    video_path = f
                    break
            
            if not video_path or not video_path.exists():
                continue  # Skip missing videos
            
            schedule_at = datetime.fromisoformat(schedule_at_str)
            
            scheduler.add_to_schedule(
                video_path=str(video_path),
                caption=caption,
                publish_time=schedule_at,
                hashtags=hashtags
            )
        
        # Process schedule
        results = scheduler.process_schedule()
        
        successful = sum(1 for r in results if r.get('success'))
        
        return jsonify({
            'status': 'scheduled',
            'total': len(results),
            'successful': successful,
            'results': results
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@instagram_bp.route('/account', methods=['GET'])
def get_account():
    """Get Instagram account information"""
    try:
        business_account_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
        access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        
        if not business_account_id or not access_token:
            return jsonify({'error': 'Instagram not configured'}), 400
        
        uploader = InstagramUploader(business_account_id, access_token)
        account_info = uploader.get_account_info()
        
        if 'error' in account_info:
            return jsonify({'error': 'Failed to fetch account info'}), 500
        
        return jsonify(account_info), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@instagram_bp.route('/insights', methods=['GET'])
def get_insights():
    """Get account insights"""
    try:
        business_account_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
        access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        
        if not business_account_id or not access_token:
            return jsonify({'error': 'Instagram not configured'}), 400
        
        metric = request.args.get('metric', 'impressions')
        
        uploader = InstagramUploader(business_account_id, access_token)
        insights = uploader.get_insights(metric)
        
        if 'error' in insights:
            return jsonify({'error': 'Failed to fetch insights'}), 500
        
        return jsonify(insights), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@instagram_bp.route('/status', methods=['GET'])
def get_status():
    """Get Instagram integration status"""
    try:
        business_account_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
        access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        
        if not business_account_id or not access_token:
            return jsonify({'status': 'not_configured'}), 200
        
        uploader = InstagramUploader(business_account_id, access_token)
        account_info = uploader.get_account_info()
        
        if 'error' in account_info:
            return jsonify({'status': 'invalid_credentials'}), 200
        
        return jsonify({
            'status': 'configured',
            'username': account_info.get('username'),
            'followers': account_info.get('followers_count', 0)
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500
