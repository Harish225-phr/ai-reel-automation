#!/usr/bin/env python
"""
ULTRA-FAST reel generation - Minimal effects, speeds up encoding dramatically
TIP: Use this for quick iterations during development
"""

import time
import config
from datetime import datetime
from main import generate_prompt_driven_reel
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

# Save current settings
original_zoom = config.ENABLE_ZOOM
original_crossfade = config.ENABLE_CROSSFADE
original_fps = config.VIDEO_FPS
original_preset = config.ENCODING_PRESET

# ULTRA-FAST MODE (2-3x faster than normal)
config.ENABLE_ZOOM = False
config.ENABLE_CROSSFADE = False  # Skip transitions
config.VIDEO_FPS = 20             # Reduced FPS
config.ENCODING_PRESET = 'ultrafast'

print("\n" + "="*70)
print("⚡ ULTRA-FAST REEL GENERATION (SPEED PRIORITY)")
print("="*70)
print(f"Start Time: {datetime.now().strftime('%H:%M:%S')}")
print(f"⚙️  Settings: ULTRAFAST encoding, 20 FPS, NO zoom, NO crossfade")
print("="*70 + "\n")

# Prompt
prompt = """Topic: Daily temple benefits
Style: spiritual motivational
Voice: Hindi male
Mood: emotional
Music: calm devotional
Video style: temple + sunrise + meditation"""

print(f"Generating reel...\n")

start_total = time.time()

try:
    output_path = generate_prompt_driven_reel(prompt)
    
    total_time = time.time() - start_total
    
    print("\n" + "="*70)
    print(f"✅ REEL GENERATED!")
    print("="*70)
    print(f"Output: {output_path}")
    print(f"\n⏱️  TOTAL TIME: {total_time:.1f} seconds ({total_time/60:.2f} minutes)")
    print(f"📊 Status: {'⚡ ULTRA-FAST' if total_time < 90 else '⚡ FAST' if total_time < 120 else 'NORMAL' if total_time < 180 else 'SLOW'}")
    print("="*70 + "\n")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}\n")
    import traceback
    traceback.print_exc()

finally:
    # Restore settings
    config.ENABLE_ZOOM = original_zoom
    config.ENABLE_CROSSFADE = original_crossfade
    config.VIDEO_FPS = original_fps
    config.ENCODING_PRESET = original_preset
