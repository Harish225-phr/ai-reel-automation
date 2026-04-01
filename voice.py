"""
Voice Generation Module for AI Reel Automation.
Generates text-to-speech audio using Microsoft Edge TTS.
Produces natural-sounding AI voices with better prosody than gTTS.
"""

import os
import asyncio
from pathlib import Path
from utils import logger, ensure_directories, get_output_filename


class EdgeTTSGenerator:
    """Generate natural-sounding voice using Microsoft Edge TTS."""
    
    # Available voices - all sound natural and professional
    VOICES = {
        'male': [
            'en-US-GuyNeural',
            'en-US-AriaNeural',  # Also works as neutral
            'en-GB-RyanNeural',  # British accent
            'en-AU-WilliamNeural',  # Australian accent
        ],
        'female': [
            'en-US-AriaNeural',
            'en-US-AvaNeural',
            'en-GB-SoniaNeural',  # British accent
            'en-AU-NatashaNeural',  # Australian accent
        ]
    }
    
    def __init__(self, voice_type='female', output_dir='audio'):
        """
        Initialize Edge TTS generator.
        
        Args:
            voice_type (str): 'male' or 'female'
            output_dir (str): Directory to save audio files
        """
        try:
            import edge_tts
            self.edge_tts = edge_tts
        except ImportError:
            logger.error("[ERROR] edge_tts not installed. Run: pip install edge-tts")
            raise
        
        self.voice_type = voice_type
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Edge TTS initialized: voice_type={voice_type}, output_dir={output_dir}")
    
    def get_random_voice(self):
        """Get a random voice for the specified type."""
        import random
        voices = self.VOICES.get(self.voice_type, self.VOICES['female'])
        return random.choice(voices)
    
    async def generate_audio_async(self, text, voice=None):
        """
        Generate audio asynchronously.
        
        Args:
            text (str): Text to convert to speech
            voice (str): Voice to use (or None for random)
            
        Returns:
            bytes: Audio data in MP3 format
        """
        try:
            if voice is None:
                voice = self.get_random_voice()
            
            logger.info(f"Generating audio with voice: {voice}")
            
            communicate = self.edge_tts.Communicate(
                text=text,
                voice=voice,
                rate='+0%',  # Normal speed
                volume='+0%'  # Normal volume
            )
            
            # Collect audio data
            audio_data = b''
            async for chunk in communicate.stream():
                if chunk['type'] == 'audio':
                    audio_data += chunk['data']
            
            logger.info(f"[OK] Generated {len(audio_data)} bytes of audio")
            return audio_data
        
        except Exception as e:
            logger.error(f"Error generating audio: {e}")
            raise
    
    def generate_audio(self, text, voice=None):
        """
        Generate audio (synchronous wrapper).
        
        Args:
            text (str): Text to convert to speech
            voice (str): Voice to use (or None for random)
            
        Returns:
            bytes: Audio data in MP3 format
        """
        return asyncio.run(self.generate_audio_async(text, voice))
    
    def save_audio(self, text, output_path, voice=None):
        """
        Generate and save audio to file.
        
        Args:
            text (str): Text to convert to speech
            output_path (str): Path to save MP3 file
            voice (str): Voice to use (or None for random)
            
        Returns:
            str: Path to saved file
        """
        try:
            logger.info(f"Generating voice audio: {len(text)} characters")
            
            audio_data = self.generate_audio(text, voice)
            
            # Save to file
            with open(output_path, 'wb') as f:
                f.write(audio_data)
            
            file_size = os.path.getsize(output_path) / 1024  # Size in KB
            logger.info(f"[OK] Voice saved: {output_path} ({file_size:.2f} KB)")
            
            return output_path
        
        except Exception as e:
            logger.error(f"Error saving audio: {e}")
            raise


