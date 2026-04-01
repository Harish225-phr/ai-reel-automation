"""
Media Fetcher Module - Pexels API Integration
Fetches high-quality stock videos from Pexels.

Features:
- Search videos by keyword
- Filter by dimensions (height >= 1280, width >= 720)
- Download HD vertical videos
- Retry with related keywords if no videos found
- Save to content/videos/

Usage:
    fetcher = PexelsMediaFetcher()
    videos = fetcher.search_and_download("motivation", count=5)
"""

import os
import requests
from pathlib import Path
from urllib.parse import urlparse
from utils import logger
import config


class PexelsMediaFetcher:
    """Fetch stock videos from Pexels API."""
    
    BASE_URL = "https://api.pexels.com/videos/search"
    
    def __init__(self, api_key=None, output_dir=None):
        """
        Initialize Pexels fetcher.
        
        Args:
            api_key (str): Pexels API key
            output_dir (str): Directory to save videos
        """
        self.api_key = api_key or config.PEXELS_API_KEY
        self.output_dir = output_dir or config.CONTENT_VIDEOS_DIR
        
        if not self.api_key:
            raise ValueError("[ERROR] PEXELS_API_KEY not configured")
        
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"[PEXELS] Initialized - API key: {self.api_key[:10]}...")
    
    def search_videos(self, query, per_page=5, min_duration=5):
        """
        Search videos on Pexels.
        
        Args:
            query (str): Search keyword
            per_page (int): Number of results
            min_duration (int): Minimum video duration in seconds
        
        Returns:
            list: Video data from API
        """
        try:
            headers = {"Authorization": self.api_key}
            params = {
                "query": query,
                "per_page": per_page,
            }
            
            logger.info(f"[PEXELS] Searching: '{query}'")
            response = requests.get(self.BASE_URL, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            videos = data.get("videos", [])
            
            logger.info(f"[PEXELS] Found {len(videos)} videos")
            return videos
        
        except requests.exceptions.RequestException as e:
            logger.error(f"[PEXELS] API error: {e}")
            return []
    
    def filter_videos(self, videos, min_width=720, min_height=1280):
        """
        Filter videos by minimum dimensions (vertical format).
        
        Args:
            videos (list): Video list from API
            min_width (int): Minimum width
            min_height (int): Minimum height
        
        Returns:
            list: Filtered videos
        """
        filtered = []
        
        for video in videos:
            width = video.get("width", 0)
            height = video.get("height", 0)
            
            # For vertical reels: height >= 1280, width >= 720
            if height >= min_height and width >= min_width:
                filtered.append(video)
                logger.debug(f"[PEXELS] Video: {width}x{height} [OK]")
            else:
                logger.debug(f"[PEXELS] Skipped: {width}x{height} (too small)")
        
        logger.info(f"[PEXELS] Filtered: {len(filtered)}/{len(videos)} suitable for vertical")
        return filtered
    
    def get_best_video_url(self, video_data):
        """
        Get best HD video URL from Pexels video data.
        
        Args:
            video_data (dict): Video object from API
        
        Returns:
            str: Video URL
        """
        video_files = video_data.get("video_files", [])
        
        # Sort by width descending to get HD
        sorted_files = sorted(video_files, key=lambda x: x.get("width", 0), reverse=True)
        
        if sorted_files:
            url = sorted_files[0].get("link")
            logger.debug(f"[PEXELS] Selected: {sorted_files[0].get('width')}x{sorted_files[0].get('height')}")
            return url
        
        return None
    
    def download_video(self, url, filename=None):
        """
        Download video from URL.
        
        Args:
            url (str): Video URL
            filename (str): Optional custom filename
        
        Returns:
            str: Path to downloaded file or None
        """
        try:
            if not filename:
                # Extract filename from URL
                parsed = urlparse(url)
                filename = os.path.basename(parsed.path) or "video.mp4"
            
            file_path = os.path.join(self.output_dir, filename)
            
            # Skip if already exists
            if os.path.exists(file_path):
                logger.info(f"[PEXELS] Already downloaded: {filename}")
                return file_path
            
            logger.info(f"[PEXELS] Downloading: {filename}")
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024*1024):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size:
                            percent = (downloaded / total_size) * 100
                            logger.debug(f"[PEXELS] Progress: {percent:.1f}%")
            
            logger.info(f"[PEXELS] Downloaded: {filename}")
            return file_path
        
        except Exception as e:
            logger.error(f"[PEXELS] Download failed: {e}")
            return None
    
    def search_and_download(self, keyword, count=5, retry_keywords=None):
        """
        Search and download videos. Retry with keyword variations only.
        
        Args:
            keyword (str): Main search keyword
            count (int): Number of videos to download
            retry_keywords (list): Keyword variations if first search fails
        
        Returns:
            list: Downloaded video file paths
        """
        # Smart retry: keyword variations only (no generic fallbacks like "nature")
        if retry_keywords is None:
            retry_keywords = [
                keyword + " background",
                keyword + " clip",
                keyword + " footage"
            ]
        
        all_keywords = [keyword] + retry_keywords
        downloaded = []
        
        for kw in all_keywords:
            if len(downloaded) >= count:
                break
            
            logger.info(f"\n[PEXELS] Attempt with keyword: '{kw}'")
            
            # Search
            videos = self.search_videos(kw, per_page=max(10, count * 2))
            
            if not videos:
                logger.warning(f"[PEXELS] No videos found for: '{kw}'")
                continue
            
            # Filter for vertical format
            filtered = self.filter_videos(videos)
            
            if not filtered:
                logger.warning(f"[PEXELS] No vertical videos for: '{kw}'")
                continue
            
            # Download
            for i, video in enumerate(filtered):
                if len(downloaded) >= count:
                    break
                
                video_url = self.get_best_video_url(video)
                if not video_url:
                    continue
                
                filename = f"{kw.replace(' ', '_')}_{len(downloaded)+1}.mp4"
                path = self.download_video(video_url, filename)
                
                if path:
                    downloaded.append(path)
        
        if not downloaded:
            logger.warning("[PEXELS] Failed to download any videos. Using fallback.")
            return []
        
        logger.info(f"\n[PEXELS] Downloaded {len(downloaded)} videos")
        return downloaded


# Alternative fallback - use cached/local videos
def get_fallback_videos(keyword, count=3):
    """
    Get fallback local videos if API fails.
    
    Args:
        keyword (str): Search keyword
        count (int): Number of videos
    
    Returns:
        list: Local video file paths
    """
    video_dir = config.CONTENT_VIDEOS_DIR
    Path(video_dir).mkdir(parents=True, exist_ok=True)
    
    # Check if any videos exist locally
    video_files = list(Path(video_dir).glob("*.mp4")) + \
                  list(Path(video_dir).glob("*.mov")) + \
                  list(Path(video_dir).glob("*.avi"))
    
    if video_files:
        logger.info(f"[FALLBACK] Using local videos: {len(video_files)} available")
        return [str(f) for f in video_files[:count]]
    
    logger.warning("[FALLBACK] No local videos available")
    return []


if __name__ == "__main__":
    # Test Pexels API
    fetcher = PexelsMediaFetcher()
    videos = fetcher.search_and_download("motivation", count=3)
    print(f"Downloaded: {videos}")
