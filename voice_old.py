"""
Voice Generation Module for AI Reel Automation.
Generates text-to-speech audio using Google Text-to-Speech (gTTS).
"""

import os
import random
from gtts import gTTS
from utils import logger, ensure_directories, read_topics, sanitize_filename, get_output_filename


# ==================== SCRIPT TEMPLATES ====================
SCRIPT_TEMPLATES = [
    "{topic}. This is an amazing fact that everyone should know. Share this with your friends!",
    "{topic}. Did you know this? Learn more interesting facts by following us!",
    "{topic}. Here's something interesting for you. Don't forget to like and share!",
    "{topic}. This will blow your mind! Tag someone who needs to know this.",
    "{topic}. Facts like these are rare! Save this for later and share with others.",
    "{topic}. This is fascinating! Make sure to subscribe for more amazing content.",
]


# ==================== VOICE GENERATION ====================
def generate_voice_from_topic(
    topic=None,
    topics_file="topics.txt",
    language='en',
    audio_dir="audio",
    audio_speed=1.0
):
    """
    Generate voice audio from a topic.
    
    Args:
        topic (str): Specific topic to use. If None, random topic is selected.
        topics_file (str): Path to topics file
        language (str): Language code (default: 'en' for English)
        audio_dir (str): Directory to save audio
        audio_speed (float): Speech speed (1.0 is normal)
        
    Returns:
        dict: Dictionary with audio path, topic, and script text
        Example: {
            'audio_path': 'audio/voice_20240101_120000.mp3',
            'topic': 'Save environment',
            'script': 'Save environment. This is an amazing fact...'
        }
    """
    try:
        logger.info("=" * 50)
        logger.info("STARTING VOICE GENERATION")
        logger.info("=" * 50)
        
        # Ensure audio directory exists
        ensure_directories()
        
        # Select topic if not provided
        if topic is None:
            topics = read_topics(topics_file)
            topic = random.choice(topics)
            logger.info(f"Selected random topic: {topic}")
        else:
            logger.info(f"Using provided topic: {topic}")
        
        # Generate script
        script_template = random.choice(SCRIPT_TEMPLATES)
        script = script_template.format(topic=topic)
        logger.info(f"Generated script: {script[:50]}...")
        
        # Create TTS object
        logger.info(f"Converting text to speech (language: {language})...")
        tts = gTTS(
            text=script,
            lang=language,
            slow=False  # Set to True for slower speech if needed
        )
        
        # Generate output filename
        filename = f"voice_{get_output_filename('').replace('.', '')}.mp3"
        audio_path = os.path.join(audio_dir, filename)
        
        # Save audio
        tts.save(audio_path)
        logger.info(f"[OK] Voice saved: {audio_path}")
        
        # Verify file was created
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file was not created: {audio_path}")
        
        file_size = os.path.getsize(audio_path) / 1024  # Size in KB
        logger.info(f"[OK] Audio file size: {file_size:.2f} KB")
        
        result = {
            'audio_path': audio_path,
            'topic': topic,
            'script': script,
            'language': language
        }
        
        logger.info("=" * 50)
        logger.info("VOICE GENERATION COMPLETED [OK]")
        logger.info("=" * 50)
        
        return result
    
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise
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
        
        # Check file size (minimum 10 KB for valid audio)
        file_size = os.path.getsize(audio_path)
        if file_size < 10240:
            logger.error(f"Audio file too small ({file_size} bytes): {audio_path}")
            return False
        
        # Try to open with moviepy
        from moviepy.audio.io.AudioFileClip import AudioFileClip
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        audio.close()
        
        if duration <= 0:
            logger.error(f"Invalid audio duration: {duration}")
            return False
        
        logger.info(f"[OK] Audio validated: {duration:.2f}s, {file_size} bytes")
        return True
    
    except Exception as e:
        logger.error(f"Audio validation error: {e}")
        return False


# ==================== BATCH VOICE GENERATION ====================
def generate_multiple_voices(count=5, topics_file="topics.txt", audio_dir="audio"):
    """
    Generate multiple voice files for batch processing.
    
    Args:
        count (int): Number of voices to generate
        topics_file (str): Path to topics file
        audio_dir (str): Directory to save audio
        
    Returns:
        list: List of dictionaries with voice data
    """
    try:
        voices = []
        topics = read_topics(topics_file)
        
        for i in range(count):
            logger.info(f"\nGenerating voice {i+1}/{count}...")
            voice_data = generate_voice_from_topic(
                topic=random.choice(topics),
                language='en',
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
        voice_data = generate_voice_from_topic()
        print("\nVoice Generation Test Result:")
        print(f"  Topic: {voice_data['topic']}")
        print(f"  Script: {voice_data['script'][:80]}...")
        print(f"  Audio: {voice_data['audio_path']}")
        
        # Validate
        is_valid = validate_audio_file(voice_data['audio_path'])
        print(f"  Valid: {is_valid}")
        
        # Get duration
        duration = get_voice_duration(voice_data['audio_path'])
        print(f"  Duration: {duration:.2f}s")
    
    except Exception as e:
        print(f"Error during test: {e}")