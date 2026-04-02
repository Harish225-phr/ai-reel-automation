"""
Instagram Auto-Upload Module
Automated reel uploading to Instagram Business Account
Uses Instagram Graph API (official, reliable, no bans)
"""

import requests
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import logging
from typing import Optional, Dict, Any
import mimetypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InstagramUploader:
    """
    Upload reels to Instagram Business Account using Graph API
    Supports scheduling and metadata management
    """
    
    # Instagram Graph API endpoints
    GRAPH_API_VERSION = "v19.0"
    INSTAGRAM_BUSINESS_API = f"https://graph.instagram.com/{GRAPH_API_VERSION}"
    
    def __init__(self, business_account_id: str, access_token: str):
        """
        Initialize Instagram uploader
        
        Args:
            business_account_id: Instagram Business Account ID (from Meta Business Manager)
            access_token: Long-lived access token from Meta App
        """
        self.business_account_id = business_account_id
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        })
        
        logger.info(f"[INSTAGRAM] Uploader initialized for account: {business_account_id}")
    
    def upload_reel(
        self,
        video_path: str,
        caption: str,
        cover_image_path: Optional[str] = None,
        schedule_at: Optional[datetime] = None,
        hashtags: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Upload reel to Instagram
        
        Args:
            video_path: Path to MP4 video file
            caption: Reel caption/description
            cover_image_path: Optional custom cover image
            schedule_at: Schedule publication (datetime object)
            hashtags: List of hashtags to add to caption
            
        Returns:
            dict: Response with reel ID and status
        """
        try:
            # Validate video file
            if not Path(video_path).exists():
                raise FileNotFoundError(f"Video not found: {video_path}")
            
            file_size = Path(video_path).stat().st_size
            logger.info(f"[INSTAGRAM] Video size: {file_size / 1024 / 1024:.1f} MB")
            
            # Add hashtags to caption
            if hashtags:
                caption = f"{caption}\n\n{' '.join(hashtags)}"
            
            # Step 1: Create container (upload video)
            logger.info("[INSTAGRAM] Step 1: Creating media container...")
            container_id = self._create_media_container(
                video_path=video_path,
                cover_image_path=cover_image_path
            )
            
            if not container_id:
                raise Exception("Failed to create media container")
            
            logger.info(f"[INSTAGRAM] Media container created: {container_id}")
            
            # Step 2: Update metadata (caption)
            logger.info("[INSTAGRAM] Step 2: Adding caption...")
            self._update_media_info(container_id, caption)
            
            # Step 3: Publish or schedule
            if schedule_at:
                logger.info(f"[INSTAGRAM] Step 3: Scheduling for {schedule_at}")
                result = self._schedule_publish(container_id, schedule_at)
            else:
                logger.info("[INSTAGRAM] Step 3: Publishing now...")
                result = self._publish_media(container_id)
            
            if result.get('success'):
                reel_id = result.get('reel_id')
                logger.info(f"[SUCCESS] Reel uploaded! ID: {reel_id}")
                return {
                    'success': True,
                    'reel_id': reel_id,
                    'url': f"https://instagram.com/reel/{reel_id}",
                    'status': 'PUBLISHED' if not schedule_at else 'SCHEDULED',
                    'publish_time': schedule_at.isoformat() if schedule_at else datetime.now().isoformat()
                }
            else:
                logger.error(f"[ERROR] Publishing failed: {result.get('error')}")
                return {
                    'success': False,
                    'error': result.get('error', 'Unknown error'),
                    'container_id': container_id
                }
        
        except Exception as e:
            logger.error(f"[ERROR] Upload failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _create_media_container(
        self,
        video_path: str,
        cover_image_path: Optional[str] = None
    ) -> Optional[str]:
        """
        Create media container (upload video to Instagram)
        """
        try:
            url = f"{self.INSTAGRAM_BUSINESS_API}/{self.business_account_id}/media"
            
            with open(video_path, 'rb') as video_file:
                # Upload video
                files = {
                    'media_type': (None, 'REELS'),
                    'video': ('reel.mp4', video_file, 'video/mp4'),
                }
                
                # Optional: Add cover image
                if cover_image_path and Path(cover_image_path).exists():
                    with open(cover_image_path, 'rb') as cover_file:
                        files['thumb'] = ('cover.jpg', cover_file, 'image/jpeg')
                        response = self.session.post(url, files=files)
                else:
                    response = self.session.post(url, files=files)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('id')
            else:
                logger.error(f"[ERROR] Container creation failed: {response.text}")
                return None
        
        except Exception as e:
            logger.error(f"[ERROR] Container creation error: {e}")
            return None
    
    def _update_media_info(self, container_id: str, caption: str) -> bool:
        """
        Update media metadata (caption, access level)
        """
        try:
            url = f"{self.INSTAGRAM_BUSINESS_API}/{container_id}"
            
            payload = {
                'caption': caption,
                'access_level': 'PUBLIC'  # or PRIVATE for private accounts
            }
            
            response = self.session.post(url, json=payload)
            
            if response.status_code == 200:
                logger.info("[INSTAGRAM] Caption added")
                return True
            else:
                logger.error(f"[ERROR] Caption update failed: {response.text}")
                return False
        
        except Exception as e:
            logger.error(f"[ERROR] Metadata update error: {e}")
            return False
    
    def _publish_media(self, container_id: str) -> Dict[str, Any]:
        """
        Publish media immediately
        """
        try:
            # Get IG account ID first
            account_id = self._get_ig_account_id()
            
            if not account_id:
                return {
                    'success': False,
                    'error': 'Could not retrieve IG account ID'
                }
            
            url = f"{self.INSTAGRAM_BUSINESS_API}/{account_id}/media_publish"
            
            payload = {
                'creation_id': container_id
            }
            
            response = self.session.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'reel_id': data.get('id')
                }
            else:
                return {
                    'success': False,
                    'error': response.text
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _schedule_publish(self, container_id: str, publish_at: datetime) -> Dict[str, Any]:
        """
        Schedule media publication
        """
        try:
            account_id = self._get_ig_account_id()
            
            if not account_id:
                return {
                    'success': False,
                    'error': 'Could not retrieve IG account ID'
                }
            
            url = f"{self.INSTAGRAM_BUSINESS_API}/{account_id}/media_publish"
            
            payload = {
                'creation_id': container_id,
                'publish_time': int(publish_at.timestamp())
            }
            
            response = self.session.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'reel_id': data.get('id'),
                    'scheduled_time': publish_at.isoformat()
                }
            else:
                return {
                    'success': False,
                    'error': response.text
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_ig_account_id(self) -> Optional[str]:
        """
        Get Instagram Account ID from Business Account ID
        """
        try:
            url = f"{self.INSTAGRAM_BUSINESS_API}/{self.business_account_id}?fields=instagram_business_account"
            
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                ig_account = data.get('instagram_business_account', {})
                return ig_account.get('id')
            else:
                logger.error(f"[ERROR] Failed to get IG account ID: {response.text}")
                return None
        
        except Exception as e:
            logger.error(f"[ERROR] Get IG account ID error: {e}")
            return None
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get business account information
        """
        try:
            url = f"{self.INSTAGRAM_BUSINESS_API}/{self.business_account_id}?fields=id,name,username,biography,profile_picture_url,followers_count,follower_count"
            
            response = self.session.get(url)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"[ERROR] Failed to get account info: {response.text}")
                return {}
        
        except Exception as e:
            logger.error(f"[ERROR] Get account info error: {e}")
            return {}
    
    def get_insights(self, metric: str = 'impressions') -> Dict[str, Any]:
        """
        Get account insights (followers, reach, impressions)
        
        Args:
            metric: One of 'impressions', 'reach', 'profile_views', 'follower_count'
        """
        try:
            url = f"{self.INSTAGRAM_BUSINESS_API}/{self.business_account_id}/insights"
            
            params = {
                'metric': metric,
                'period': 'day'
            }
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"[ERROR] Failed to get insights: {response.text}")
                return {}
        
        except Exception as e:
            logger.error(f"[ERROR] Get insights error: {e}")
            return {}


