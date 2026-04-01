#!/usr/bin/env python
"""
Direct reel generation for temple benefits - Hindi, emotional, spiritual
"""

from main import generate_prompt_driven_reel
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

prompt = """Topic: Daily temple benefits
Style: spiritual motivational
Voice: Hindi male
Mood: emotional
Music: calm devotional
Video style: temple + sunrise + meditation"""

print("\n" + "="*70)
print("GENERATING YOUR REEL")
print("="*70)
print(f"Prompt:\n{prompt}\n")

result = generate_prompt_driven_reel(prompt=prompt, num_videos=5)

if result['success']:
    print("\n" + "="*70)
    print("REEL SUCCESSFULLY CREATED!")
    print("="*70)
    print(f"\nOutput: {result['output_path']}")
    print(f"Duration: {result['duration']:.1f} seconds")
    print(f"Size: {result['size_mb']:.2f} MB")
    print(f"Language: {result['language']} ({result['voice']})")
    print(f"Mood: {result['mood']}")
    print(f"Music: {result['music_type']}")
    print(f"Videos: {result['videos_used']} clips")
    print(f"Has Background Music: {result['has_music']}")
    print("\nREADY FOR INSTAGRAM REELS, YOUTUBE SHORTS, TIKTOK!")
else:
    print(f"\nERROR: {result.get('error')}")
