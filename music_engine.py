"""
Music Engine - Fetch background music from Pixabay
Supports multiple music types with intelligent fallback
"""

import os
import logging
from pathlib import Path
from typing import Optional
import requests
import re

logger = logging.getLogger(__name__)


class PixabayMusicFetcher:
    """Fetch high-quality background music from Pixabay."""
    
    PIXABAY_API_BASE = "https://pixabay.com/api/videos/"
    
    MUSIC_SEARCH_QUERIES = {
        'calm': ['calm ambient music', 'peaceful background', 'meditation music'],
        'spiritual': ['spiritual background music', 'devotional music', 'peaceful ambient'],
        'motivational': ['motivational background music', 'inspiring music', 'uplifting'],
        'energetic': ['energetic music', 'dynamic background', 'upbeat music'],
        'cinematic': ['cinematic background', 'epic music', 'dramatic background'],
    }
    
    def __init__(self, api_key: Optional[str] = None, output_dir: str = 'music'):
        """Initialize Pixabay fetcher."""
        self.api_key = api_key or os.getenv('PIXABAY_API_KEY')
        self.output_dir = output_dir
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        
        if not self.api_key:
            logger.warning("[MUSIC] No Pixabay API key provided. Using fallback only.")
        else:
            logger.info("[MUSIC] Pixabay fetcher initialized")
    
    def fetch_music(self, music_type: str = 'calm', duration_min: int = 20) -> Optional[str]:
        """
        Fetch background music from Pixabay.
        
        Args:
            music_type (str): Type of music (calm, spiritual, motivational, energetic, cinematic)
            duration_min (int): Minimum duration in seconds
            
        Returns:
            Path to downloaded music file or None
        """
        
        if not self.api_key:
            logger.info("[MUSIC] No API key. Using procedural fallback.")
            return self._generate_procedural_audio(music_type, 30)
        
        # Get search queries for music type
        queries = self.MUSIC_SEARCH_QUERIES.get(music_type, self.MUSIC_SEARCH_QUERIES['calm'])
        
        for query in queries:
            try:
                logger.info(f"[MUSIC] Searching Pixabay for: {query}")
                music_path = self._search_and_download(query, duration_min)
                
                if music_path:
                    logger.info(f"[MUSIC] ✓ Downloaded: {os.path.basename(music_path)}")
                    return music_path
                    
            except Exception as e:
                logger.warning(f"[MUSIC] Search failed for '{query}': {e}")
        
        # Fallback to procedural
        logger.info("[MUSIC] Pixabay search failed. Using procedural audio.")
        return self._generate_procedural_audio(music_type, 30)
    
    def _search_and_download(self, query: str, duration_min: int) -> Optional[str]:
        """Search and download music from Pixabay."""
        
        try:
            params = {
                'key': self.api_key,
                'q': query,
                'order': 'popular',
                'per_page': 5,
                'video_type': 'film'
            }
            
            response = requests.get(
                self.PIXABAY_API_BASE,
                params=params,
                timeout=10
            )
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            hits = data.get('hits', [])
            
            if not hits:
                return None
            
            # Find video with suitable duration
            for video in hits:
                # Get preview URL (highest quality available)
                video_url = video.get('videos', {}).get('large', {}).get('url')
                
                if not video_url:
                    continue
                
                # Download video
                logger.info(f"[MUSIC] Downloading: {video.get('id')}")
                
                try:
                    music_response = requests.get(video_url, timeout=30)
                    
                    if music_response.status_code == 200:
                        # Save as MP3/WAV
                        filename = f"music_pixabay_{video.get('id')}.mp4"
                        filepath = os.path.join(self.output_dir, filename)
                        
                        with open(filepath, 'wb') as f:
                            f.write(music_response.content)
                        
                        logger.info(f"[MUSIC] Saved: {filename}")
                        return filepath
                        
                except Exception as e:
                    logger.warning(f"[MUSIC] Download error: {e}")
            
            return None
            
        except Exception as e:
            logger.error(f"[MUSIC] Pixabay error: {e}")
            return None
    
    def _generate_procedural_audio(self, music_type: str, duration: int = 30) -> Optional[str]:
        """
        Generate procedural background music as fallback.
        Uses scipy to create ambient audio.
        """
        
        try:
            import numpy as np
            from scipy import signal
            from scipy.io import wavfile
            
            logger.info(f"[MUSIC] Generating procedural {music_type} audio ({duration}s)...")
            
            sample_rate = 44100
            num_samples = int(duration * sample_rate)
            t = np.linspace(0, duration, num_samples)
            
            # Generate audio based on type
            if music_type in ['calm', 'spiritual', 'peaceful']:
                # Ambient pad: peaceful frequencies
                audio = np.zeros(num_samples)
                frequencies = [65.41, 98.00, 146.83, 164.81]  # C2, G2, D3, E3
                amplitudes = [0.25, 0.2, 0.3, 0.25]
                
                for freq, amp in zip(frequencies, amplitudes):
                    phase_variation = 0.02 * np.sin(t * 0.5)
                    audio += amp * np.sin(2 * np.pi * freq * (t + phase_variation))
                
                volume = 0.12
                
            elif music_type in ['motivational', 'energetic', 'cinematic']:
                # Nature sounds: filtered noise
                audio = np.random.normal(0, 1, num_samples)
                b, a = signal.butter(2, 0.04)
                
                try:
                    audio = signal.filtfilt(b, a, audio)
                    audio = signal.filtfilt(b, a, audio)
                except:
                    pass
                
                volume = 0.12
            else:
                # Default: calm
                audio = np.zeros(num_samples)
                frequencies = [65.41, 98.00, 146.83]
                amplitudes = [0.25, 0.2, 0.3]
                
                for freq, amp in zip(frequencies, amplitudes):
                    phase_variation = 0.02 * np.sin(t * 0.5)
                    audio += amp * np.sin(2 * np.pi * freq * (t + phase_variation))
                
                volume = 0.12
            
            # Fade in/out
            fade_time = min(3.0, duration / 4)
            fade_samples = int(fade_time * sample_rate)
            
            if fade_samples > 0:
                fade_in = np.linspace(0, 1, fade_samples)
                fade_out = np.linspace(1, 0, fade_samples)
                audio[:fade_samples] *= fade_in
                audio[-fade_samples:] *= fade_out
            
            # Normalize and apply volume
            if np.max(np.abs(audio)) > 0:
                audio = audio / np.max(np.abs(audio)) * volume
            else:
                audio = audio * volume
            
            # Convert to int16
            audio_int16 = np.int16(audio * 32767)
            
            # Save
            filename = f"music_procedural_{music_type}.wav"
            filepath = os.path.join(self.output_dir, filename)
            
            wavfile.write(filepath, sample_rate, audio_int16)
            logger.info(f"[MUSIC] ✓ Generated: {filename}")
            
            return filepath
            
        except ImportError:
            logger.error("[MUSIC] scipy not available for procedural audio")
            return None
        except Exception as e:
            logger.error(f"[MUSIC] Procedural generation error: {e}")
            return None


class MusicEngine:
    """Main music fetching engine."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize music engine."""
        self.fetcher = PixabayMusicFetcher(api_key=api_key)
    
    def fetch(self, music_type: str = 'calm', duration: int = 30) -> Optional[str]:
        """
        Fetch background music.
        
        Args:
            music_type (str): Type of music
            duration (int): Target duration in seconds
            
        Returns:
            Path to music file or None
        """
        return self.fetcher.fetch_music(music_type, duration)
