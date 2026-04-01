"""
Smart Script Generator - Generates scripts matching mood and tone
"""

import re


class SmartScriptGenerator:
    """
    Generates scripts matching desired mood and tone.
    Uses prompt parameters to craft appropriate narration.
    """

    # Tone templates based on mood
    MOOD_TEMPLATES = {
        'motivational': {
            'opening': [
                "What if I told you that {keyword} could completely transform your life? Here's how...",
                "Feeling stuck? The answer might be simpler than you think: {keyword}...",
                "The most successful people on the planet know this secret about {keyword}...",
                "Are you ready to discover the life-changing power of {keyword}?",
                "Stop struggling. {keyword} is the breakthrough you've been searching for...",
            ],
            'body': [
                "First - and this is crucial - {benefit}. This changes everything.",
                "Second, and this one will blow your mind: {benefit}.",
                "Here's what most people miss: {benefit}.",
                "The breakthrough happens right here: {benefit}.",
                "This is where the transformation accelerates: {benefit}.",
            ],
            'closing': [
                "Imagine yourself a year from now, transformed by {keyword}. That's your future.",
                "The best time to start was yesterday. The second best is right now. Choose {keyword}.",
                "Your success with {keyword} depends on one decision: taking action today.",
                "This isn't just information - this is your roadmap to becoming unstoppable.",
                "Your transformation starts now. Will you seize this opportunity with {keyword}?",
            ]
        },
        'emotional': {
            'opening': [
                "There's something beautiful about {keyword} that touches the deepest part of us...",
                "Let me share something that transformed my understanding of {keyword}...",
                "In those quiet moments, the true power of {keyword} reveals itself...",
                "Close your eyes and feel the profound grace of {keyword}...",
                "Sometimes the most life-changing moments are when we fully embrace {keyword}...",
            ],
            'body': [
                "When we truly understand {benefit}, everything changes.",
                "This is where the magic happens: {benefit}.",
                "Can you feel it? {benefit} - this is transformation.",
                "Pay close attention to this: {benefit}.",
                "Let this sink deep into your soul: {benefit}.",
            ],
            'closing': [
                "Let {keyword} heal your heart and awaken your spirit today.",
                "Your journey with {keyword} starts with feeling, not thinking.",
                "Open yourself completely to {keyword} - this is where miracles happen.",
                "The path of {keyword} leads to your highest self.",
                "Begin now. This is your moment. This is {keyword}.",
            ]
        },
        'spiritual': {
            'opening': [
                "For thousands of years, people have discovered divine truth through {keyword}...",
                "There's an ancient power in {keyword} that modern science is only beginning to understand...",
                "Your spiritual awakening begins with understanding {keyword}...",
                "In devotion to {keyword}, we find our highest purpose and truest self...",
                "The cosmos has been calling you toward {keyword}. Can you feel it?",
            ],
            'body': [
                "This is the divine truth: {benefit}.",
                "When you embrace {benefit}, you align with universal energy.",
                "The spiritual power lies in this: {benefit}.",
                "Your soul recognizes this wisdom: {benefit}.",
                "Feel the eternal energy flowing through: {benefit}.",
            ],
            'closing': [
                "Let {keyword} be your bridge to the divine.",
                "Your sacred journey with {keyword} begins right now.",
                "In {keyword}, discover your infinite potential and eternal truth.",
                "This is your calling. Embrace {keyword} and transform completely.",
                "Your awakening starts here, in the beauty of {keyword}.",
            ]
        },
        'educational': {
            'opening': [
                "Scientists have made a groundbreaking discovery about {keyword}...",
                "Research reveals why {keyword} is reshaping our understanding...",
                "Most people don't know this crucial fact about {keyword}...",
                "Here's what experts have finally proven about {keyword}...",
                "The data is clear: {keyword} is the key to transformation...",
            ],
            'body': [
                "The evidence is undeniable: {benefit}.",
                "Studies consistently show that {benefit}.",
                "This scientific breakthrough explains how {benefit}.",
                "The research confirms what practitioners have always known: {benefit}.",
                "Real-world results prove that {benefit}.",
            ],
            'closing': [
                "Armed with this knowledge, you can master {keyword} completely.",
                "The science is undeniable. {keyword} truly changes everything.",
                "This knowledge puts you ahead of 99% of people.",
                "Now that you understand {keyword}, your life will never be the same.",
                "Take action on this knowledge. Your future depends on understanding {keyword}.",
            ]
        },
        'funny': {
            'opening': [
                "Okay, so {keyword} is about to blow your mind...",
                "Warning: What you're about to learn about {keyword} is hilarious...",
                "You're not ready for this {keyword} story...",
                "Trust me, {keyword} is way funnier than you think...",
                "Prepare yourself. {keyword} is about to get real...",
            ],
            'body': [
                "Ready? Here it is: {benefit}. Seriously.",
                "The crazy part? {benefit}. No joke.",
                "This is where {benefit} gets wild.",
                "Plot twist: {benefit}. Mind blown.",
                "And here's the best part: {benefit}.",
            ],
            'closing': [
                "So yeah, {keyword} is absolutely incredible.",
                "That's why {keyword} has millions of believers.",
                "Now you're part of the {keyword} revolution. Welcome.",
                "Share this {keyword} magic with everyone you know.",
                "Your life just changed because of {keyword}.",
            ]
        }
    }

    BENEFIT_DATABASE = {
        'temple': [
            'spiritual peace flows through your entire being',
            'your mind releases stress and harmful thoughts',
            'you connect with something greater than yourself',
            'your inner light shines brighter each day',
            'ancient wisdom guides your most important decisions',
            'blessings and protection surround your life',
            'your soul finds its true purpose and direction'
        ],
        'yoga': [
            'your body becomes strong, flexible, and resilient',
            'stress and anxiety melt away with each breathing exercise',
            'your mind finds clarity and peaceful focus',
            'energy flows through your being with renewed vitality',
            'your physical health transforms in remarkable ways',
            'emotional balance becomes your natural state',
            'inner strength and confidence radiate from within'
        ],
        'meditation': [
            'your mind becomes like still water, clear and peaceful',
            'anxiety releases its grip on your daily life',
            'you discover a deep sense of inner contentment',
            'focus and concentration sharpen dramatically',
            'sleep becomes deeper and more restorative',
            'creativity flows naturally and effortlessly',
            'you find your true self beneath all the noise'
        ],
        'fitness': [
            'your body transforms into its strongest version',
            'energy surges through you all day long',
            'confidence radiates from your healthier, stronger physique',
            'you add years of vitality and longevity to your life',
            'your mind becomes sharper and more resilient',
            'disease runs far from your thriving body',
            'happiness elevates as your health improves'
        ],
        'nature': [
            'your mind heals from the weight of daily stress',
            'you become grounded in the present moment',
            'stress hormones release and your nervous system calms',
            'creativity awakens with natural inspiration',
            'you feel connected to something larger and timeless',
            'perspective returns, bringing inner peace',
            'your spirit renews with natural energy'
        ],
        'success': [
            'your dreams transform into living reality',
            'personal fulfillment fills every corner of your heart',
            'financial abundance flows into your life',
            'respect and recognition come from those around you',
            'unstoppable confidence defines your presence',
            'others find inspiration in your remarkable journey',
            'your legacy impacts generations to come'
        ]
    }

    # ================================================================
    # HINDI TEMPLATES AND BENEFITS
    # ================================================================
    HINDI_MOOD_TEMPLATES = {
        'motivational': {
            'opening': [
                "क्या आप जानते हैं कि {keyword} आपके जीवन को पूरी तरह बदल सकता है?",
                "आज ही शुरू करें {keyword} की यात्रा क्योंकि यह आपका सबसे बड़ा मौका है।",
                "हजारों लोग {keyword} की शक्ति से अपना जीवन बदल चुके हैं।",
                "रुकिए मत। {keyword} के साथ आपकी सफलता निश्चित है।",
                "इस समय सबसे जरूरी है {keyword} को समझना।",
            ],
            'body': [
                "सुनिए: {benefit}",
                "यह बहुत महत्वपूर्ण है - {benefit}",
                "ध्यान दीजिए इस शक्ति को: {benefit}",
                "यही सच्चाई है: {benefit}",
                "आपका भविष्य बदलता है जब आप समझते हैं कि {benefit}",
            ],
            'closing': [
                "{keyword} को अपनाइए और अपना सपना सच करिए।",
                "अब का समय है। {keyword} के साथ शुरू करें।",
                "आपकी सफलता {keyword} में ही छिपी है।",
                "आज ही तय करें - {keyword} आपका रास्ता है।",
                "यही आपका मौका है। {keyword} को चुनिए अभी।",
            ]
        },
        'emotional': {
            'opening': [
                "{keyword} में कुछ ऐसी खूबसूरती है जो हमारे दिल को छूती है।",
                "मैं आपको {keyword} का एक गहरा सच बताना चाहता हूं।",
                "जब हम {keyword} को सच में समझते हैं, तो सबकुछ बदल जाता है।",
                "आपके आत्मा को {keyword} की जरूरत है।",
                "चुप रहकर {keyword} की शक्ति को महसूस कीजिए।",
            ],
            'body': [
                "यह हो रहा है: {benefit}",
                "क्या आप इसे महसूस कर रहे हैं? {benefit}",
                "यह वास्तविकता है: {benefit}",
                "आपका दिल जानता है कि {benefit}",
                "गहराई से सोचिए: {benefit}",
            ],
            'closing': [
                "{keyword} आपके दिल को ठीक कर सकता है।",
                "आपकी {keyword} की यात्रा आज से शुरू होती है।",
                "{keyword} में आपका असली आत्म छिपा है।",
                "यह आपका समय है। {keyword} को अपनाइए।",
                "अब से। यह पल। यही {keyword} है।",
            ]
        },
        'spiritual': {
            'opening': [
                "हजारों सालों से {keyword} के द्वारा लोग सच्ची शक्ति पा रहे हैं।",
                "{keyword} में एक प्राचीन दिव्य शक्ति है।",
                "आपकी आध्यात्मिक जागृति {keyword} से शुरू होती है।",
                "पूजा और {keyword} में ही सच्चा उद्देश्य छिपा है।",
                "ब्रह्मांड आपको {keyword} की ओर बुला रहा है।",
            ],
            'body': [
                "यह दिव्य सच है: {benefit}",
                "जब आप {benefit} को अपनाते हैं, तो आप दिव्य शक्ति से जुड़ जाते हैं।",
                "भीतर की शक्ति यह है: {benefit}",
                "आपकी आत्मा यह सच जानती है: {benefit}",
                "अनंत ऊर्जा {benefit} के द्वारा आप तक आती है।",
            ],
            'closing': [
                "{keyword} आपका आध्यात्मिक सेतु बने।",
                "{keyword} की पवित्र यात्रा आज शुरू होती है।",
                "{keyword} में, आप अपनी अनंत संभावना पाएंगे।",
                "यह आपका बुलावा है। {keyword} को अपनाइए।",
                "{keyword} की सच्चाई में आपकी मुक्ति छिपी है।",
            ]
        },
    }

    HINDI_BENEFIT_DATABASE = {
        'yoga': [
            'आपका शरीर मजबूत, लचकदार और स्वस्थ हो जाता है',
            'तनाव और चिंता दूर हो जाती है हर सांस के साथ',
            'मन शांति और स्पष्टता पाता है',
            'ऊर्जा नई शक्ति के साथ बहती है',
            'आपका स्वास्थ्य बेहतरी से भर जाता है',
            'भावनात्मक संतुलन आपका स्वभाव बन जाता है',
            'आत्मविश्वास आपके अंदर से खिल उठता है'
        ],
        'temple': [
            'आध्यात्मिक शांति आपके पूरे अस्तित्व में बहती है',
            'मन तनाव और नकारात्मता से मुक्त हो जाता है',
            'आप कुछ महान से जुड़ जाते हैं',
            'आपका भीतरी प्रकाश उज्ज्वल हो उठता है',
            'प्राचीन ज्ञान आपके सबसे महत्वपूर्ण फैसलों को गाइड करता है',
            'आशीर्वाद और सुरक्षा आपके जीवन को घेरे रहती है',
            'आपकी आत्मा अपना सच्चा उद्देश्य खोज लेती है'
        ],
        'meditation': [
            'आपका मन शांत जल की तरह स्वच्छ और शांत हो जाता है',
            'चिंता आपकी जीवन से दूर हो जाती है',
            'आप गहरी आंतरिक संतुष्टि की खोज करते हैं',
            'ध्यान और एकाग्रता तेजी से बढ़ती है',
            'नींद गहरी और शांतिदायक हो जाती है',
            'रचनात्मकता स्वाभाविक रूप से बाहर आती है',
            'सभी शोर के नीचे आप अपने आत्मा को पाते हैं'
        ],
        'fitness': [
            'आपका शरीर सबसे मजबूत संस्करण बन जाता है',
            'ऊर्जा पूरे दिन आप में दौड़ती है',
            'आत्मविश्वास आपके स्वस्थ शरीर से निकलता है',
            'आप जीवन में और साल जोड़ते हैं',
            'आपका दिमाग और भी तेज़ हो जाता है',
            'बीमारी आपके स्वस्थ शरीर से दूर रहती है',
            'खुशी बढ़ती है जब आपका स्वास्थ्य बेहतर होता है'
        ],
        'success': [
            'आपके सपने जीवंत वास्तविकता बन जाते हैं',
            'आंतरिक संतुष्टि आपके दिल को भर देती है',
            'आर्थिक समृद्धि आपके जीवन में बहती है',
            'सम्मान और पहचान हर तरफ से आती है',
            'अपराजेय आत्मविश्वास आपको परिभाषित करता है',
            'दूसरे आपके असाधारण यात्रा से प्रेरित होते हैं',
            'आपकी विरासत पीढ़ियों को प्रभावित करती है'
        ]
    }

    @staticmethod
    def generate_script(keyword: str, mood: str, duration: int = 30, 
                       num_sentences: int = 6, language: str = 'english') -> str:
        """
        Generate a complete script matching mood and keyword.
        
        Args:
            keyword (str): Main topic (e.g., 'temple benefits', 'meditation')
            mood (str): Desired tone (motivational, emotional, spiritual, educational, funny)
            duration (int): Approximate reel duration for pacing
            num_sentences (int): Number of sentences to generate
            language (str): Language for script ('english' or 'hindi')
            
        Returns:
            str: Generated script
        """
        
        # Validate inputs
        mood = mood.lower() if mood else 'motivational'
        language = language.lower() if language else 'english'
        
        # Select templates and benefits based on language
        if language == 'hindi':
            if mood not in SmartScriptGenerator.HINDI_MOOD_TEMPLATES:
                mood = 'motivational'
            templates = SmartScriptGenerator.HINDI_MOOD_TEMPLATES[mood]
            benefits_db = SmartScriptGenerator.HINDI_BENEFIT_DATABASE
        else:
            if mood not in SmartScriptGenerator.MOOD_TEMPLATES:
                mood = 'motivational'
            templates = SmartScriptGenerator.MOOD_TEMPLATES[mood]
            benefits_db = SmartScriptGenerator.BENEFIT_DATABASE
        
        # Extract base keyword for benefit lookup
        base_keyword = SmartScriptGenerator._extract_base_keyword(keyword)
        benefits = benefits_db.get(
            base_keyword, 
            benefits_db.get('success', list(benefits_db.values())[0])
        )
        
        script_parts = []
        
        # Add opening
        opening = SmartScriptGenerator._pick_random(templates['opening'])
        opening = opening.format(keyword=keyword)
        script_parts.append(opening)
        
        # Add body sentences
        num_body = max(num_sentences - 2, 2)
        used_benefits = set()
        for i in range(num_body):
            benefit_idx = i % len(benefits)
            benefit = benefits[benefit_idx]
            used_benefits.add(benefit)
            
            body_template = SmartScriptGenerator._pick_random(templates['body'])
            body = body_template.format(
                keyword=keyword,
                benefit=benefit
            )
            script_parts.append(body)
        
        # Add closing
        closing = SmartScriptGenerator._pick_random(templates['closing'])
        closing = closing.format(keyword=keyword)
        script_parts.append(closing)
        
        # Join into complete script
        script = ' '.join(script_parts)
        
        return script

    @staticmethod
    def _extract_base_keyword(keyword: str) -> str:
        """Extract base keyword from complex phrase."""
        keyword_lower = keyword.lower()
        for base in ['yoga', 'temple', 'meditation', 'fitness', 'nature', 'success']:
            if base in keyword_lower:
                return base
        return 'success'

    @staticmethod
    def _pick_random(items: list):
        """Pick random item from list (without random module for consistency)."""
        import hashlib
        seed = hashlib.md5(str(items).encode()).hexdigest()
        index = int(seed, 16) % len(items)
        return items[index]

    @staticmethod
    def split_script_to_sentences(script: str, max_sentences: int = None) -> list:
        """
        Split script into logical sentences.
        
        Args:
            script (str): Full script
            max_sentences (int): Maximum sentences to return
            
        Returns:
            list: List of sentences
        """
        # Split by sentence markers
        sentences = re.split(r'(?<=[.!?])\s+', script)
        
        # Clean up
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Limit if needed
        if max_sentences and len(sentences) > max_sentences:
            sentences = sentences[:max_sentences]
        
        return sentences


def demo_script_generator():
    """Demo the script generator."""
    test_cases = [
        ('temple daily benefits', 'spiritual'),
        ('fitness and health', 'motivational'),
        ('meditation practice', 'emotional'),
        ('success mindset', 'educational'),
    ]
    
    print("SMART SCRIPT GENERATOR DEMO")
    print("=" * 70)
    
    for keyword, mood in test_cases:
        print(f"\n📝 Generating {mood} script about: {keyword}")
        print("-" * 70)
        
        script = SmartScriptGenerator.generate_script(keyword, mood)
        print(f"\nScript:\n{script}")
        
        sentences = SmartScriptGenerator.split_script_to_sentences(script)
        print(f"\nSentences ({len(sentences)}):")
        for i, sentence in enumerate(sentences, 1):
            print(f"  {i}. {sentence}")


if __name__ == '__main__':
    demo_script_generator()
