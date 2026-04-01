#!/usr/bin/env python3
"""
Quick test using fallback templates (no HuggingFace download needed)
Tests 4-step pipeline in ~3-5 minutes
"""

import os
import sys
from pathlib import Path
os.environ['HF_HOME'] = 'D:\\HF_Cache'
os.environ['PIXABAY_API_KEY'] = '55255362-cad7c618b8998f92934f36486'

# Force fallback by making transformers unavailable
sys.modules['transformers'] = None

from script_engine import ScriptEngine
from music_engine import MusicEngine  
from voice_engine import VoiceEngine
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_dummy_video(filename: str):
    """Create a dummy video file for testing."""
    Path("video").mkdir(exist_ok=True)
    filepath = f"video/{filename}"
    # Create a simple MP4-like file (just for testing, not playable)
    with open(filepath, 'wb') as f:
        f.write(b'dummy video content' * 1000)  # ~19KB
    logger.info(f"Created dummy video: {filepath}")
    return filepath

def test_pipeline():
    """Test full pipeline with fallback templates"""
    
    logger.info("=" * 80)
    logger.info("🚀 QUICK TEST - TEMPLATE-BASED (NO HF DOWNLOAD)")
    logger.info("=" * 80)
    
    try:
        # Step 1: Generate script (using fallback templates)
        logger.info("\n[STEP 1/4] GENERATING SCRIPT (FALLBACK)")
        script_engine = ScriptEngine()
        script, sentences = script_engine.generate(
            keyword="yoga benefits",
            language="hindi"
        )
        logger.info(f"✓ Generated {len(sentences)} sentences")
        for i, sent in enumerate(sentences, 1):
            logger.info(f"  {i}. {sent}")
        
        # Step 2: Generate voice
        logger.info("\n[STEP 2/4] GENERATING VOICE (HINDI MALE)")
        voice_engine = VoiceEngine()
        audio_path = voice_engine.generate(
            script=script,
            language="hindi",
            gender="male",
            output_filename="test_voice.mp3"
        )
        if audio_path:
            logger.info(f"✓ Voice generated: {audio_path}")
        else:
            logger.warning("⚠ Voice generation returned None (might need edge_tts)")
            return False
        
        # Step 3: Fetch music
        logger.info("\n[STEP 3/4] FETCHING MUSIC")
        music_engine = MusicEngine()
        music_path = music_engine.fetch(
            music_type="motivational",
            duration=20
        )
        if music_path:
            logger.info(f"✓ Music fetched: {music_path}")
        else:
            logger.warning("⚠ Music fetching returned None (fallback to procedural)")
        
        # Step 4: Verify audio files exist
        logger.info("\n[STEP 4/4] VERIFYING OUTPUTS")
        if audio_path and os.path.exists(audio_path):
            size = os.path.getsize(audio_path)
            logger.info(f"✓ Voice audio exists: {size} bytes")
        
        if music_path and os.path.exists(music_path):
            size = os.path.getsize(music_path)
            logger.info(f"✓ Music file exists: {size} bytes")
        
        logger.info("\n" + "=" * 80)
        logger.info("✅ QUICK TEST COMPLETE - CORE SYSTEMS WORKING")
        logger.info("=" * 80)
        logger.info(f"\nGenerated assets:")
        logger.info(f"  - Script: {len(sentences)} sentences")
        logger.info(f"  - Voice: {audio_path if audio_path else 'FAILED'}")
        logger.info(f"  - Music: {music_path if music_path else 'FALLBACK'}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ TEST FAILED: {e}", exc_info=True)
        return False

if __name__ == "__main__":
    success = test_pipeline()
    sys.exit(0 if success else 1)
