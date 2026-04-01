"""
Prompt Parser - Extracts user intent from natural language prompts
Converts natural language into structured reel parameters
"""

import re
from typing import Dict, Tuple


class PromptParser:
    """
    Parses natural language prompts and extracts reel generation parameters.
    
    Example:
        "Create a 25 second Hindi motivational reel about temple benefits 
         with calm music and male voice"
    
    Output:
        {
            'keyword': 'temple benefits',
            'language': 'hindi',
            'voice_type': 'male',
            'mood': 'motivational',
            'music_type': 'calm',
            'video_theme': 'temple',
            'duration': 25,
            'style': 'spiritual'
        }
    """

    # Language patterns
    LANGUAGE_PATTERNS = {
        'hindi': r'\b(hindi|hin)\b',
        'english': r'\b(english|eng|english\s+only|just\s+english)\b'
    }

    # Voice gender patterns
    VOICE_PATTERNS = {
        'male': r'\b(male|man|boy|masculine|guy)\b',
        'female': r'\b(female|woman|girl|feminine|lady)\b'
    }

    # Mood patterns
    MOOD_PATTERNS = {
        'motivational': r'\b(motivational|motivating|inspiring|pump\s+up|energetic|energize)\b',
        'emotional': r'\b(emotional|emotional|touching|heart\s+touching|sad|soothing|calm|peaceful)\b',
        'educational': r'\b(educational|informative|educational|teach|learn|knowledge)\b',
        'spiritual': r'\b(spiritual|spiritual|divine|meditation|meditative|devotional|prayer)\b',
        'funny': r'\b(funny|humorous|comedy|hilarious|laugh)\b'
    }

    # Music type patterns
    MUSIC_PATTERNS = {
        'calm': r'\b(calm|relaxed|peaceful|soothing|soft|gentle|quiet)\b',
        'motivational': r'\b(motivational|inspiring|cinematic|epic|powerful|energetic)\b',
        'spiritual': r'\b(spiritual|meditation|devotional|spiritual|mantra)\b',
        'upbeat': r'\b(upbeat|happy|cheerful|lively|dance)\b'
    }

    # Video theme patterns
    THEME_PATTERNS = {
        'temple': r'\b(temple|shrine|prayer|worship|religious|devotion)\b',
        'nature': r'\b(nature|forest|tree|mountain|river|landscape|green|outdoor)\b',
        'success': r'\b(success|achievement|win|winning|goal|reach)\b',
        'motivation': r'\b(motivation|motivate|inspire|inspiration)\b',
        'fitness': r'\b(fitness|workout|exercise|gym|sport|athletic)\b',
        'meditation': r'\b(meditation|meditate|peaceful|calm|relax)\b',
        'daily_life': r'\b(daily|routine|morning|lifestyle|life)\b'
    }

    # Duration pattern
    DURATION_PATTERN = r'(\d+)\s*(?:second|sec|s|minute|min|m)'

    # Style patterns
    STYLE_PATTERNS = {
        'cinematic': r'\b(cinematic|cinema|film|movie\s+style)\b',
        'fast_paced': r'\b(fast|paced|quick|rapid|high\s+energy)\b',
        'slow': r'\b(slow|slow\s+paced|leisurely)\b',
        'documentary': r'\b(documentary|doc\s+style)\b'
    }

    @staticmethod
    def parse(prompt: str) -> Dict:
        """
        Parse natural language prompt and extract parameters.
        
        Handles both formats:
        1. Natural language: "Create a Hindi motivational reel about temple"
        2. Structured format: "Topic: temple\nStyle: motivational\nVoice: Hindi male"
        
        Args:
            prompt (str): Natural language user prompt OR structured format
            
        Returns:
            dict: Structured parameters for reel generation
        """
        prompt_lower = prompt.lower()
        
        # Check if structured format (contains Topic:, Style:, Voice:, etc.)
        is_structured = 'topic:' in prompt_lower or 'style:' in prompt_lower
        
        if is_structured:
            # Parse structured format
            return PromptParser._parse_structured_format(prompt)
        else:
            # Parse natural language format (existing logic)
            return {
                'keyword': PromptParser._extract_keyword(prompt),
                'language': PromptParser._extract_language(prompt_lower),
                'voice_type': PromptParser._extract_voice_type(prompt_lower),
                'mood': PromptParser._extract_mood(prompt_lower),
                'music_type': PromptParser._extract_music_type(prompt_lower),
                'video_theme': PromptParser._extract_video_theme(prompt_lower),
                'duration': PromptParser._extract_duration(prompt_lower),
                'style': PromptParser._extract_style(prompt_lower),
                'original_prompt': prompt
            }

    @staticmethod
    def _parse_structured_format(prompt: str) -> Dict:
        """
        Parse structured format prompts like:
        Topic: Daily temple benefits
        Style: spiritual motivational
        Voice: Hindi male
        Mood: emotional
        Music: calm devotional
        Video style: temple + sunrise + meditation
        """
        lines = prompt.split('\n')
        params = {
            'keyword': 'content',
            'language': 'english',
            'voice_type': 'female',
            'mood': 'motivational',
            'music_type': 'motivational',
            'video_theme': 'motivation',
            'duration': 30,
            'style': 'cinematic',
            'original_prompt': prompt
        }
        
        for line in lines:
            line = line.strip().lower()
            if not line or ':' not in line:
                continue
            
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # Topic/Keyword
            if key in ['topic', 'keyword', 'subject']:
                params['keyword'] = value.strip()
            
            # Language
            elif key in ['language', 'lang']:
                if 'hindi' in value or 'hin' in value:
                    params['language'] = 'hindi'
                else:
                    params['language'] = 'english'
            
            # Voice
            elif key in ['voice', 'narrator', 'voice type']:
                # Extract language from voice field if present
                if 'hindi' in value or 'hin' in value:
                    params['language'] = 'hindi'
                
                # Extract gender
                if 'male' in value or 'man' in value or 'guy' in value:
                    params['voice_type'] = 'male'
                elif 'female' in value or 'woman' in value or 'girl' in value:
                    params['voice_type'] = 'female'
            
            # Mood
            elif key in ['mood', 'tone']:
                if 'emotional' in value or 'touched' in value or 'touching' in value:
                    params['mood'] = 'emotional'
                elif 'spiritual' in value or 'divine' in value or 'devotional' in value:
                    params['mood'] = 'spiritual'
                elif 'educational' in value or 'educational' in value:
                    params['mood'] = 'educational'
                elif 'funny' in value or 'humor' in value:
                    params['mood'] = 'funny'
                elif 'motivational' in value or 'motivating' in value:
                    params['mood'] = 'motivational'
            
            # Style (can also hint at mood)
            elif key in ['style']:
                # Extract mood from style if mood not already set to specific value
                if 'emotional' in value:
                    params['mood'] = 'emotional'
                elif 'spiritual' in value:
                    params['mood'] = 'spiritual'
                elif 'motivational' in value:
                    params['mood'] = 'motivational'
            
            # Music
            elif key in ['music', 'background', 'bg music', 'music type']:
                if 'calm' in value or 'peaceful' in value or 'soothing' in value:
                    params['music_type'] = 'calm'
                elif 'devotional' in value or 'spiritual' in value or 'meditation' in value:
                    params['music_type'] = 'spiritual'
                elif 'upbeat' in value or 'happy' in value or 'energetic' in value:
                    params['music_type'] = 'upbeat'
                elif 'motivational' in value or 'epic' in value or 'cinematic' in value:
                    params['music_type'] = 'motivational'
            
            # Video Style/Theme
            elif key in ['video style', 'video theme', 'videos', 'theme']:
                # Extract themes from keywords
                if 'temple' in value:
                    params['video_theme'] = 'temple'
                elif 'nature' in value or 'forest' in value or 'green' in value:
                    params['video_theme'] = 'nature'
                elif 'sunrise' in value or 'mountain' in value or 'success' in value:
                    params['video_theme'] = 'success'
                elif 'fitness' in value or 'workout' in value or 'gym' in value:
                    params['video_theme'] = 'fitness'
                elif 'meditation' in value or 'peaceful' in value:
                    params['video_theme'] = 'meditation'
                else:
                    # Use first theme mentioned
                    for theme in ['temple', 'nature', 'success', 'fitness', 'meditation']:
                        if theme in value:
                            params['video_theme'] = theme
                            break
            
            # Duration
            elif key in ['duration', 'length', 'time']:
                duration_match = re.search(r'(\d+)', value)
                if duration_match:
                    dur = int(duration_match.group(1))
                    if 'minute' in value or 'min' in value:
                        dur *= 60
                    if 10 <= dur <= 120:
                        params['duration'] = dur
        
        return params

    @staticmethod
    def _extract_keyword(prompt: str) -> str:
        """
        Extract main topic/keyword from prompt.
        
        Strategy:
        1. Look for "about <keyword>"
        2. Look for "regarding <keyword>"
        3. Look for <keyword> after main action verbs
        4. Extract longest meaningful noun phrase
        """
        prompt_lower = prompt.lower()
        
        # Pattern: "about <topic>" - made terminators optional to handle end-of-string
        about_match = re.search(r'about\s+([a-z\s\-]+?)(?:\.|,|with|using|add|$)', prompt_lower)
        if about_match:
            keyword = about_match.group(1).strip()
            if keyword and keyword != 'a' and len(keyword) > 2:
                return keyword
        
        # Pattern: "regarding <topic>"
        regarding_match = re.search(r'regarding\s+([a-z\s\-]+?)(?:\.|,|with|$)', prompt_lower)
        if regarding_match:
            keyword = regarding_match.group(1).strip()
            if keyword and keyword != 'a' and len(keyword) > 2:
                return keyword
        
        # Pattern: "reel <topic>"
        reel_match = re.search(r'reel\s+(?:about\s+)?([a-z\s\-]+?)(?:\.|,|with|using|$)', prompt_lower)
        if reel_match:
            keyword = reel_match.group(1).strip()
            if keyword and keyword != 'a' and len(keyword) > 2:
                return keyword
        
        # Fallback: extract text after "create" or "make" or "generate"
        create_match = re.search(r'(?:create|make|generate)\s+(?:a\s+)?(?:reel\s+)?(?:about\s+)?(?:(?:hindi|english|in\s+)?(?:spiritual|motivational|emotional|funny|educational)\s+)?([a-z\s\-]+?)(?:\.|,|with|$)', 
                                prompt_lower)
        if create_match:
            keyword = create_match.group(1).strip()
            if keyword and keyword != 'a' and len(keyword) > 2:
                return keyword
        
        return "inspiring content"

    @staticmethod
    def _extract_language(prompt_lower: str) -> str:
        """Extract language preference."""
        for lang, pattern in PromptParser.LANGUAGE_PATTERNS.items():
            if re.search(pattern, prompt_lower):
                return lang
        return 'english'  # Default

    @staticmethod
    def _extract_voice_type(prompt_lower: str) -> str:
        """Extract voice gender preference."""
        for voice, pattern in PromptParser.VOICE_PATTERNS.items():
            if re.search(pattern, prompt_lower):
                return voice
        return 'female'  # Default

    @staticmethod
    def _extract_mood(prompt_lower: str) -> str:
        """Extract desired mood/tone."""
        for mood, pattern in PromptParser.MOOD_PATTERNS.items():
            if re.search(pattern, prompt_lower):
                return mood
        return 'motivational'  # Default

    @staticmethod
    def _extract_music_type(prompt_lower: str) -> str:
        """Extract music type preference."""
        for music_type, pattern in PromptParser.MUSIC_PATTERNS.items():
            if re.search(pattern, prompt_lower):
                return music_type
        return 'motivational'  # Default

    @staticmethod
    def _extract_video_theme(prompt_lower: str) -> str:
        """Extract primary video theme."""
        for theme, pattern in PromptParser.THEME_PATTERNS.items():
            if re.search(pattern, prompt_lower):
                return theme
        return 'motivation'  # Default

    @staticmethod
    def _extract_duration(prompt_lower: str) -> int:
        """Extract desired reel duration in seconds."""
        duration_match = re.search(PromptParser.DURATION_PATTERN, prompt_lower)
        if duration_match:
            duration = int(duration_match.group(1))
            # Convert minutes to seconds if needed
            if 'minute' in duration_match.group(0):
                duration *= 60
            # Ensure reasonable range
            if 10 <= duration <= 120:
                return duration
        return 30  # Default 30 seconds

    @staticmethod
    def _extract_style(prompt_lower: str) -> str:
        """Extract editing style preference."""
        for style, pattern in PromptParser.STYLE_PATTERNS.items():
            if re.search(pattern, prompt_lower):
                return style
        return 'cinematic'  # Default

    @staticmethod
    def get_voice_for_language_and_mood(language: str, gender: str, mood: str) -> str:
        """
        Map language, gender, and mood to specific voice.
        
        Returns:
            str: Edge TTS voice identifier
        """
        voice_map = {
            ('hindi', 'male', 'motivational'): 'hi-IN-MadhurNeural',
            ('hindi', 'male', 'emotional'): 'hi-IN-MadhurNeural',
            ('hindi', 'male', 'spiritual'): 'hi-IN-MadhurNeural',
            ('hindi', 'female', 'motivational'): 'hi-IN-SwaraNeural',
            ('hindi', 'female', 'emotional'): 'hi-IN-SwaraNeural',
            ('hindi', 'female', 'spiritual'): 'hi-IN-SwaraNeural',
            
            ('english', 'male', 'motivational'): 'en-US-GuyNeural',
            ('english', 'male', 'emotional'): 'en-US-AmberNeural',
            ('english', 'male', 'spiritual'): 'en-US-GuyNeural',
            ('english', 'male', 'educational'): 'en-US-GuyNeural',
            ('english', 'female', 'motivational'): 'en-US-JennyNeural',
            ('english', 'female', 'emotional'): 'en-US-JennyNeural',
            ('english', 'female', 'spiritual'): 'en-US-JennyNeural',
            ('english', 'female', 'educational'): 'en-US-JennyNeural',
        }
        
        key = (language.lower(), gender.lower(), mood.lower())
        return voice_map.get(key, 'en-US-JennyNeural')  # Default fallback

    @staticmethod
    def get_music_search_query(music_type: str, keyword: str = '') -> str:
        """
        Generate search query for Freesound API based on music type.
        
        Args:
            music_type (str): Type of music (calm, motivational, spiritual, etc.)
            keyword (str): Optional keyword for refinement
            
        Returns:
            str: Search query for Freesound
        """
        music_queries = {
            'calm': 'calm peaceful relaxing background music',
            'motivational': 'cinematic motivational inspirational music',
            'spiritual': 'meditation spiritual devotional music',
            'upbeat': 'happy cheerful upbeat background music'
        }
        
        base_query = music_queries.get(music_type, 'background music')
        
        if keyword:
            return f"{base_query} {keyword}"
        return base_query

    @staticmethod
    def get_video_search_queries(theme: str, keyword: str = '') -> list:
        """
        Generate search queries for Pexels API based on keyword PRIMARY, theme secondary.
        
        PRIORITY: Keyword is most important (actual topic)
        Theme is a modifier to refine results without changing primary topic
        
        Args:
            theme (str): Video theme (temple, nature, success, etc.)
            keyword (str): Original keyword (PRIMARY - actual topic)
            
        Returns:
            list: List of search queries to try (keyword-first strategy)
        """
        theme_modifiers = {
            'temple': ['spiritual', 'prayer', 'peaceful'],
            'nature': ['nature', 'outdoor', 'landscape'],
            'success': ['sunrise', 'mountain', 'goal'],
            'motivation': ['inspire', 'goal', 'ambitious'],
            'fitness': ['workout', 'health', 'activity'],
            'meditation': ['peaceful', 'calm', 'relax'],
            'daily_life': ['lifestyle', 'routine', 'daily']
        }
        
        modifiers = theme_modifiers.get(theme, [])
        queries = []
        
        # STRATEGY: Keyword FIRST (primary), theme modifies second (secondary)
        if keyword:
            # Exact keyword first (most relevant)
            queries.append(keyword)
            
            # Keyword with theme modifiers (refined)
            for modifier in modifiers[:2]:  # Use top 2 modifiers only
                queries.append(f"{keyword} {modifier}")
            
            # Variations for fallback
            queries.extend([
                f"{keyword} video",
                f"{keyword} footage", 
                f"{keyword} background"
            ])
        else:
            # No keyword provided, use theme defaults
            queries.extend(modifiers if modifiers else ['video', 'content'])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_queries = []
        for q in queries:
            q_lower = q.lower()
            if q_lower not in seen:
                seen.add(q_lower)
                unique_queries.append(q)
        
        return unique_queries


