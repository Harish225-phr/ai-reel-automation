"""
AI REEL GENERATOR - TURBO MODE (SUPER FAST!)
Generates reels in 30-60 seconds instead of 5+ minutes
Uses template-based scripts (no HuggingFace model loading)
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from utils import logger
from engine.script_engine import ScriptEngine
from engine.video_engine_pro import VideoEngine
from voice_engine import VoiceEngine
from music_engine import MusicEngine
from video_fetcher import VideoFetcher
import config
import json

# DISABLE HUGGINGFACE - USE TEMPLATES ONLY (FAST!)
os.environ['HAS_HUGGINGFACE'] = 'False'


class ReelPromptParserTurbo:
    """Fast prompt parsing without heavy NLP"""
    
    @staticmethod
    def parse(prompt: str):
        """Parse prompt quickly"""
        # Detect language
        language = 'hi' if any(ord(char) > 2400 for char in prompt) else 'en'
        
        # Extract keyword (first few words)
        words = prompt.split()
        keyword = ' '.join([w for w in words if len(w) > 2][:3])
        
        if not keyword:
            keyword = prompt[:30]
        
        # Detect style
        style = 'motivational'
        if any(word in prompt.lower() for word in ['teach', 'learn', 'how', 'tutorial']):
            style = 'educational'
        elif any(word in prompt.lower() for word in ['funny', 'laugh', 'meme', 'joke']):
            style = 'entertaining'
        elif any(word in prompt.lower() for word in ['trending', 'viral', 'challenge']):
            style = 'trending'
        
        return {
            'original_prompt': prompt,
            'keyword': keyword,
            'language': language,
            'style': style,
            'mood': 'uplifting'
        }


def main():
    """Generate reel - TURBO MODE"""
    
    if len(sys.argv) < 2:
        print("[ERROR] Usage: python main_turbo.py 'Your reel prompt'")
        sys.exit(1)
    
    prompt = ' '.join(sys.argv[1:])
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    try:
        # ===================================================================
        print("[PARSE] Parsing prompt...")
        parsed = ReelPromptParserTurbo.parse(prompt)
        print(f"[PARSE] Keyword: {parsed['keyword']}")
        print(f"[PARSE] Language: {parsed['language']}")
        print(f"[PARSE] Style: {parsed['style']}")
        
        # ===================================================================
        print("[SCRIPT] Generating script (template-based)...")
        script_result = ScriptEngine.generate(
            keyword=parsed['keyword'],
            style=parsed['style'],
            length='long'
        )
        script = script_result['script']
        print(f"[SCRIPT] Generated {len(script)} character script")
        
        # ===================================================================
        print("[CLIPS] Fetching video clips...")
        videos = VideoFetcher.fetch_pexels_videos(
            keyword=parsed['keyword'],
            count=config.PEXELS_VIDEO_COUNT  # Uses config (optimized to 4 not 10)
        )
        print(f"[CLIPS] Downloaded {len(videos)} video clips")
        
        # ===================================================================
        print("[VOICE] Creating voice-over...")
        voice_engine = VoiceEngine()
        audio_file = voice_engine.generate(
            script=script,
            language=parsed['language'],
            gender='male'
        )
        print(f"[VOICE] Voice file: {audio_file}")
        
        # ===================================================================
        print("[MUSIC] Finding background music...")
        music_engine = MusicEngine()
        music_file = music_engine.fetch(
            music_type=parsed['mood'],
            duration=30
        )
        print(f"[MUSIC] Music file: {music_file}")
        
        # ===================================================================
        print("[COMPOSE] Composing final reel...")
        video_engine = VideoEngine()
        
        # Create reel
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        language_tag = 'hindi' if parsed['language'] == 'hi' else 'english'
        keyword_slug = parsed['keyword'].replace(' ', '_').lower()[:20]
        output_file = f"reel_{language_tag}_{keyword_slug}_{timestamp}.mp4"
        
        reel_result = video_engine.create_reel(
            script=script_result['script'],
            audio_path=audio_file,
            video_paths=videos,
            background_music_path=music_file,
            output_name=output_file,
            keyword=parsed['keyword']
        )
        
        print(f"[COMPOSE] Video composed: {output_file}")
        
        # Verify file was created
        output_path = Path(__file__).parent / "output" / output_file
        if not output_path.exists():
            raise FileNotFoundError(f"Video file not created: {output_path}")
        
        file_size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"[COMPOSE] File verified: {output_file} ({file_size_mb:.2f} MB)")

        
        # ===================================================================
        print(f"[SUCCESS] Reel generated: {output_file}")
        print(f"[SUCCESS] Location: output/{output_file}")
        
        return 0
        
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
