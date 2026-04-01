#!/usr/bin/env python3
"""
Professional AI Reel Generator - Complete Orchestrator
Generates Instagram reels with:
- HuggingFace AI scripts (non-repetitive, professional)
- Professional subtitles with formatting
- Hook and CTA overlays
- Cinematic video effects
- Background music from Pixabay
- Hindi and English support
- Voice synthesis with Edge TTS

Usage:
    python main.py "Create a Hindi motivational reel about benefits of daily temple visit"
    python main.py "Generate English spiritual reel about meditation with cinematic music"
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path
import json
import re

# Engines
from script_engine import ScriptEngine
from music_engine import MusicEngine
from voice_engine import VoiceEngine
from video_engine import VideoEngine
from prompt_parser import PromptParser
from utils import logger

# ============================================================================
# LOGGING SETUP
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ============================================================================
# CONFIGURATION
# ============================================================================
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')
PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY', '')

CONFIG = {
    'output_dir': 'output',
    'audio_dir': 'audio',
    'music_dir': 'music',
    'temp_dir': 'temp_subtitles',
    'video_width': 1080,
    'video_height': 1920,
    'video_fps': 30,
    'voice_rate': 'normal',
    'music_volume': 0.12,
}

# ============================================================================
# PROMPT PARSER
# ============================================================================
class ReelPromptParser:
    """Parse natural language prompt to reel parameters."""
    
    @staticmethod
    def parse(prompt: str) -> dict:
        """
        Parse prompt to extract parameters.
        
        Args:
            prompt (str): Natural language description
            
        Returns:
            dict: {keyword, language, mood, music_type, voice_type}
        """
        
        logger.info(f"\n[PARSE] Analyzing prompt: {prompt[:100]}...")
        
        # Default values
        result = {
            'keyword': '',
            'language': 'english',
            'mood': 'motivational',
            'music_type': 'cinematic',
            'voice_type': 'male',
        }
        
        prompt_lower = prompt.lower()
        
        # Detect language
        hindi_keywords = [
            'hindi', 'हिंदी', 'भारत', 'देशी', 'yoga', 'temple', 'meditation',
            'आपक', 'करीं', 'कहनी', 'बताता', 'फायदे', 'लिए', 'कार्य'
        ]
        
        if any(keyword in prompt_lower for keyword in hindi_keywords) or \
           any(ord(char) > 2304 and ord(char) < 2432 for char in prompt):
            result['language'] = 'hindi'
            logger.info("[PARSE] Detected language: HINDI")
        else:
            result['language'] = 'english'
            logger.info("[PARSE] Detected language: ENGLISH")
        
        # Extract main keyword/topic
        keyword_patterns = [
            r'about\s+([a-z\s\-]+?)(?:\s+with|\s+benefits|$)',
            r'reel\s+about\s+([a-z\s\-]+?)(?:\s+with|$)',
            r'create\s+[a-z\s\-]*?\s+about\s+([a-z\s\-]+?)(?:\s+with|$)',
            r'generate\s+[a-z\s\-]*?\s+about\s+([a-z\s\-]+?)(?:\s+with|$)',
            r'topic[:=]\s*([a-z\s\-]+?)(?:\s+with|$)',
        ]
        
        for pattern in keyword_patterns:
            match = re.search(pattern, prompt_lower)
            if match:
                keyword = match.group(1).strip()
                # Filter out unwanted words
                if keyword and keyword not in ['a', 'an', 'the'] and len(keyword) > 2:
                    result['keyword'] = keyword
                    break
        
        if not result['keyword']:
            result['keyword'] = 'inspiring content'
        
        logger.info(f"[PARSE] Keyword: {result['keyword']}")
        
        # Detect mood
        mood_keywords = {
            'motivational': ['motivat', 'inspir', 'empower', 'success'],
            'emotional': ['emotional', 'touching', 'heart', 'feel'],
            'spiritual': ['spiritual', 'divine', 'sacred', 'meditation', 'temple'],
            'educational': ['educat', 'learn', 'understand', 'knowledge'],
            'funny': ['funny', 'humor', 'laugh', 'hilarious'],
        }
        
        for mood, keywords in mood_keywords.items():
            if any(kw in prompt_lower for kw in keywords):
                result['mood'] = mood
                break
        
        logger.info(f"[PARSE] Mood: {result['mood']}")
        
        # Detect music type
        music_keywords = {
            'calm': ['calm', 'peaceful', 'quiet', 'gentle'],
            'spiritual': ['spiritual', 'devotional', 'sacred'],
            'motivational': ['motivat', 'inspir', 'powerful'],
            'energetic': ['energetic', 'dynamic', 'upbeat', 'active'],
            'cinematic': ['cinematic', 'epic', 'dramatic'],
        }
        
        result['music_type'] = 'cinematic'
        for music_type, keywords in music_keywords.items():
            if any(kw in prompt_lower for kw in keywords):
                result['music_type'] = music_type
                break
        
        logger.info(f"[PARSE] Music type: {result['music_type']}")
        
        # Detect voice gender
        if 'female' in prompt_lower or 'woman' in prompt_lower:
            result['voice_type'] = 'female'
        else:
            result['voice_type'] = 'male'
        
        logger.info(f"[PARSE] Voice: {result['voice_type']}")
        
        return result


# ============================================================================
# VIDEO FETCHER (Pexels)
# ============================================================================
def fetch_videos_pexels(keyword: str, count: int = 10) -> list:
    """Fetch videos from Pexels."""
    
    try:
        from media_fetcher import PexelsMediaFetcher
        
        logger.info(f"[VIDEO_FETCH] Searching Pexels: {keyword}")
        fetcher = PexelsMediaFetcher(os.getenv('PEXELS_API_KEY', ''))
        videos = fetcher.search_and_download(
            keyword=keyword,
            count=count
        )
        
        if videos:
            logger.info(f"[VIDEO_FETCH] ✓ Found {len(videos)} videos")
            return videos
        else:
            logger.warning("[VIDEO_FETCH] No videos found")
            return []
            
    except Exception as e:
        logger.error(f"[VIDEO_FETCH] Error: {e}")
        return []


# ============================================================================
# MAIN PIPELINE
# ============================================================================
def generate_reel(prompt: str) -> str:
    """
    Generate complete Instagram reel from natural language prompt.
    
    Args:
        prompt (str): Natural language description
        
    Returns:
        str: Path to generated reel or empty string
    """
    
    try:
        logger.info("\n" + "="*80)
        logger.info("🚀 AI REEL GENERATOR - PROFESSIONAL PIPELINE")
        logger.info("="*80)
        
        # ====================================================================
        # STEP 1: PARSE PROMPT
        # ====================================================================
        logger.info("\n[STEP 1/6] PARSING PROMPT")
        logger.info("="*80)
        
        params = ReelPromptParser.parse(prompt)
        keyword = params['keyword']
        language = params['language']
        mood = params['mood']
        music_type = params['music_type']
        voice_type = params['voice_type']
        
        logger.info(f"[PARAM] Keyword: {keyword}")
        logger.info(f"[PARAM] Language: {language}")
        logger.info(f"[PARAM] Mood: {mood}")
        logger.info(f"[PARAM] Music: {music_type}")
        logger.info(f"[PARAM] Voice: {voice_type}")
        
        # ====================================================================
        # STEP 2: GENERATE SCRIPT (HUGGINGFACE AI)
        # ====================================================================
        logger.info("\n[STEP 2/6] GENERATING AI SCRIPT")
        logger.info("="*80)
        
        script_engine = ScriptEngine()
        full_script, script_sentences = script_engine.generate(
            keyword=keyword,
            language=language
        )
        
        logger.info(f"[SCRIPT] Generated {len(script_sentences)} sentences:")
        for i, sent in enumerate(script_sentences, 1):
            logger.info(f"  {i}. {sent[:70]}...")
        
        # ====================================================================
        # STEP 3: FETCH VIDEO CLIPS
        # ====================================================================
        logger.info("\n[STEP 3/6] FETCHING VIDEO CLIPS")
        logger.info("="*80)
        
        video_clips = fetch_videos_pexels(keyword, count=10)
        
        if len(video_clips) < 3:
            logger.error("[ERROR] Not enough videos fetched")
            logger.info("[FALLBACK] Attempting alternative search")
            video_clips = fetch_videos_pexels(f"{mood} {keyword}", count=10)
        
        if len(video_clips) < 3:
            logger.error("[CRITICAL] Cannot proceed without videos")
            return ""
        
        logger.info(f"[VIDEO] ✓ {len(video_clips)} clips available")
        
        # ====================================================================
        # STEP 4: GENERATE VOICE AUDIO
        # ====================================================================
        logger.info("\n[STEP 4/6] GENERATING VOICE AUDIO")
        logger.info("="*80)
        
        voice_engine = VoiceEngine(CONFIG['audio_dir'])
        audio_filename = f"voice_{language}_{voice_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        audio_path = voice_engine.generate(
            script=full_script,
            language=language,
            gender=voice_type,
            rate='normal',
            output_filename=audio_filename
        )
        
        if not audio_path:
            logger.error("[ERROR] Voice generation failed")
            return ""
        
        logger.info(f"[VOICE] ✓ Audio generated: {audio_filename}")
        
        # ====================================================================
        # STEP 5: FETCH BACKGROUND MUSIC
        # ====================================================================
        logger.info("\n[STEP 5/6] FETCHING BACKGROUND MUSIC")
        logger.info("="*80)
        
        music_engine = MusicEngine(api_key=PIXABAY_API_KEY)
        music_path = music_engine.fetch(music_type=music_type, duration=30)
        
        if music_path:
            logger.info(f"[MUSIC] ✓ Music acquired: {os.path.basename(music_path)}")
        else:
            logger.warning("[MUSIC] No music available - will use voice only")
        
        # ====================================================================
        # STEP 6: CREATE PROFESSIONAL REEL
        # ====================================================================
        logger.info("\n[STEP 6/6] CREATING PROFESSIONAL REEL")
        logger.info("="*80)
        
        video_engine = VideoEngine(CONFIG['output_dir'])
        
        output_filename = f"reel_{language}_{keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        
        output_path = video_engine.create_reel(
            video_clips=video_clips,
            audio_path=audio_path,
            music_path=music_path,
            script_sentences=script_sentences,
            keyword=keyword,
            language=language,
            output_filename=output_filename
        )
        
        # ====================================================================
        # FINAL RESULTS
        # ====================================================================
        if output_path and os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / (1024 * 1024)
            
            logger.info("\n" + "="*80)
            logger.info("✅ REEL GENERATION COMPLETE!")
            logger.info("="*80)
            logger.info(f"[OUTPUT] File: {output_filename}")
            logger.info(f"[OUTPUT] Size: {file_size:.1f} MB")
            logger.info(f"[OUTPUT] Path: {output_path}")
            logger.info(f"[DEBUG] Script sentences: {len(script_sentences)}")
            logger.info(f"[DEBUG] Video clips used: {len(video_clips)}")
            logger.info(f"[DEBUG] Music: {'Yes' if music_path else 'No'}")
            logger.info(f"[DEBUG] Language: {language}")
            logger.info(f"[DEBUG] Voice: {voice_type}")
            logger.info("="*80)
            
            return output_path
        else:
            logger.error("\n" + "="*80)
            logger.error("❌ REEL GENERATION FAILED")
            logger.error("="*80)
            return ""
        
    except Exception as e:
        logger.error(f"\n[CRITICAL ERROR] {e}")
        import traceback
        logger.error(traceback.format_exc())
        return ""


# ============================================================================
# CLI INTERFACE
# ============================================================================
def main():
    """Main entry point."""
    
    if len(sys.argv) < 2:
        print("\n" + "="*80)
        print("AI REEL GENERATOR - Usage Examples")
        print("="*80)
        print("\nBasic usage:")
        print('  python main.py "Create a motivational reel about fitness"')
        print('  python main.py "Generate Hindi reel about temple benefits"')
        print('  python main.py "Create a spiritual reel about meditation with calm music"')
        print("\nThe system will automatically:")
        print("  ✓ Detect language (English/Hindi)")
        print("  ✓ Parse mood and music style")
        print("  ✓ Generate AI script (non-repetitive)")
        print("  ✓ Fetch relevant stock videos")
        print("  ✓ Generate voice with selected language")
        print("  ✓ Download background music")
        print("  ✓ Create professional reel with subtitles")
        print("  ✓ Add hook and CTA overlays")
        print("  ✓ Mix audio and export")
        print("\n" + "="*80)
        return
    
    prompt = ' '.join(sys.argv[1:])
    
    reel_path = generate_reel(prompt)
    
    if reel_path:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
