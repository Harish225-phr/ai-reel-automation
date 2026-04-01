"""
STABLE SCRIPT ENGINE - Fixed Structure for Reliability
Generates: Hook + 3 Benefits + CTA (Fixed formula for consistency)
No AI models. Deterministic output. Always works.
"""

import random


class StableScriptEngine:
    """
    Fixed-structure script generator.
    
    Formula: Hook (2s) + Benefit 1 (8s) + Benefit 2 (8s) + Benefit 3 (8s) + CTA (2s)
    Total: ~28 seconds of narration
    """
    
    HOOK_TEMPLATES = [
        "What if I told you {keyword} could completely change your life?",
        "Let me show you something life-changing about {keyword}.",
        "Ready to discover the power of {keyword}?",
        "Here's what you need to know about {keyword}.",
        "Stop what you're doing and listen to this about {keyword}.",
        "Everyone's talking about {keyword}. Here's why.",
        "The secret to {keyword} that nobody's telling you.",
        "You've been missing out on the benefits of {keyword}.",
    ]
    
    BENEFIT_TEMPLATES = [
        "First, {keyword} gives you {benefit}. This alone transforms your day.",
        "Here's the amazing part: {keyword} provides {benefit}. It's life-changing.",
        "You need to know this: {keyword} creates {benefit}. Trust me.",
        "The best part? {keyword} unlocks {benefit}. Your future self will thank you.",
        "Get ready for this: {keyword} delivers {benefit}. Seriously.",
    ]
    
    CTA_TEMPLATES = [
        "Start your journey with {keyword} today. You won't regret it.",
        "Ready to transform? Choose {keyword} right now.",
        "Don't wait. Experience {keyword} for yourself. Do it today.",
        "This is your moment. Take action with {keyword}. Let's go.",
        "Your life changes when you embrace {keyword}. Start now.",
    ]
    
    BENEFITS_BY_KEYWORD = {
        # Motivational/Success keywords
        'motivation': ['unstoppable confidence', 'crystal clear focus', 'unbreakable determination'],
        'success': ['rapid growth', 'financial freedom', 'personal power'],
        'achievement': ['peak performance', 'breakthrough results', 'lasting impact'],
        'goals': ['laser focus', 'momentum building', 'milestone crushing'],
        'productivity': ['extreme efficiency', 'flow state mastery', 'time multiplication'],
        
        # Fitness/Health keywords
        'fitness': ['lean muscle growth', 'explosive energy', 'athletic performance'],
        'workout': ['maximum strength', 'cardio endurance', 'body transformation'],
        'health': ['vibrant wellness', 'immune strength', 'mental clarity'],
        'yoga': ['inner peace', 'physical flexibility', 'stress relief'],
        'meditation': ['mindful awareness', 'emotional balance', 'deep relaxation'],
        
        # Financial keywords
        'money': ['passive income streams', 'wealth accumulation', 'financial independence'],
        'business': ['market dominance', 'revenue explosion', 'client magnetism'],
        'investing': ['portfolio growth', 'smart wealth building', 'financial security'],
        'startup': ['rapid scaling', 'market disruption', 'unicorn potential'],
        
        # Learning keywords
        'learning': ['rapid skill mastery', 'knowledge retention', 'confident execution'],
        'education': ['intellectual growth', 'career advancement', 'expert status'],
        'skills': ['professional excellence', 'market value increase', 'opportunity doors'],
        'coding': ['problem-solving power', 'tech mastery', 'career transformation'],
        
        # Lifestyle keywords
        'lifestyle': ['time freedom', 'location independence', 'life balance'],
        'travel': ['adventure experiences', 'cultural immersion', 'bucket list living'],
        'happiness': ['joy cultivation', 'life satisfaction', 'inner fulfillment'],
        'morning': ['energetic starts', 'focused productivity', 'day domination'],
        
        # Default generic benefits
        'default': ['incredible transformation', 'powerful momentum', 'life-changing results'],
    }
    
    @staticmethod
    def get_benefits(keyword: str) -> list:
        """Get 3 benefits for a keyword"""
        keyword_lower = keyword.lower()
        
        # Check for exact match
        if keyword_lower in StableScriptEngine.BENEFITS_BY_KEYWORD:
            return StableScriptEngine.BENEFITS_BY_KEYWORD[keyword_lower]
        
        # Check for partial match
        for key, benefits in StableScriptEngine.BENEFITS_BY_KEYWORD.items():
            if key in keyword_lower or keyword_lower in key:
                return benefits
        
        # Return default
        return StableScriptEngine.BENEFITS_BY_KEYWORD['default']
    
    @staticmethod
    def generate(keyword: str, language: str = 'en') -> dict:
        """
        Generate fixed-structure script.
        
        Args:
            keyword (str): Main topic/keyword
            language (str): 'en' or 'hi' (for future expansion)
        
        Returns:
            dict: {
                'script': Full narration text,
                'duration_estimate': Estimated seconds,
                'structure': List of [section, text] pairs,
                'word_count': Total words
            }
        """
        
        # Get 3 benefits for this keyword
        benefits = StableScriptEngine.get_benefits(keyword)
        
        # Randomly select templates for variety
        hook = random.choice(StableScriptEngine.HOOK_TEMPLATES).format(keyword=keyword)
        
        benefit_1 = random.choice(StableScriptEngine.BENEFIT_TEMPLATES).format(
            keyword=keyword,
            benefit=benefits[0]
        )
        benefit_2 = random.choice(StableScriptEngine.BENEFIT_TEMPLATES).format(
            keyword=keyword,
            benefit=benefits[1]
        )
        benefit_3 = random.choice(StableScriptEngine.BENEFIT_TEMPLATES).format(
            keyword=keyword,
            benefit=benefits[2]
        )
        
        cta = random.choice(StableScriptEngine.CTA_TEMPLATES).format(keyword=keyword)
        
        # Combine into final script
        script = f"{hook} {benefit_1} {benefit_2} {benefit_3} {cta}"
        
        # Build structure map for debug
        structure = [
            ('Hook', hook),
            ('Benefit 1', benefit_1),
            ('Benefit 2', benefit_2),
            ('Benefit 3', benefit_3),
            ('CTA', cta),
        ]
        
        # Count words and estimate duration
        word_count = len(script.split())
        # Average speech rate: ~150 words per minute = 2.5 words per second
        duration_estimate = word_count / 2.5
        
        return {
            'script': script,
            'duration_estimate': duration_estimate,
            'structure': structure,
            'word_count': word_count,
            'keyword': keyword,
        }


def demo():
    """Demo the stable script generator"""
    keywords = [
        'motivation',
        'fitness',
        'money',
        'learning',
        'happiness',
    ]
    
    for keyword in keywords:
        print(f"\n{'='*60}")
        print(f"Keyword: {keyword}")
        print('='*60)
        
        result = StableScriptEngine.generate(keyword)
        print(f"Script: {result['script']}\n")
        print(f"Word count: {result['word_count']}")
        print(f"Duration estimate: {result['duration_estimate']:.1f} seconds")
        print(f"\nStructure:")
        for section, text in result['structure']:
            print(f"  {section}: {text[:60]}...")


if __name__ == '__main__':
    demo()
