"""
Fallback Audio Generation for missing background music.
Creates simple atmosphere sounds that don't require external APIs.
"""

import os
import numpy as np
from scipy import signal
import logging

logger = logging.getLogger(__name__)

class FallbackAudioGenerator:
    """Generate simple fallback audio when no music is available"""
    
    @staticmethod
    def create_silence(duration_seconds, sample_rate=44100):
        """
        Create silent audio track (fallback).
        
        Args:
            duration_seconds (float): Duration of silence
            sample_rate (int): Sample rate (Hz)
            
        Returns:
            np.array: Silent audio data
        """
        try:
            num_samples = int(duration_seconds * sample_rate)
            silence = np.zeros(num_samples, dtype=np.float32)
            logger.debug(f"[FALLBACK] Created silence: {duration_seconds:.1f}s")
            return silence
        except Exception as e:
            logger.error(f"[FALLBACK] Error creating silence: {e}")
            return None
    
    @staticmethod
    def create_drone_tone(duration_seconds, frequency=111.0, sample_rate=44100, volume=0.15):
        """
        Create a simple drone/ambient tone (good for meditation, spiritual content).
        Uses a sine wave with very low amplitude for background atmosphere.
        
        Args:
            duration_seconds (float): Duration
            frequency (float): Frequency in Hz (111 Hz = spiritual/healing frequency)
            sample_rate (int): Sample rate
            volume (float): Volume multiplier (0.0-1.0)
            
        Returns:
            np.array: Audio data
        """
        try:
            num_samples = int(duration_seconds * sample_rate)
            t = np.linspace(0, duration_seconds, num_samples)
            
            # Main tone
            tone = np.sin(2 * np.pi * frequency * t)
            
            # Add subtle harmonics
            tone += 0.3 * np.sin(2 * np.pi * frequency * 2 * t)  # Octave
            tone += 0.2 * np.sin(2 * np.pi * frequency * 1.5 * t)  # Fifth
            
            # Fade in and out for smooth transitions
            fade_time = min(2.0, duration_seconds / 4)
            fade_samples = int(fade_time * sample_rate)
            
            if fade_samples > 0:
                fade_in = np.linspace(0, 1, fade_samples)
                fade_out = np.linspace(1, 0, fade_samples)
                tone[:fade_samples] *= fade_in
                tone[-fade_samples:] *= fade_out
            
            # Normalize and apply volume
            tone = tone / np.max(np.abs(tone)) * volume
            tone = tone.astype(np.float32)
            
            logger.info(f"[FALLBACK] Created drone tone: {duration_seconds:.1f}s @ {frequency}Hz")
            return tone
            
        except Exception as e:
            logger.error(f"[FALLBACK] Error creating drone: {e}")
            return None
    
    @staticmethod
    def create_ambient_pad(duration_seconds, sample_rate=44100, volume=0.12):
        """
        Create atmospheric ambient pad using multiple frequencies.
        Good for peaceful, meditative, or spiritual content.
        
        Args:
            duration_seconds (float): Duration
            sample_rate (int): Sample rate
            volume (float): Volume multiplier
            
        Returns:
            np.array: Audio data
        """
        try:
            num_samples = int(duration_seconds * sample_rate)
            t = np.linspace(0, duration_seconds, num_samples)
            audio = np.zeros(num_samples)
            
            # Multiple frequencies for richness
            frequencies = [65.41, 98.00, 146.83, 164.81]  # C2, G2, D3, E3 - peaceful scale
            amplitudes = [0.25, 0.2, 0.3, 0.25]
            
            for freq, amp in zip(frequencies, amplitudes):
                # Add slight chorus effect by varying the phase
                phase_variation = 0.02 * np.sin(t * 0.5)
                audio += amp * np.sin(2 * np.pi * freq * (t + phase_variation))
            
            # Fade in and out
            fade_time = min(3.0, duration_seconds / 4)
            fade_samples = int(fade_time * sample_rate)
            
            if fade_samples > 0:
                fade_in = np.linspace(0, 1, fade_samples)
                fade_out = np.linspace(1, 0, fade_samples)
                audio[:fade_samples] *= fade_in
                audio[-fade_samples:] *= fade_out
            
            # Normalize
            audio = audio / np.max(np.abs(audio)) * volume
            audio = audio.astype(np.float32)
            
            logger.info(f"[FALLBACK] Created ambient pad: {duration_seconds:.1f}s")
            return audio
            
        except Exception as e:
            logger.error(f"[FALLBACK] Error creating ambient pad: {e}")
            return None
    
    @staticmethod
    def create_nature_sounds(duration_seconds, sound_type='rain', sample_rate=44100, volume=0.10):
        """
        Create simple nature-like sounds (rain, wind, etc).
        
        Args:
            duration_seconds (float): Duration
            sound_type (str): 'rain', 'wind', 'waves'
            sample_rate (int): Sample rate
            volume (float): Volume
            
        Returns:
            np.array: Audio data
        """
        try:
            num_samples = int(duration_seconds * sample_rate)
            
            if sound_type == 'rain':
                # White noise with gentle filtering
                audio = np.random.normal(0, 1, num_samples)
                # Low pass filter for softer rain sound
                from scipy import signal
                b, a = signal.butter(2, 0.05)  # 2nd order butterworth, 5% cutoff
                try:
                    audio = signal.filtfilt(b, a, audio)
                except:
                    pass
                
            elif sound_type == 'wind':
                # Lower frequency noise
                audio = np.random.normal(0, 1, num_samples)
                b, a = signal.butter(2, 0.03)  # Even lower cutoff
                try:
                    audio = signal.filtfilt(b, a, audio)
                except:
                    pass
                    
            elif sound_type == 'waves':
                # Colored noise with resonance
                audio = np.random.normal(0, 1, num_samples)
                # Multiple passes for deeper color
                b, a = signal.butter(2, 0.04)
                try:
                    audio = signal.filtfilt(b, a, audio)
                    audio = signal.filtfilt(b, a, audio)
                except:
                    pass
            else:
                audio = np.zeros(num_samples)
            
            # Fade in and out
            fade_time = min(2.0, duration_seconds / 5)
            fade_samples = int(fade_time * sample_rate)
            
            if fade_samples > 0:
                fade_in = np.linspace(0, 1, fade_samples)
                fade_out = np.linspace(1, 0, fade_samples)
                audio[:fade_samples] *= fade_in
                audio[-fade_samples:] *= fade_out
            
            # Normalize
            audio = audio / np.max(np.abs(audio)) * volume
            audio = audio.astype(np.float32)
            
            logger.info(f"[FALLBACK] Created {sound_type} sounds: {duration_seconds:.1f}s")
            return audio
            
        except Exception as e:
            logger.error(f"[FALLBACK] Error creating {sound_type}: {e}")
            return None
