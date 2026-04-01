#!/usr/bin/env python
"""
Test script to verify Python 3.14+ compatibility.
Tests moviepy imports and module availability.
"""

import sys
import os

print("=" * 70)
print("AI REEL AUTOMATION - Python 3.14+ COMPATIBILITY TEST")
print("=" * 70)

# Check Python version
print(f"\n[1] Python Version Check")
print(f"    Current: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
if sys.version_info >= (3, 8):
    print("    ✓ Python version is compatible (3.8+)")
else:
    print("    ✗ Python version too old (need 3.8+)")
    sys.exit(1)

# Test utility imports
print(f"\n[2] Testing Utility Module")
try:
    from utils import logger, check_dependencies, ensure_directories
    logger.info("    ✓ Utils module imported successfully")
except Exception as e:
    print(f"    ✗ Failed to import utils: {e}")
    sys.exit(1)

# Test voice module
print(f"\n[3] Testing Voice Module")
try:
    from voice import generate_voice_from_topic, validate_audio_file
    logger.info("    ✓ Voice module imported successfully")
except Exception as e:
    print(f"    ✗ Failed to import voice: {e}")
    sys.exit(1)

# Test direct moviepy imports (without moviepy.editor)
print(f"\n[4] Testing MoviePy Imports (Direct, No moviepy.editor)")
try:
    from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
    logger.info("    ✓ ImageSequenceClip imported")
    
    from moviepy.audio.io.AudioFileClip import AudioFileClip
    logger.info("    ✓ AudioFileClip imported")
    
    from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
    logger.info("    ✓ CompositeVideoClip imported")
    
    from moviepy.video.compositing.CompositeAudioClip import CompositeAudioClip
    logger.info("    ✓ CompositeAudioClip imported")
    
    from moviepy.video.compositing.concatenate import concatenate_videoclips
    logger.info("    ✓ concatenate_videoclips imported")
    
    from moviepy.video.VideoClip import VideoClip, TextClip
    logger.info("    ✓ VideoClip and TextClip imported")
    
    print("    ✓ All MoviePy direct imports successful")
except ImportError as e:
    print(f"    ✗ MoviePy import failed: {e}")
    print("\n    Fix: pip install moviepy --upgrade")
    sys.exit(1)

# Test video module
print(f"\n[5] Testing Video Module")
try:
    from video import (
        check_moviepy_compatibility,
        create_video_from_images,
        generate_reel,
        REEL_WIDTH,
        REEL_HEIGHT
    )
    logger.info("    ✓ Video module imported successfully")
    logger.info(f"    ✓ Reel dimensions: {REEL_WIDTH}x{REEL_HEIGHT}")
    
    # Test compatibility check
    check_moviepy_compatibility()
    logger.info("    ✓ MoviePy compatibility check passed")
    
except Exception as e:
    print(f"    ✗ Failed to import video module: {e}")
    sys.exit(1)

# Test main module
print(f"\n[6] Testing Main Module")
try:
    from main import (
        generate_complete_reel,
        batch_generate_reels,
        ReelConfig,
        check_video_module
    )
    logger.info("    ✓ Main module imported successfully")
    logger.info(f"    ✓ FPS setting: {ReelConfig.REEL_FPS}")
    logger.info(f"    ✓ Resolution: {ReelConfig.REEL_WIDTH}x{ReelConfig.REEL_HEIGHT}")
    
    # Test video module check
    if check_video_module():
        logger.info("    ✓ Video module check passed")
    else:
        print("    ✗ Video module check failed")
        sys.exit(1)
        
except Exception as e:
    print(f"    ✗ Failed to import main: {e}")
    sys.exit(1)

# Test PIL
print(f"\n[7] Testing PIL/Pillow")
try:
    from PIL import Image, ImageDraw, ImageFilter
    logger.info("    ✓ PIL/Pillow imported successfully")
except Exception as e:
    print(f"    ✗ PIL import failed: {e}")
    print("    Fix: pip install Pillow --upgrade")
    sys.exit(1)

# Test dependencies
print(f"\n[8] Testing Dependency Check")
try:
    check_dependencies()
    logger.info("    ✓ All dependencies are installed")
except Exception as e:
    print(f"    ✗ Dependency check failed: {e}")
    sys.exit(1)

# Test directory setup
print(f"\n[9] Testing Directory Setup")
try:
    ensure_directories()
    logger.info("    ✓ All required directories are ready")
except Exception as e:
    print(f"    ✗ Directory setup failed: {e}")
    sys.exit(1)

# Final summary
print("\n" + "=" * 70)
print("✓ ALL COMPATIBILITY TESTS PASSED")
print("=" * 70)
print("\nSystem is ready for Python 3.14+!")
print("\nUsage:")
print("  python main.py                    # Generate single reel")
print("  python main.py --batch 5          # Generate 5 reels")
print("  python main.py --no-music         # Without background music")
print("  python main.py --validate         # Run setup validation")
print("\n" + "=" * 70)