def demo_parser():
    """Demo the prompt parser."""
    test_prompts = [
        "Create a 25 second Hindi motivational reel about benefits of temple daily with calm devotional music, male voice",
        "Generate emotional English reel about fitness with upbeat music",
        "Make a 45 second spiritual meditation reel with peaceful background and female narrator",
    ]
    
    print("PROMPT PARSER DEMO")
    print("=" * 70)
    
    for prompt in test_prompts:
        print(f"\n📝 Prompt: {prompt}")
        print("-" * 70)
        
        params = PromptParser.parse(prompt)
        
        print(f"  Keyword: {params['keyword']}")
        print(f"  Language: {params['language']}")
        print(f"  Voice: {params['voice_type']}")
        print(f"  Mood: {params['mood']}")
        print(f"  Music: {params['music_type']}")
        print(f"  Video Theme: {params['video_theme']}")
        print(f"  Duration: {params['duration']}s")
        print(f"  Style: {params['style']}")
        
        voice = PromptParser.get_voice_for_language_and_mood(
            params['language'], 
            params['voice_type'], 
            params['mood']
        )
        print(f"  Selected Voice: {voice}")
        
        music_query = PromptParser.get_music_search_query(params['music_type'], params['keyword'])
        print(f"  Music Search: {music_query}")
        
        video_queries = PromptParser.get_video_search_queries(params['video_theme'], params['keyword'])
        print(f"  Video Search Queries: {video_queries}")


if __name__ == '__main__':
    demo_parser()