class InstagramScheduler:
    """
    Schedule multiple reel uploads
    """
    
    def __init__(self, uploader: InstagramUploader):
        self.uploader = uploader
        self.schedule = []
    
    def add_to_schedule(
        self,
        video_path: str,
        caption: str,
        publish_time: datetime,
        hashtags: Optional[list] = None,
        cover_image_path: Optional[str] = None
    ):
        """Add reel to upload schedule"""
        self.schedule.append({
            'video_path': video_path,
            'caption': caption,
            'publish_time': publish_time,
            'hashtags': hashtags or [],
            'cover_image_path': cover_image_path
        })
        
        logger.info(f"[SCHEDULER] Added: {Path(video_path).name} at {publish_time}")
    
    def process_schedule(self) -> list:
        """Process all scheduled uploads"""
        results = []
        
        for item in self.schedule:
            logger.info(f"[SCHEDULER] Processing: {Path(item['video_path']).name}")
            
            result = self.uploader.upload_reel(
                video_path=item['video_path'],
                caption=item['caption'],
                cover_image_path=item['cover_image_path'],
                schedule_at=item['publish_time'],
                hashtags=item['hashtags']
            )
            
            results.append(result)
            time.sleep(2)  # Rate limiting
        
        return results
    
    def clear_schedule(self):
        """Clear all scheduled uploads"""
        self.schedule = []
        logger.info("[SCHEDULER] Schedule cleared")


# Example usage function
def upload_example():
    """Example of how to use Instagram uploader"""
    
    # Get credentials from environment or config
    BUSINESS_ACCOUNT_ID = "YOUR_BUSINESS_ACCOUNT_ID"
    ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
    
    # Initialize uploader
    uploader = InstagramUploader(BUSINESS_ACCOUNT_ID, ACCESS_TOKEN)
    
    # Upload immediately
    result = uploader.upload_reel(
        video_path="output/reel_20260402_120000.mp4",
        caption="Check out this amazing reel! 🎬✨",
        hashtags=['#reels', '#shorts', '#viral']
    )
    
    print(f"Upload result: {result}")
    
    # Or schedule for later
    scheduled_time = datetime.now() + timedelta(hours=2)
    
    result = uploader.upload_reel(
        video_path="output/reel_20260402_130000.mp4",
        caption="Scheduled reel coming up soon! 🚀",
        schedule_at=scheduled_time,
        hashtags=['#schedule', '#automation']
    )
    
    print(f"Scheduled result: {result}")
