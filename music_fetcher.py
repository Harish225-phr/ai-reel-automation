"""
Music Fetcher Module - Freesound API Integration
Fetches royalty-free background music for reels.

Features:
- Search background music by keyword
- Download MP3 audio files
- Retry with related keywords if needed
- Save to assets/music/
- Fallback to local music

Freesound Categories:
- Motivational music
- Cinematic background
- Nature background music

Usage:
    fetcher = FreesoundMusicFetcher()
    music = fetcher.search_and_download("motivational music")
"""

import os
import requests
from pathlib import Path
from urllib.parse import urlparse, urljoin
from utils import logger
import config


class FreesoundMusicFetcher:
    """Fetch background music from Freesound API."""
    
    BASE_URL = "https://freesound.org/api/v2"
    
    MUSIC_SEARCHES = [
        "motivational music",
        "cinematic background",
        "nature background music",
        "ambient music",
        "royalty free background",
    ]
    
    def __init__(self, api_key=None, output_dir=None):
        """
        Initialize Freesound fetcher.
        
        Args:
            api_key (str): Freesound API key
            output_dir (str): Directory to save music
        """
        self.api_key = api_key or config.FREESOUND_API_KEY
        self.output_dir = output_dir or config.MUSIC_DIR
        
        if not self.api_key:
            raise ValueError("[ERROR] FREESOUND_API_KEY not configured")
        
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"[FREESOUND] Initialized - API key: {self.api_key[:10]}...")
    
    def search_sounds(self, query, filter_str="", sort="-rating", limit=15):
        """
        Search sounds on Freesound.
        
        Args:
            query (str): Search keyword
            filter_str (str): Additional Freesound filters
            sort (str): Sort by (-rating, -downloads, -created)
            limit (int): Number of results
        
        Returns:
            list: Sound data from API
        """
        try:
            search_url = f"{self.BASE_URL}/search/text/"
            
            params = {
                "query": query,
                "token": self.api_key,
                "sort": sort,
                "limit": limit,
                "page_size": limit,
            }
            
            if filter_str:
                params["filter"] = filter_str
            
            logger.info(f"[FREESOUND] Searching: '{query}'")
            response = requests.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            sounds = data.get("results", [])
            
            logger.info(f"[FREESOUND] Found {len(sounds)} sounds")
            return sounds
        
        except requests.exceptions.RequestException as e:
            logger.error(f"[FREESOUND] API error: {e}")
            return []
    
    def filter_sounds_by_license(self, sounds, allow_cc=True):
        """
        Filter sounds by license (royalty-free, CC).
        
        Args:
            sounds (list): Sound list from API
            allow_cc (bool): Allow Creative Commons licenses
        
        Returns:
            list: Filtered sounds
        """
        filtered = []
        
        for sound in sounds:
            license_name = sound.get("license", "").lower()
            
            # Accept: CC0 (public), CC-BY (attribution), CC-BY-SA
            if "cc" in license_name.lower() or "public" in license_name.lower():
                filtered.append(sound)
                logger.debug(f"[FREESOUND] [OK] License: {license_name}")
            else:
                logger.debug(f"[FREESOUND] Skipped: {license_name}")
        
        logger.info(f"[FREESOUND] Filtered: {len(filtered)}/{len(sounds)} royalty-free")
        return filtered
    
    def filter_by_duration(self, sounds, max_duration=180):
        """
        Filter sounds by maximum duration.
        
        Args:
            sounds (list): Sound list
            max_duration (int): Maximum duration in seconds
        
        Returns:
            list: Filtered sounds
        """
        filtered = []
        
        for sound in sounds:
            duration = sound.get("duration", 0)
            
            if duration <= max_duration and duration > 5:
                filtered.append(sound)
                logger.debug(f"[FREESOUND] Duration: {duration:.1f}s [OK]")
            else:
                logger.debug(f"[FREESOUND] Skipped duration: {duration:.1f}s")
        
        return filtered
    
    def get_download_url(self, sound_data):
        """
        Get download URL for sound (prefer MP3).
        
        Args:
            sound_data (dict): Sound object from API
        
        Returns:
            str: Download URL or None
        """
        previews = sound_data.get("previews", {})
        
        # Try to get MP3 preview/download
        if "preview-hq-mp3" in previews:
            return previews["preview-hq-mp3"]
        elif "preview-lq-mp3" in previews:
            return previews["preview-lq-mp3"]
        
        # Try download URL (may require authorization)
        download_url = sound_data.get("url")
        if download_url:
            # Append format parameter for MP3
            return f"{download_url}download/?token={self.api_key}"
        
        return None
    
    def download_music(self, url, filename=None):
        """
        Download music file from URL.
        
        Args:
            url (str): Music URL
            filename (str): Optional custom filename
        
        Returns:
            str: Path to downloaded file or None
        """
        try:
            if not filename:
                parsed = urlparse(url)
                filename = os.path.basename(parsed.path) or "background_music.mp3"
            
            # Ensure .mp3 extension
            if not filename.lower().endswith('.mp3'):
                filename = os.path.splitext(filename)[0] + '.mp3'
            
            file_path = os.path.join(self.output_dir, filename)
            
            # Skip if already exists
            if os.path.exists(file_path):
                logger.info(f"[FREESOUND] Already downloaded: {filename}")
                return file_path
            
            logger.info(f"[FREESOUND] Downloading: {filename}")
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
                            logger.debug(f"[FREESOUND] Progress: {percent:.1f}%")
            
            # Verify file size
            if os.path.getsize(file_path) < 100000:  # Less than 100KB is probably invalid
                os.remove(file_path)
                logger.warning(f"[FREESOUND] File too small, deleted: {filename}")
                return None
            
            logger.info(f"[FREESOUND] Downloaded: {filename}")
            return file_path
        
        except Exception as e:
            logger.error(f"[FREESOUND] Download failed: {e}")
            return None
    
    def search_and_download(self, keywords=None, count=1):
        """
        Search and download background music. Retry with multiple keywords.
        
        Args:
            keywords (list): Search keywords (uses defaults if None)
            count (int): Number of music files to download
        
        Returns:
            list: Downloaded music file paths
        """
        keywords = keywords or self.MUSIC_SEARCHES
        downloaded = []
        
        for keyword in keywords:
            if len(downloaded) >= count:
                break
            
            logger.info(f"\n[FREESOUND] Searching: '{keyword}'")
            
            # Search
            sounds = self.search_sounds(keyword, limit=20)
            
            if not sounds:
                logger.warning(f"[FREESOUND] No sounds found for: '{keyword}'")
                continue
            
            # Filter by license
            filtered = self.filter_sounds_by_license(sounds)
            
            if not filtered:
                logger.warning(f"[FREESOUND] No royalty-free sounds for: '{keyword}'")
                continue
            
            # Filter by duration
            filtered = self.filter_by_duration(filtered, max_duration=180)
            
            if not filtered:
                logger.warning(f"[FREESOUND] No suitable duration for: '{keyword}'")
                continue
            
            # Download
            for sound in filtered:
                if len(downloaded) >= count:
                    break
                
                download_url = self.get_download_url(sound)
                if not download_url:
                    logger.debug("[FREESOUND] No download URL available")
                    continue
                
                title = sound.get("name", "music").replace(" ", "_")
                filename = f"{title}_{len(downloaded)+1}.mp3"
                
                path = self.download_music(download_url, filename)
                
                if path:
                    downloaded.append(path)
        
        if not downloaded:
            logger.warning("[FREESOUND] Failed to download any music. Using fallback.")
            return []
        
        logger.info(f"\n[FREESOUND] Downloaded {len(downloaded)} music tracks")
        return downloaded


def get_fallback_music(count=1):
    """
    Get fallback local music if API fails.
    
    Args:
        count (int): Number of music files
    
    Returns:
        list: Local music file paths
    """
    music_dir = config.MUSIC_DIR
    Path(music_dir).mkdir(parents=True, exist_ok=True)
    
    # Check if any music exists locally
    music_files = list(Path(music_dir).glob("*.mp3")) + \
                  list(Path(music_dir).glob("*.wav")) + \
                  list(Path(music_dir).glob("*.m4a"))
    
    if music_files:
        logger.info(f"[FALLBACK] Using local music: {len(music_files)} available")
        return [str(f) for f in music_files[:count]]
    
    logger.warning("[FALLBACK] No local music available")
    return []


if __name__ == "__main__":
    # Test Freesound API
    fetcher = FreesoundMusicFetcher()
    music = fetcher.search_and_download(count=1)
    print(f"Downloaded: {music}")
