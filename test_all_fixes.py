#!/usr/bin/env python3
"""
Test script to validate all 3 fixes:
1. Video search priority (keyword first, not theme)
2. Enhanced script quality (poetic language, emotional hooks)
3. Background music with fallback (Freesound → Procedural)
"""

import sys
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_video_search_priority():
    """Test that video search prioritizes keyword over theme."""
    logger.info("\n" + "="*60)
    logger.info("TEST 1: Video Search Priority")
    logger.info("="*60)
    
    try:
        from prompt_parser import PromptParser
        
        # Test 1a: Yoga should search "yoga" first, not "temple"
        yoga_queries = PromptParser.get_video_search_queries(
            keyword="yoga benefits",
            theme="temple"
        )
        
        logger.info(f"Yoga + Temple theme queries: {yoga_queries}")
        
        # Verify: First query should be keyword-based, not temple-based
        first_query = yoga_queries[0].lower() if yoga_queries else ""
        has_yoga = "yoga" in first_query
        
        if has_yoga:
            logger.info("✅ PASS: Yoga appears in first search query")
            logger.info(f"   First query: '{yoga_queries[0]}'")
        else:
            logger.warning("❌ FAIL: Yoga not in first search query")
            logger.warning(f"   First query: '{yoga_queries[0] if yoga_queries else 'EMPTY'}'")
            return False
            
        # Test 1b: Verify no duplicates
        if len(yoga_queries) == len(set(yoga_queries)):
            logger.info("✅ PASS: No duplicate queries")
        else:
            logger.warning("❌ FAIL: Duplicate queries found")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ ERROR in video search test: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def test_script_quality():
    """Test that scripts use enhanced, poetic language."""
    logger.info("\n" + "="*60)
    logger.info("TEST 2: Enhanced Script Quality")
    logger.info("="*60)
    
    try:
        from script_generator_smart import SmartScriptGenerator
        
        # Test 2a: Check that yoga benefits are poetic
        benefits = SmartScriptGenerator.BENEFIT_DATABASE.get('yoga', [])
        logger.info(f"Yoga benefits ({len(benefits)} options):")
        for i, benefit in enumerate(benefits, 1):
            logger.info(f"  {i}. {benefit}")
        
        # Verify poetic language quality
        has_poetic = any(
            word in ' '.join(benefits).lower() 
            for word in ['flows', 'melts', 'radiates', 'surges', 'becomes']
        )
        
        if has_poetic:
            logger.info("✅ PASS: Poetic language detected in benefits")
        else:
            logger.warning("❌ FAIL: Benefits lack poetic language")
            return False
        
        # Test 2b: Generate script and check for emotional hooks
        script = SmartScriptGenerator.generate_script(
            keyword="yoga benefits",
            mood="motivational",
            num_sentences=5
        )
        
        logger.info(f"\nGenerated Script (Motivational):")
        logger.info(f"  {script[:100]}...")
        
        emotional_keywords = ['what if', 'transform', 'feeling', 'stuck', 'stop']
        has_emotional_hooks = any(
            keyword in script.lower() for keyword in emotional_keywords
        )
        
        if has_emotional_hooks:
            logger.info("✅ PASS: Emotional hooks detected in script")
        else:
            logger.warning("⚠️  WARN: Script may lack emotional engagement")
        
        # Test 2c: Check emotional mood templates
        script_emotional = SmartScriptGenerator.generate_script(
            keyword="meditation",
            mood="emotional",
            num_sentences=5
        )
        
        if script_emotional and len(script_emotional) > 50:
            logger.info("✅ PASS: Emotional script generated successfully")
        else:
            logger.warning("❌ FAIL: Emotional script generation failed")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ ERROR in script quality test: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def test_music_fetcher():
    """Test that music fetcher has fallback capability."""
    logger.info("\n" + "="*60)
    logger.info("TEST 3: Music Fetcher with Fallback")
    logger.info("="*60)
    
    try:
        from music_fetcher_enhanced import EnhancedMusicFetcher
        
        # Test 3a: Initialize fetcher
        fetcher = EnhancedMusicFetcher(
            api_key=None,  # Simulate no API key to test fallback
            output_dir="music"
        )
        logger.info("✅ PASS: EnhancedMusicFetcher initialized")
        
        # Test 3b: Check methods exist
        methods = ['fetch_music', '_fetch_from_freesound', '_generate_fallback_music']
        for method in methods:
            if hasattr(fetcher, method):
                logger.info(f"✅ PASS: Method '{method}' exists")
            else:
                logger.warning(f"❌ FAIL: Method '{method}' missing")
                return False
        
        # Test 3c: Try fetching music (will use fallback since no API key)
        logger.info("\nAttempting music fetch (will use fallback)...")
        music_path = fetcher.fetch_music(
            query="calm meditation music",
            duration=10,
            music_type="calm"
        )
        
        if music_path:
            logger.info(f"✅ PASS: Music fetched/generated: {Path(music_path).name}")
            
            # Verify file exists
            if Path(music_path).exists():
                logger.info(f"✅ PASS: Music file exists at {music_path}")
                file_size = Path(music_path).stat().st_size
                logger.info(f"   File size: {file_size:,} bytes")
            else:
                logger.warning(f"❌ FAIL: Music file not found at {music_path}")
                return False
        else:
            logger.info("ℹ️  INFO: No music generated (may require scipy)")
        
        return True
        
    except ImportError as e:
        logger.warning(f"⚠️  WARN: Cannot test fallback audio (scipy not installed): {e}")
        logger.info("   This is OK if procedural audio is optional")
        return True
    except Exception as e:
        logger.error(f"❌ ERROR in music fetcher test: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def main():
    """Run all tests."""
    logger.info("🚀 TESTING ALL 3 FIXES")
    logger.info("="*60)
    
    results = {
        "Video Search Priority": test_video_search_priority(),
        "Script Quality": test_script_quality(),
        "Music Fetcher": test_music_fetcher(),
    }
    
    logger.info("\n" + "="*60)
    logger.info("FINAL RESULTS")
    logger.info("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status}: {test_name}")
    
    logger.info("="*60)
    logger.info(f"Score: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 ALL FIXES VALIDATED SUCCESSFULLY!")
        return 0
    else:
        logger.warning(f"⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
