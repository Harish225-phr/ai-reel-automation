"""
Stock Video Fetcher Module for AI Reel Automation.
Downloads high-quality videos from multiple sources (Pexels, Pixabay).
"""

import os
import random
import tempfile
from pathlib import Path
from utils import logger
import config

# Try to import requests, fallback to urllib if not available
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    import urllib.request
    HAS_REQUESTS = False


class VideoFetcher:
    """Fetch and download stock videos from multiple sources."""
    
    # API endpoints
    PEXELS_BASE = 'https://api.pexels.com/videos/search'
    PIXABAY_BASE = 'https://pixabay.com/api/videos/'
    
    # API keys from config (or environment variables)
    PEXELS_API_KEY = os.environ.get('PEXELS_API_KEY') or config.PEXELS_API_KEY
    PIXABAY_API_KEY = os.environ.get('PIXABAY_API_KEY') or config.PIXABAY_API_KEY
    
    # VIDEO CACHE: Avoid re-downloading same keyword videos
    _video_cache = {}
    
    def __init__(self, output_dir='videos'):
        """
        Initialize the video fetcher.
        
        Args:
            output_dir (str): Directory to save downloaded videos
        """
        self.output_dir = output_dir
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Video fetcher initialized: output_dir={output_dir}")
    
    @staticmethod
    def fetch_pexels_videos(keyword, count=3):
        """
        Fetch videos from Pexels API and download them.
        Uses cache to avoid re-downloading same keyword videos.
        
        Args:
            keyword (str): Search query
            count (int): Number of videos to fetch
            
        Returns:
            list: List of downloaded video file paths
        """
        # CHECK CACHE FIRST! ⚡ INSTANT if cached
        cache_key = f"{keyword}_{count}"
        if cache_key in VideoFetcher._video_cache:
            cached_videos = VideoFetcher._video_cache[cache_key]
            logger.info(f"[CACHE HIT] Using cached videos for '{keyword}' ({len(cached_videos)} videos)")
            return cached_videos
        
        logger.info(f"[CACHE MISS] Downloading videos for '{keyword}'...")
        
        try:
            headers = {'Authorization': VideoFetcher.PEXELS_API_KEY}
            params = {
                'query': keyword,
                'per_page': count,
                'page': 1
            }
            
            response = requests.get(
                VideoFetcher.PEXELS_BASE,
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                video_paths = []
                
                for video in data.get('videos', []):
                    # Get the smallest HD video (usually 720p)
                    for video_file in video.get('video_files', []):
                        if video_file.get('quality') in ['hd', 'sd']:
                            url = video_file['link']
                            
                            # Download the video
                            try:
                                video_response = requests.get(url, timeout=30)
                                if video_response.status_code == 200:
                                    # Save to temp file
                                    import tempfile
                                    temp_file = tempfile.NamedTemporaryFile(
                                        suffix='.mp4',
                                        delete=False,
                                        dir='videos'
                                    )
                                    temp_file.write(video_response.content)
                                    temp_file.close()
                                    video_paths.append(temp_file.name)
                                    logger.debug(f"[OK] Downloaded video: {temp_file.name}")
                            except Exception as e:
                                logger.warning(f"Failed to download {url}: {e}")
                            
                            break
                
                logger.info(f"[OK] Fetched {len(video_paths)} videos from Pexels for '{keyword}'")
                # CACHE THE VIDEOS! 📁
                VideoFetcher._video_cache[cache_key] = video_paths
                logger.info(f"[CACHE] Stored {len(video_paths)} videos in cache")
                return video_paths
            else:
                logger.warning(f"Pexels API error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching from Pexels: {e}")
            return []
    
    @staticmethod
    def fetch_pixabay_videos(keyword, count=3):
        """
        Fetch videos from Pixabay API.
        
        Args:
            keyword (str): Search query
            count (int): Number of videos to fetch
            
        Returns:
            list: List of video info dicts
        """
        try:
            params = {
                'key': VideoFetcher.PIXABAY_API_KEY,
                'q': keyword,
                'per_page': count,
                'page': 1,
                'video_type': 'all'
            }
            
            response = requests.get(
                VideoFetcher.PIXABAY_BASE,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                videos = []
                
                for hit in data.get('hits', []):
                    videos.append({
                        'url': hit['videos']['small']['url'],  # Use small/preview
                        'duration': hit.get('duration', 0),
                        'source': 'pixabay'
                    })
                
                logger.info(f"[OK] Fetched {len(videos)} videos from Pixabay for '{keyword}'")
                return videos
            else:
                logger.warning(f"Pixabay API error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching from Pixabay: {e}")
            return []
    
    def download_video(self, url, video_id):
        """
        Download a video from URL.
        
        Args:
            url (str): Video URL
            video_id (str): Unique video identifier
            
        Returns:
            str: Path to downloaded video or None
        """
        try:
            output_path = os.path.join(
                self.output_dir,
                f'stock_video_{video_id}.mp4'
            )
            
            # Skip if already downloaded
            if os.path.exists(output_path):
                logger.info(f"Video already exists: {output_path}")
                return output_path
            
            # Download video
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
            
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            logger.info(f"[OK] Downloaded video: {output_path} ({size_mb:.2f} MB)")
            return output_path
            
        except Exception as e:
            logger.error(f"Error downloading video: {e}")
            return None
    
    def get_videos_for_keyword(self, keyword, count=5):
        """
        Get multiple stock videos for a keyword.
        
        Args:
            keyword (str): Search keyword
            count (int): Number of videos to fetch
            
        Returns:
            list: List of downloaded video paths or empty list
        """
        try:
            logger.info(f"Searching for videos related to '{keyword}'...")
            
            if not HAS_REQUESTS:
                logger.warning("[WARN] requests module not installed - video fetching unavailable")
                logger.info("Install with: pip install requests")
                return []
            
            all_videos = []
            
            # Try Pexels first
            logger.info(f"Attempting to fetch from Pexels...")
            try:
                pexels_videos = self.fetch_pexels_videos(keyword, count)
                all_videos.extend(pexels_videos)
            except Exception as e:
                logger.warning(f"Pexels fetch failed: {e}")
            
            # Try Pixabay as fallback
            if len(all_videos) < count:
                logger.info(f"Attempting to fetch from Pixabay...")
                try:
                    pixabay_videos = self.fetch_pixabay_videos(keyword, count - len(all_videos))
                    all_videos.extend(pixabay_videos)
                except Exception as e:
                    logger.warning(f"Pixabay fetch failed: {e}")
            
            if all_videos:
                logger.info(f"[OK] Found {len(all_videos)} videos")
                # Return video metadata (paths will be None as we can't download without requests)
                return [{'path': None, 'duration': 5, 'source': 'pexels/pixabay'} for _ in all_videos[:count]]
            else:
                logger.warning(f"[WARN] No videos found for '{keyword}'")
                return []
            
        except Exception as e:
            logger.error(f"Error getting videos: {e}")
            return []


def fetch_videos(keyword, count=5):
    """Convenience function to fetch videos."""
    fetcher = VideoFetcher()
    return fetcher.get_videos_for_keyword(keyword, count)
