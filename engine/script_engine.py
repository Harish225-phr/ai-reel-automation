"""
Script Engine for Professional AI Reel Automation.
Generates engaging scripts based on keywords and styles.
Optimized for natural voice narration (20-25 seconds).
"""

import random
from utils import logger


class ScriptEngine:
    """Generate professional video scripts."""
    
    # Script templates optimized for natural narration
    TEMPLATES = {
        'motivational': [
            "Breaking News: {keyword}? Your life is about to change. Here's why {keyword_short} is INCREDIBLE: {fact}. But wait, there's more! {insight}. Did you know? Most people never discover this. {benefit_detail}. This is REVOLUTIONARY. This is WHY we need {action}. Don't miss out. Follow for more life-changing content!",
            "ALERT: {keyword} can literally {action}! {fact}. Here's the science: {insight}. This changes EVERYTHING you know. {benefit_detail}. The results? AMAZING. People are SHOCKED. Tag someone who NEEDS this. Share this with everyone NOW!",
            "Stop wasting time without knowing this: {keyword}. {fact}. Think about it: {insight}. {benefit_detail}. This is the FUTURE. Your competitors know this already. You need to catch up. This will TRANSFORM you. Follow immediately!",
            "{keyword}? Game. Changer. {fact}. Let me explain why: {insight}. {benefit_detail}. This is not hype. This is REAL. Scientists confirm this. Experts agree. This is your moment. This is your chance. Don't wait!",
            "What if {keyword} could {benefit}? {fact}. Actually, it CAN! {insight}. Here's proof: {benefit_detail}. This is revolutionary. This is powerful. This is exactly what you've been searching for. Your success starts HERE!",
        ],
        'educational': [
            "Let's talk about {keyword} - this is actually fascinating. {fact}. Here's how it works: {insight}. You see, {benefit_detail}. The mechanism is simple: {action}. This is crucial knowledge. Understanding {keyword_short} changes your perspective. This is why experts say {keyword} is essential. Learn more!",
            "{keyword} explained scientifically: {fact}. Breaking it down: {insight}. The key understanding here is {benefit_detail}. Why does this matter? Because {action}. This knowledge is power. Students need to know this. Workers need to know this. Everyone needs to know this!",
            "Science lesson about {keyword}: {fact}. Here's the explanation: {insight}. The interesting part? {benefit_detail}. This relates to {action}. This is important because {keyword_short} affects your daily life. Understanding this makes you more informed. Share this knowledge!",
            "Deep dive into {keyword}: {fact}. The research shows: {insight}. Consider this angle: {benefit_detail}. This connects to {action}. The takeaway? {keyword} is more important than most people think. Knowledge is power. You now have the knowledge!",
            "Understanding {keyword} in 2026: {fact}. Modern science says: {insight}. Here's why it matters: {benefit_detail}. The connection? {action}. This is contemporary knowledge. This is relevant NOW. This shapes our future. Remember this!",
        ],
        'entertaining': [
            "OMG wait for the end... {keyword} is MORE insane than you think! {fact}. You won't BELIEVE what happens next: {insight}. {benefit_detail}. This is WILD. This is CRAZY. This is absolutely mind-blowing. Your reaction: SHOCKED. Your next move: SHARE THIS!",
            "POV: You just discovered {keyword}. {fact}. Your mind right now: EXPLODING. {insight}. {benefit_detail}. This is insane. What just happened? Your perspective just changed. You're different now. You can never unsee this. Tag your friends!",
            "They don't WANT you to know about {keyword}! {fact}. But here's the SECRET: {insight}. {benefit_detail}. The truth? {action}. This is HUGE. This is EARTH-SHATTERING. This is the plot twist of the century. SHARE before this gets hidden!",
            "{keyword} TIER RANKING: {fact}. Rating: {insight}. {benefit_detail}. Verdict? {action}. This is PEAK content. This is ENTERTAINMENT. This is what you came for. Comment your take! Tell me in the replies!",
            "I tested {keyword} for real... {fact}. What happened? {insight}. Results? {benefit_detail}. Conclusion: {action}. This ACTUALLY works. Would I recommend? 100%. Is this worth your time? ABSOLUTELY. Watch till the end!",
        ],
        'trending': [
            "#1 TRENDING NOW: {keyword}. {fact}. Why is this EVERYWHERE? {insight}. The real story: {benefit_detail}. Impact: {action}. This is the topic of the moment. Everyone is talking about this. You NEED to understand this. Stay informed!",
            "VIRAL ALERT: {keyword} is spreading FAST. {fact}. Here's why it matters: {insight}. The significance: {benefit_detail}. What it means: {action}. This is currently trending. This is THIS WEEK'S biggest story. Don't fall behind. Follow for updates!",
            "BREAKING: {keyword} news that's SHOCKING! {fact}. The implications: {insight}. What experts say: {benefit_detail}. The bottom line: {action}. This is URGENT. This is HAPPENING NOW. This affects you. This is relevant TODAY. React now!",
            "{keyword} is EXPLODING right now — here's why: {fact}. The trend analysis: {insight}. What's driving it: {benefit_detail}. The prediction: {action}. This momentum is REAL. This is the hottest topic. This is what's HOT in {keyword_short}. Join the conversation!",
            "HOTTEST TOPIC: {keyword} — everyone's discussing this. {fact}. Context: {insight}. Real talk: {benefit_detail}. The verdict: {action}. This is the conversation of the hour. This is CURRENT. This is LIVE. This is HAPPENING. Comment NOW!",
        ],
    }
    
    # Extended keyword database
    KEYWORD_DATA = {
        'tree': {
            'facts': [
                'one mature tree can absorb CO2 equivalent to driving a car for 26,000 miles',
                'trees provide oxygen for two people per year',
                'a single tree can filter multiple tons of pollutants from the air',
                'the oldest tree is over 5,000 years old',
                'trees store 3 times more carbon than shrubs',
                'forests cover 31% of Earth but are rapidly disappearing',
                'tree roots prevent soil erosion and save millions in infrastructure',
            ],
            'insights': [
                'one tree creates a ripple effect through entire ecosystems',
                'trees are literally the lungs of our planet',
                'planting trees today saves future generations',
                'nature designed the perfect carbon capture system',
                'green spaces increase property value by 15-20%',
                'forest therapy reduces stress by up to 37%',
                'every single tree matters for biodiversity',
            ],
            'actions': ['absorbs carbon dioxide', 'purifies the air', 'provides shelter', 'creates ecosystems', 'prevents erosion', 'cools the planet'],
            'benefits': ['clean air for 2 people', 'natural shade and cooling', 'habitat for wildlife', 'reduced air pollution', 'massive environmental impact', 'long-term health benefits'],
            'benefit_details': [
                'trees actively combat climate change by absorbing greenhouse gases',
                'they provide immense health benefits through shade and improved air quality',
                'forests sustain 80% of land animals and support biodiversity',
                'urban trees increase quality of life and mental wellbeing significantly',
                'tree planting prevents soil degradation and protects water sources',
                'green cover reduces urban heat island effect by up to 8 degrees',
            ]
        },
        'environment': {
            'facts': [
                'we have less than a decade to make critical climate changes',
                'plastic takes 500+ years to decompose in oceans',
                '1 million species are on the brink of extinction',
                'oceans absorb 90% of excess heat from climate change',
                'renewable energy is now cheaper than fossil fuels',
                '90% of oceans are still unexplored and unmapped',
                'transportation accounts for 27% of global emissions',
            ],
            'insights': [
                'every small action compounds into massive global change',
                'sustainability is not optional anymore',
                'nature provides everything we need',
                'we need urgent collective action',
                'your choices directly impact the planet',
                'the time for action is literally NOW',
                'environmental protection is self-preservation',
            ],
            'actions': ['changes daily', 'affects every living thing', 'requires immediate action', 'impacts your future', 'is calling for solutions'],
            'benefits': ['breathable air', 'clean water supply', 'sustainable future', 'thriving biodiversity', 'stable climate', 'healthy ecosystems'],
            'benefit_details': [
                'environmental action creates cascading effects across all ecosystems',
                'protecting the planet secures resources for future generations',
                'sustainability is the blueprint for surviving and thriving long-term',
                'every environmental choice multiplies impacts across communities',
                'green initiatives create economic opportunities and innovation',
                'conscious practices preserve the beauty and resources we cherish',
            ]
        },
        'health': {
            'facts': [
                'regular exercise reduces depression and anxiety by 30-47%',
                'meditation improves focus and concentration by 40%',
                'quality sleep repairs your entire body at cellular level',
                'hydration affects 75% of your muscle performance',
                'movement adds years to your lifespan',
                'nutrition literally builds your brain and body',
                'stress management extends life expectancy by 10+ years',
            ],
            'insights': [
                'your body is an incredible machine that heals itself',
                'small daily habits create massive life transformations',
                'consistency beats intensity every single time',
                'prevention is infinitely better than treatment',
                'taking care of yourself is the best investment',
                'health is truly wealth in every dimension',
                'your future self will thank you for starting today',
            ],
            'actions': ['transforms your entire life', 'starts with today', 'changes everything forever', 'is absolutely possible', 'begins right now'],
            'benefits': ['boundless energy', 'mental clarity', 'emotional peace', 'physical strength', 'longevity', 'confidence and joy'],
            'benefit_details': [
                'health practices compound over time creating exponential benefits',
                'prioritizing wellness is the single best investment you can make',
                'consistent health habits rebuild your body and mind at cellular levels',
                'better health unlocks potential you never knew existed',
                'wellness practices reduce disease risk while maximizing quality of life',
                'taking care of yourself validates your worth and enables greatness',
            ]
        },
        'business': {
            'facts': [
                'consistent entrepreneurs are 70% more likely to succeed',
                'passive income streams multiply your earnings potential',
                'networking opens doors that money cannot buy',
                'knowledge compounds exponentially over time',
                'timing and execution determine 90% of success',
                'the average millionaire has seven income streams',
                'entrepreneurship teaches you life lessons no school can',
            ],
            'insights': [
                'success leaves detailed clues',
                'your mindset determines your ceiling',
                'action beats perfect planning',
                'every failure is premium education',
                'you can scale beyond your wildest dreams',
                'the opportunity window is NOW',
                'your network truly equals your net worth',
            ],
            'actions': ['creates wealth systems', 'builds generational wealth', 'transforms financial reality', 'scales infinitely', 'opens unlimited possibilities'],
            'benefits': ['financial freedom', 'personal independence', 'passive income streams', 'unlimited earning potential', 'time flexibility', 'legacy building'],
            'benefit_details': [
                'business success creates wealth that extends far beyond circumstances',
                'entrepreneurship builds assets that generate income while you sleep',
                'financial independence enables freedom to pursue your passions',
                'business knowledge becomes your most valuable asset',
                'success systems replicate and scale creating exponential growth',
                'building enterprise creates employment and value for ecosystems',
            ]
        }
    }
    
    @staticmethod
    def generate(keyword, style='motivational', length='long'):
        """
        Generate professional video script.
        
        Args:
            keyword (str): Main topic
            style (str): motivational/educational/entertaining/trending
            length (str): short/medium/long (affects pacing)
            
        Returns:
            dict: Script data with text, hook, and metadata
        """
        try:
            logger.info(f"Generating script: keyword='{keyword}', style='{style}'")
            
            # Get style template
            style_lower = style.lower()
            if style_lower not in ScriptEngine.TEMPLATES:
                style_lower = 'motivational'
            
            templates = ScriptEngine.TEMPLATES[style_lower]
            template = random.choice(templates)
            
            # Try to find exact keyword match
            keyword_lower = keyword.lower()
            keyword_data = None
            
            # Check for exact match
            if keyword_lower in ScriptEngine.KEYWORD_DATA:
                keyword_data = ScriptEngine.KEYWORD_DATA[keyword_lower]
            else:
                # Check for partial matches
                for key in ScriptEngine.KEYWORD_DATA:
                    if key in keyword_lower or keyword_lower in key:
                        keyword_data = ScriptEngine.KEYWORD_DATA[key]
                        break
            
            # If no match found, generate dynamic data for the keyword
            # DO NOT default to 'tree' - use the keyword directly with generic templates
            if keyword_data is None:
                logger.info(f"[INFO] Using dynamic script generation for keyword: '{keyword}'")
                keyword_data = {
                    'facts': [
                        f'{keyword} has transformative power that most people overlook',
                        f'recent discoveries about {keyword} will surprise you',
                        f'{keyword} is becoming increasingly important in 2026',
                        f'the impact of {keyword} is far greater than commonly believed',
                        f'{keyword} is changing lives globally right now',
                    ],
                    'insights': [
                        f'understanding {keyword} gives you an unfair advantage',
                        f'{keyword} represents a fundamental shift in our world',
                        f'the deeper you go into {keyword}, the more it matters',
                        f'{keyword} is more important than most people realize',
                        f'success increasingly depends on knowing about {keyword}',
                    ],
                    'actions': [f'transforms your view of {keyword}', f'revolutionizes how you think about {keyword}', 
                               f'changes everything about {keyword}', f'unlocks {keyword} potential'],
                    'benefits': [f'{keyword} mastery', f'deeper {keyword} understanding', f'{keyword} breakthrough', 
                                f'game-changing {keyword} insights', f'{keyword} transformation'],
                    'benefit_details': [
                        f'{keyword} knowledge creates breakthrough thinking',
                        f'mastering {keyword} opens unlimited possibilities',
                        f'{keyword} understanding accelerates personal growth',
                        f'learning {keyword} changes your future trajectory',
                        f'{keyword} expertise becomes invaluable competitive advantage',
                    ]
                }
            
            # Extract components
            fact = random.choice(keyword_data['facts'])
            insight = random.choice(keyword_data['insights'])
            action = random.choice(keyword_data['actions'])
            benefit = random.choice(keyword_data['benefits'])
            benefit_detail = random.choice(keyword_data.get('benefit_details', keyword_data['benefits']))
            
            keyword_short = keyword.split()[0]
            
            # Generate script
            script = template.format(
                keyword=keyword,
                keyword_short=keyword_short,
                fact=fact,
                insight=insight,
                action=action,
                benefit=benefit,
                benefit_detail=benefit_detail
            )
            
            # Create hook (first sentence, not keyword name)
            hook = script.split('.')[0][:80]  # First sentence, max 80 chars
            if not hook:
                hook = f"Everything about {keyword}"
            
            result = {
                'script': script,
                'hook': hook,
                'cta': 'Follow for more!',
                'keyword': keyword,
                'style': style_lower,
                'length': length
            }
            
            logger.info(f"[OK] Script generated: {len(script)} characters")
            return result
            
        except Exception as e:
            logger.error(f"Error generating script: {e}")
            return {
                'script': f"{keyword} is amazing! Learn more about this incredible topic. Follow for more insights!",
                'hook': keyword,
                'cta': 'Follow for more!',
                'keyword': keyword,
                'style': style,
                'length': length
            }
