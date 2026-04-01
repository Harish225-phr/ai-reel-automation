"""
Music Fetcher with Fallback Audio Generator
Tries Freesound API, falls back to procedural audio generation
"""

import os
from pathlib import Path
import logging
import numpy as np
from scipy import signal
from scipy.io import wavfile

logger = logging.getLogger(__name__)

try:
    import requests
except ImportError:
    requests = None


class EnhancedMusicFetcher:
    """
    Fetch music with intelligent fallback to procedural audio generation.
    """
    
    FREESOUND_API_BASE = 'https://freesound.org/api/v2/search/text/'
    
    def __init__(self, api_key=None, output_dir='music'):
        """Initialize music fetcher."""
        self.api_key = api_key
        self.output_dir = output_dir
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Enhanced Music Fetcher initialized: {output_dir}")
    
    def fetch_music(self, query, duration=30, music_type='calm'):
        """
        Fetch music with fallback to procedural generation.
        
        Args:
            query (str): Search query for Freesound
            duration (float): Duration in seconds
            music_type (str): Type of music (calm, energetic, spiritual, etc.)
            
        Returns:
            str: Path to music file or None
        """
        # Try Freesound first
        if self.api_key:
            try:
                logger.info(f"[MUSIC] Trying Freesound API: '{query}'")
                music_path = self._fetch_from_freesound(query)
                if music_path:
                    logger.info(f"[MUSIC] ✅ Got from Freesound: {os.path.basename(music_path)}")
                    return music_path
            except Exception as e:
                logger.warning(f"[MUSIC] Freesound failed: {e}")
        
        # Fallback to procedural generation
        try:
            logger.info(f"[MUSIC] Generating procedural {music_type} audio...")
            music_path = self._generate_fallback_music(duration, music_type)
            if music_path:
                logger.info(f"[MUSIC] ✅ Generated: {os.path.basename(music_path)}")
                return music_path
        except Exception as e:
            logger.warning(f"[MUSIC] Generation failed: {e}")
        
        logger.warning("[MUSIC] No music available - voice only")
        return None
    
    def _fetch_from_freesound(self, query):
        """Try to fetch from Freesound API."""
        if not requests or not self.api_key:
            return None
        
        try:
            params = {
                'query': query,
                'token': self.api_key,
                'sort': '-rating',
                'limit': 5,
                'page_size': 5
            }
            
            response = requests.get(
                self.FREESOUND_API_BASE,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                if results:
                    # Download first result
                    sound = results[0]
                    # Return sound info (would need actual download logic)
                    logger.debug(f"Found sound: {sound.get('name')}")
                    return None  # Placeholder
            
            return None
            
        except Exception as e:
            logger.debug(f"Freesound error: {e}")
            return None
    
    def _generate_fallback_music(self, duration, music_type):
        """
        Generate fallback music using procedural audio with scipy.
        
        Args:
            duration (float): Duration in seconds
            music_type (str): calm, energetic, spiritual, etc.
            
        Returns:
            str: Path to generated audio file
        """
        try:
            sample_rate = 44100
            num_samples = int(duration * sample_rate)
            t = np.linspace(0, duration, num_samples)
            
            # Generate audio based on type
            if music_type in ['calm', 'spiritual', 'peaceful', 'devotional']:
                # Ambient pad: multiple frequencies creating peaceful atmosphere
                audio = np.zeros(num_samples)
                
                # Use peaceful frequencies
                frequencies = [65.41, 98.00, 146.83, 164.81]  # C2, G2, D3, E3
                amplitudes = [0.25, 0.2, 0.3, 0.25]
                
                for freq, amp in zip(frequencies, amplitudes):
                    # Add slight chorus effect
                    phase_variation = 0.02 * np.sin(t * 0.5)
                    audio += amp * np.sin(2 * np.pi * freq * (t + phase_variation))
                
                volume = 0.15
                
            elif music_type in ['energetic', 'motivational', 'upbeat']:
                # Nature-like sounds: filtered noise
                audio = np.random.normal(0, 1, num_samples)
                
                # Low-pass filter for waves/nature sound
                b, a = signal.butter(2, 0.04)
                try:
                    audio = signal.filtfilt(b, a, audio)
                    audio = signal.filtfilt(b, a, audio)
                except:
                    pass
                
                volume = 0.12
            else:
                # Default: calm/spiritual
                audio = np.zeros(num_samples)
                frequencies = [65.41, 98.00, 146.83]
                amplitudes = [0.25, 0.2, 0.3]
                
                for freq, amp in zip(frequencies, amplitudes):
                    phase_variation = 0.02 * np.sin(t * 0.5)
                    audio += amp * np.sin(2 * np.pi * freq * (t + phase_variation))
                
                volume = 0.15
            
            # Fade in and out
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
            
            # Save to WAV file
            timestamp = __import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S%f')[-6:]
            filename = f"music_{music_type}_{timestamp}.wav"
            filepath = os.path.join(self.output_dir, filename)
            
            wavfile.write(filepath, sample_rate, audio_int16)
            logger.info(f"[MUSIC] Generated {music_type} audio: {filename} ({duration:.1f}s)")
            
            return filepath
            
        except Exception as e:
            logger.error(f"[MUSIC] Generation error: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return None
