"""
Voice Engine - Generate voice audio using Edge TTS
Supports Hindi and English with emotional variations
"""

import os
import logging
from typing import Optional
from pathlib import Path
import asyncio

logger = logging.getLogger(__name__)

try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    logger.warning("[VOICE] edge_tts not installed")
    HAS_EDGE_TTS = False


class VoiceEngine:
    """Generate voice audio from text using Edge TTS."""
    
    VOICES = {
        'hindi': {
            'male': 'hi-IN-MadhurNeural',
            'female': 'hi-IN-SwaraNeural',
        },
        'english': {
            'male': 'en-US-BrianNeural',
            'female': 'en-US-JessicaNeural',
        }
    }
    
    RATES = {
        'normal': '+0%',
        'slow': '-15%',
        'fast': '+10%',
    }
    
    def __init__(self, output_dir: str = 'audio'):
        """Initialize voice engine."""
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        if not HAS_EDGE_TTS:
            logger.error("[VOICE] edge_tts not available")
        else:
            logger.info("[VOICE] Voice engine initialized")
    
    def generate(
        self,
        script: str,
        language: str = 'english',
        gender: str = 'male',
        rate: str = 'normal',
        output_filename: str = 'voice.mp3'
    ) -> Optional[str]:
        """
        Generate voice audio from script.
        
        Args:
            script: Text to convert to speech
            language: 'english' or 'hindi'
            gender: 'male' or 'female'
            rate: 'slow', 'normal', or 'fast'
            output_filename: Output file name
            
        Returns:
            Path to generated audio file or None
        """
        
        if not HAS_EDGE_TTS:
            logger.error("[VOICE] edge_tts not available. Cannot generate voice.")
            return None
        
        try:
            # Get voice
            voice_lang = self.VOICES.get(language, self.VOICES['english'])
            voice = voice_lang.get(gender, voice_lang['male'])
            
            # Get rate
            rate_value = self.RATES.get(rate, self.RATES['normal'])
            
            logger.info(f"[VOICE] Generating {language} {gender} voice ({rate})")
            logger.info(f"[VOICE] Voice: {voice}, Rate: {rate_value}")
            logger.info(f"[VOICE] Script length: {len(script)} chars")
            
            # Generate async
            output_path = os.path.join(self.output_dir, output_filename)
            
            # Run async function
            asyncio.run(self._generate_async(
                script,
                voice,
                rate_value,
                output_path
            ))
            
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                logger.info(f"[VOICE] ✓ Generated: {output_filename} ({file_size:,} bytes)")
                return output_path
            else:
                logger.error("[VOICE] Audio file not created")
                return None
            
        except Exception as e:
            logger.error(f"[VOICE] Generation failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    async def _generate_async(
        self,
        script: str,
        voice: str,
        rate: str,
        output_path: str
    ):
        """Generate voice async."""
        
        try:
            communicate = edge_tts.Communicate(
                text=script,
                voice=voice,
                rate=rate
            )
            
            await communicate.save(output_path)
            logger.info(f"[VOICE] Audio saved to {output_path}")
            
        except Exception as e:
            logger.error(f"[VOICE] Async generation error: {e}")
            raise
