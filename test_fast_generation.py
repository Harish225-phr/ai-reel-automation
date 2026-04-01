#!/usr/bin/env python
"""
Fast-mode reel generation test - Optimized for speed
Shows timing breakdown for each step
"""

import time
from datetime import datetime
from main import generate_prompt_driven_reel
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

print("\n" + "="*70)
print("🚀 OPTIMIZED REEL GENERATION (FAST MODE)")
print("="*70)
print(f"Start Time: {datetime.now().strftime('%H:%M:%S')}\n")

# Timer dictionary
timings = {}

# Prompt from user
prompt = """Topic: Daily temple benefits
Style: spiritual motivational
Voice: Hindi male
Mood: emotional
Music: calm devotional
Video style: temple + sunrise + meditation"""

print(f"📋 Prompt:\n{prompt}\n")

# Generate reel
start_total = time.time()

try:
    output_path = generate_prompt_driven_reel(prompt)
    
    total_time = time.time() - start_total
    
    print("\n" + "="*70)
    print(f"✅ REEL GENERATED SUCCESSFULLY!")
    print("="*70)
    print(f"Output: {output_path}")
    print(f"\n⏱️  Total Time: {total_time:.1f} seconds ({total_time/60:.2f} minutes)")
    print(f"📊 Performance: {'FAST ⚡' if total_time < 120 else 'NORMAL' if total_time < 180 else 'SLOW'}")
    print("="*70 + "\n")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}\n")
    import traceback
    traceback.print_exc()