def generate_voice_from_script(script, voice_type='female', audio_dir='audio', selected_voice=None):
    """
    Generate voice from a script using Edge TTS.
    
    Args:
        script (str): Script text to convert
        voice_type (str): 'male' or 'female'
        audio_dir (str): Directory to save audio
        selected_voice (str): Specific voice to use (e.g., 'hi-IN-MadhurNeural')
                             If None, uses voice_type to pick random
        
    Returns:
        dict: Dictionary with audio path, script, and metadata
    """
    try:
        logger.info("=" * 50)
        logger.info("STARTING VOICE GENERATION (EDGE TTS)")
        logger.info("=" * 50)
        
        ensure_directories()
        
        # Initialize generator
        generator = EdgeTTSGenerator(voice_type=voice_type, output_dir=audio_dir)
        
        # Generate filename
        filename = f"voice_{get_output_filename('').replace('.', '')}.mp3"
        audio_path = os.path.join(audio_dir, filename)
        
        # Save audio (using selected_voice if provided)
        generator.save_audio(script, audio_path, voice=selected_voice)
        
        # Verify file was created
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file was not created: {audio_path}")
        
        result = {
            'audio_path': audio_path,
            'script': script,
            'voice_type': voice_type,
            'voice': selected_voice or 'random',
            'provider': 'edge-tts'
        }
        
        logger.info("=" * 50)
        logger.info("VOICE GENERATION COMPLETED [OK]")
        logger.info("=" * 50)
        
        return result
    
    except Exception as e:
        logger.error(f"Error generating voice: {e}")
        raise


def get_voice_duration(audio_path):
    """
    Get duration of audio file in seconds.
    
    Args:
        audio_path (str): Path to audio file
        
    Returns:
        float: Duration in seconds (or None if error)
    """
    try:
        from moviepy.audio.io.AudioFileClip import AudioFileClip
        
        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            return None
        
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        audio.close()
        
        logger.debug(f"Audio duration: {duration:.2f} seconds")
        return duration
    
    except Exception as e:
        logger.error(f"Error getting audio duration: {e}")
        return None


def validate_audio_file(audio_path):
    """
    Validate audio file integrity.
    
    Args:
        audio_path (str): Path to audio file
        
    Returns:
        bool: True if file is valid
    """
    try:
        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            return False
        
        # Check file size (minimum 5 KB for valid audio)
        file_size = os.path.getsize(audio_path)
        if file_size < 5120:
            logger.error(f"Audio file too small ({file_size} bytes): {audio_path}")
            return False
        
        # Try to open duration
        duration = get_voice_duration(audio_path)
        if duration is None or duration <= 0:
            logger.error(f"Invalid audio duration: {duration}")
            return False
        
        logger.info(f"[OK] Audio validated: {duration:.2f}s, {file_size} bytes")
        return True
    
    except Exception as e:
        logger.error(f"Audio validation error: {e}")
        return False


def generate_multiple_voices(scripts, voice_type='female', audio_dir='audio'):
    """
    Generate multiple voice files from scripts.
    
    Args:
        scripts (list): List of script strings
        voice_type (str): 'male' or 'female'
        audio_dir (str): Directory to save audio
        
    Returns:
        list: List of dictionaries with voice data
    """
    try:
        voices = []
        
        for i, script in enumerate(scripts):
            logger.info(f"\nGenerating voice {i+1}/{len(scripts)}...")
            voice_data = generate_voice_from_script(
                script=script,
                voice_type=voice_type,
                audio_dir=audio_dir
            )
            voices.append(voice_data)
        
        logger.info(f"\n[OK] Generated {len(voices)} voices successfully")
        return voices
    
    except Exception as e:
        logger.error(f"Error generating multiple voices: {e}")
        raise


if __name__ == "__main__":
    # Test voice generation
    try:
        test_script = "Trees are incredible. They absorb carbon dioxide and produce oxygen. One mature tree can provide oxygen for two people. This is why planting trees is one of the best things you can do for the environment. Follow for more amazing facts!"
        
        voice_data = generate_voice_from_script(test_script, voice_type='female')
        print("\nVoice Generation Test Result:")
        print(f"  Script: {voice_data['script'][:80]}...")
        print(f"  Audio: {voice_data['audio_path']}")
        print(f"  Voice Type: {voice_data['voice_type']}")
        
        # Validate
        is_valid = validate_audio_file(voice_data['audio_path'])
        print(f"  Valid: {is_valid}")
        
        # Get duration
        duration = get_voice_duration(voice_data['audio_path'])
        if duration:
            print(f"  Duration: {duration:.2f}s")
    
    except Exception as e:
        print(f"Error during test: {e}")
