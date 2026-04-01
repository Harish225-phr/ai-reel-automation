"""
STABLE VOICE ENGINE - Edge TTS with Fallbacks
Enhanced with retry logic and multiple voice options
"""

import os
import logging
from typing import Optional
from pathlib import Path
import asyncio
import time

logger = logging.getLogger(__name__)

try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    logger.warning("[VOICE] edge_tts not installed")
    HAS_EDGE_TTS = False


class StableVoiceEngine:
    """Reliable voice generation with retries and fallbacks."""
    
    VOICES = {
        'en': {
            'male': ['en-US-BrianNeural', 'en-US-GuyNeural', 'en-GB-RyanNeural'],
            'female': ['en-US-JessicaNeural', 'en-US-AriaNeural', 'en-GB-SoniaNeural'],
        },
        'hi': {
            'male': ['hi-IN-MadhurNeural', 'hi-IN-ManishNeural'],
            'female': ['hi-IN-SwaraNeural', 'hi-IN-GargiBNeural'],
        },
    }
    
    RATES = {
        'normal': '+0%',
        'slow': '-15%',
        'fast': '+10%',
    }
    
    MAX_RETRIES = 3
    RETRY_DELAY = 2  
    
    def __init__(self, output_dir: str = 'audio'):
        """Initialize voice engine."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        if not HAS_EDGE_TTS:
            logger.error("[VOICE] edge_tts not available")
        else:
            logger.info("[VOICE] OK Voice engine initialized")
    
    def generate(
        self,
        script: str,
        language: str = 'en',
        gender: str = 'female',
        rate: str = 'normal',
        output_filename: str = 'voice.mp3'
    ) -> Optional[str]:
        """
        Generate voice audio from script with retries.
        """
        
        if not HAS_EDGE_TTS:
            logger.error("[VOICE] ERROR edge_tts not available")
            return None
        
        if not script or len(script.strip()) == 0:
            logger.error("[VOICE] ERROR Script is empty")
            return None
        
        language = language.lower()
        if language not in ['en', 'hi']:
            language = 'en'
        
        gender = gender.lower()
        if gender not in ['male', 'female']:
            gender = 'female'
        
        output_path = str(self.output_dir / output_filename)
        
        print("[VOICE] Generating voice...")
        print(f"[DEBUG]   Language: {language}")
        print(f"[DEBUG]   Gender: {gender}")
        print(f"[DEBUG]   Script: {len(script)} chars")
        
        voices = self.VOICES.get(language, self.VOICES['en']).get(gender, [])
        
        for voice in voices:
            for attempt in range(1, self.MAX_RETRIES + 1):
                try:
                    print(f"[DEBUG]   Attempt {attempt}/{self.MAX_RETRIES}: {voice}")
                    
                    rate_value = self.RATES.get(rate, '+0%')
                    
                    asyncio.run(self._generate_async(
                        script=script,
                        voice=voice,
                        rate=rate_value,
                        output_path=output_path
                    ))
                    
                    if os.path.exists(output_path):
                        file_size = os.path.getsize(output_path)
                        if file_size > 1000:
                            print(f"[DEBUG]   OK Generated: {file_size:,} bytes")
                            print(f"[VOICE] OK Voice created: {output_filename}")
                            return output_path
                        else:
                            print(f"[DEBUG]   ERROR File too small: {file_size} bytes")
                            os.remove(output_path)
                    
                except Exception as e:
                    error_msg = str(type(e).__name__)
                    print(f"[DEBUG]   ERROR Attempt {attempt}: {error_msg[:50]}")
                    
                    if attempt < self.MAX_RETRIES:
                        print(f"[DEBUG]   Retrying in {self.RETRY_DELAY}s...")
                        time.sleep(self.RETRY_DELAY)
        
        print("[ERROR] ERROR Voice generation failed")
        return None
    
    async def _generate_async(
        self,
        script: str,
        voice: str,
        rate: str,
        output_path: str
    ):
        """Generate voice asynchronously."""
        try:
            communicate = edge_tts.Communicate(
                text=script,
                voice=voice,
                rate=rate
            )
            await communicate.save(output_path)
        except Exception as e:
            raise


if __name__ == '__main__':
    engine = StableVoiceEngine()
    
    test_script = "This is a test script. Hello world!"
    result = engine.generate(
        script=test_script,
        language='en',
        gender='female'
    )
    print("Generated: " + str(result))
