"""
STABLE REEL GENERATOR - Reliability First Approach
Uses fixed scripts, enforced validation, comprehensive debug output
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import traceback

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from script_engine_stable import StableScriptEngine
from video_engine_stable import StableVideoEngine
from voice_engine_stable import StableVoiceEngine
from music_engine import MusicEngine
from video_fetcher import VideoFetcher
import config


def main():
    """Generate reel using stable components"""
    
    print("\n" + "="*70)
    print("STABLE REEL GENERATOR - Reliability First")
    print("="*70)
    
    if len(sys.argv) < 2:
        print("[ERROR] Usage: python main_stable.py 'Your reel prompt'")
        sys.exit(1)
    
    prompt = ' '.join(sys.argv[1:])
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    try:
        # ===================================================================
        # STEP 1: PARSE PROMPT (Simple, reliable)
        # ===================================================================
        print("\n[STEP 1] Parsing prompt...")
        
        keyword = prompt.replace('create', '').replace('make', '').strip()
        if len(keyword) < 3:
            keyword = 'motivation'
        keyword = keyword[:50]  # Limit length
        
        language = 'hi' if any(ord(char) > 2400 for char in prompt) else 'en'
        
        print(f"[DEBUG] Keyword: {keyword}")
        print(f"[DEBUG] Language: {language}")
        print(f"[PARSE] OK Prompt parsed")
        
        # ===================================================================
        # STEP 2: GENERATE FIXED SCRIPT
        # ===================================================================
        print("\n[STEP 2] Generating fixed-structure script...")
        
        script_result = StableScriptEngine.generate(
            keyword=keyword,
            language=language
        )
        script = script_result['script']
        
        print(f"[DEBUG] Word count: {script_result['word_count']}")
        print(f"[DEBUG] Duration estimate: {script_result['duration_estimate']:.1f}s")
        print(f"[DEBUG] Structure: Hook + 3 Benefits + CTA")
        for section, text in script_result['structure']:
            print(f"[DEBUG]   {section}: {text[:50]}...")
        print(f"[SCRIPT] OK Script generated ({script_result['word_count']} words)")
        
        # ===================================================================
        # STEP 3: FETCH VIDEO CLIPS
        # ===================================================================
        print("\n[STEP 3] Fetching video clips...")
        
        try:
            videos = VideoFetcher.fetch_pexels_videos(
                keyword=keyword,
                count=config.PEXELS_VIDEO_COUNT
            )
            print(f"[DEBUG] Fetched {len(videos)} video clips")
        except Exception as e:
            print(f"[WARNING] ⚠ Video fetch failed: {e}")
            videos = []
        
        if not videos:
            print(f"[ERROR] ✗ No videos fetched!")
            print(f"[ERROR] Cannot proceed - minimum 3 clips required")
            print(f"[ERROR] STOPPING GENERATION")
            sys.exit(1)
        
        print(f"[CLIPS] OK {len(videos)} clips fetched")
        for i, vid_path in enumerate(videos, 1):
            print(f"[DEBUG]   Clip {i}: {Path(vid_path).name if vid_path else 'INVALID'}")
        
        # ===================================================================
        # STEP 4: GENERATE VOICE (Edge TTS only)
        # ===================================================================
        print("\n[STEP 4] Generating voice narration (Edge TTS)...")
        
        try:
            voice_engine = StableVoiceEngine()
            
            audio_file = voice_engine.generate(
                script=script,
                language=language,
                gender='female'
            )
            
            if not audio_file or not Path(audio_file).exists():
                raise FileNotFoundError(f"Voice audio not created")
            
            audio_duration = 0
            try:
                from moviepy.editor import AudioFileClip
                audio_clip = AudioFileClip(audio_file)
                audio_duration = audio_clip.duration
                audio_clip.close()
            except:
                audio_duration = script_result['duration_estimate']
            
            print(f"[DEBUG] Voice file: {Path(audio_file).name}")
            print(f"[DEBUG] Duration: {audio_duration:.2f}s")
            print(f"[VOICE] OK Voice generated")
        except Exception as e:
            print(f"[ERROR] ✗ Voice generation failed: {e}")
            print(f"[ERROR] STOPPING GENERATION - Cannot proceed without voice")
            raise
        
        # ===================================================================
        # STEP 5: GET MUSIC (with default fallback)
        # ===================================================================
        print("\n[STEP 5] Setting up background music...")
        
        music_file = None
        try:
            music_engine = MusicEngine()
            music_file = music_engine.fetch(
                music_type='motivational',
                duration=int(audio_duration) + 5
            )
            if music_file and Path(music_file).exists():
                print(f"[DEBUG] Music file: {Path(music_file).name}")
                print(f"[MUSIC] OK Music ready")
            else:
                print(f"[WARNING] ⚠ Music API failed, will use default")
        except Exception as e:
            print(f"[WARNING] ⚠ Music fetch failed: {e}")
            print(f"[WARNING] Will use default music if available")
        
        # ===================================================================
        # STEP 6: COMPOSE VIDEO (Stable Engine)
        # ===================================================================
        print("\n[STEP 6] Composing final reel...")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        language_tag = 'hindi' if language == 'hi' else 'english'
        keyword_slug = keyword.replace(' ', '_').lower()[:20]
        output_file = f"reel_stable_{language_tag}_{keyword_slug}_{timestamp}.mp4"
        
        video_engine = StableVideoEngine(output_dir=output_dir)
        
        output_path = video_engine.create_reel(
            script=script,
            audio_path=audio_file,
            video_paths=videos,
            background_music_path=music_file,
            output_name=output_file,
            keyword=keyword
        )
        
        # ===================================================================
        # SUCCESS
        # ===================================================================
        print("\n" + "="*70)
        print("SUCCESS: REEL GENERATION SUCCESSFUL")
        print("="*70)
        print(f"\n[OUTPUT] Reel created: {output_file}")
        print(f"[OUTPUT] Location: {output_path}")
        print(f"[OUTPUT] Ready for upload!\n")
        
        print(f"[SUCCESS] Reel generated: {output_file}")
        print(f"[SUCCESS] Location: output/{output_file}")
        
        return output_path
    
    except Exception as e:
        print("\n" + "="*70)
        print("FAILED: REEL GENERATION FAILED")
        print("="*70)
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        print(f"\nFull traceback:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
