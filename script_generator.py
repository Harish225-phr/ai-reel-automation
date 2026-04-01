"""
Script Generation Module for AI Reel Automation.
Generates engaging video scripts based on keywords and styles.
"""

import random
from utils import logger


class ScriptGenerator:
    """Generate video scripts with various styles."""
    
    # Script templates by style - NOW DESIGNED FOR 20-25 SECONDS
    TEMPLATES = {
        'motivational': [
            "Breaking News: {keyword}? Your life is about to change. Here's why {keyword_short} is INCREDIBLE: {fact}. But wait, there's more! {insight}. Did you know? Most people never discover this. {benefit_detail}. This is REVOLUTIONARY. This is WHY we need {action}. Don't miss out. Follow for more life-changing content!",
            "ALERT: {keyword} can literally {action}! {fact}. Here's the science: {insight}. This changes EVERYTHING you know. {benefit_detail}. The results? AMAZING. People are SHOCKED. Tag someone who NEEDS this. Share this with everyone NOW!",
            "Stop wasting time without knowing this: {keyword}. {fact}. Think about it: {insight}. {benefit_detail}. This is the FUTURE. Your competitors know this already. You need to catch up. This will TRANSFORM you. Follow immediately!",
            "{keyword}? Game. Changer. {fact}. Let me explain why: {insight}. {benefit_detail}. This is not hype. This is REAL. Scientists confirm this. Experts agree. This is your moment. This is your chance. Don't wait!",
            "What if {keyword} could {benefit}? {fact}. Actually, it CAN! {insight}. Here's proof: {benefit_detail}. This is revolutionary. This is powerful. This is exactly what you've been searching for. Your success starts HERE!"
        ],
        'educational': [
            "Let's talk about {keyword} - this is actually fascinating. {fact}. Here's how it works: {insight}. You see, {benefit_detail}. The mechanism is simple: {action}. This is crucial knowledge. Understanding {keyword_short} changes your perspective. This is why experts say {keyword} is essential. Learn more!",
            "{keyword} explained scientifically: {fact}. Breaking it down: {insight}. The key understanding here is {benefit_detail}. Why does this matter? Because {action}. This knowledge is power. Students need to know this. Workers need to know this. Everyone needs to know this!",
            "Science lesson about {keyword}: {fact}. Here's the explanation: {insight}. The interesting part? {benefit_detail}. This relates to {action}. This is important because {keyword_short} affects your daily life. Understanding this makes you more informed. Share this knowledge!",
            "Deep dive into {keyword}: {fact}. The research shows: {insight}. Consider this angle: {benefit_detail}. This connects to {action}. The takeaway? {keyword} is more important than most people think. Knowledge is power. You now have the knowledge!",
            "Understanding {keyword} in 2026: {fact}. Modern science says: {insight}. Here's why it matters: {benefit_detail}. The connection? {action}. This is contemporary knowledge. This is relevant NOW. This shapes our future. Remember this!"
        ],
        'entertaining': [
            "OMG wait for the end... {keyword} is MORE insane than you think! {fact}. You won't BELIEVE what happens next: {insight}. {benefit_detail}. This is WILD. This is CRAZY. This is absolutely mind-blowing. Your reaction: SHOCKED. Your next move: SHARE THIS!",
            "POV: You just discovered {keyword}. {fact}. Your mind right now: EXPLODING. {insight}. {benefit_detail}. This is insane. What just happened? Your perspective just changed. You're different now. You can never unsee this. Tag your friends!",
            "They don't WANT you to know about {keyword}! {fact}. But here's the SECRET: {insight}. {benefit_detail}. The truth? {action}. This is HUGE. This is EARTH-SHATTERING. This is the plot twist of the century. SHARE before this gets hidden!",
            "{keyword} TIER RANKING: {fact}. Rating: {insight}. {benefit_detail}. Verdict? {action}. This is PEAK content. This is ENTERTAINMENT. This is what you came for. Comment your take! Tell me in the replies!",
            "I tested {keyword} for real... {fact}. What happened? {insight}. Results? {benefit_detail}. Conclusion: {action}. This ACTUALLY works. Would I recommend? 100%. Is this worth your time? ABSOLUTELY. Watch till the end!"
        ],
        'trending': [
            "#1 TRENDING NOW: {keyword}. {fact}. Why is this EVERYWHERE? {insight}. The real story: {benefit_detail}. Impact: {action}. This is the topic of the moment. Everyone is talking about this. You NEED to understand this. Stay informed!",
            "VIRAL ALERT: {keyword} is spreading FAST. {fact}. Here's why it matters: {insight}. The significance: {benefit_detail}. What it means: {action}. This is currently trending. This is THIS WEEK'S biggest story. Don't fall behind. Follow for updates!",
            "BREAKING: {keyword} news that's SHOCKING! {fact}. The implications: {insight}. What experts say: {benefit_detail}. The bottom line: {action}. This is URGENT. This is HAPPENING NOW. This affects you. This is relevant TODAY. React now!",
            "{keyword} is EXPLODING right now — here's why: {fact}. The trend analysis: {insight}. What's driving it: {benefit_detail}. The prediction: {action}. This momentum is REAL. This is the hottest topic. This is what's HOT in {keyword_short}. Join the conversation!",
            "HOTTEST TOPIC: {keyword} — everyone's discussing this. {fact}. Context: {insight}. Real talk: {benefit_detail}. The verdict: {action}. This is the conversation of the hour. This is CURRENT. This is LIVE. This is HAPPENING. Comment NOW!"
        ]
    }
    
    # Extended keyword-specific facts and insights - FOR LONGER SCRIPTS
    KEYWORD_DATA = {
        'tree': {
            'facts': [
                'one mature tree can absorb CO2 equivalent to driving a car for 26,000 miles',
                'trees provide oxygen for two people per year',
                'a single tree can filter multiple tons of pollutants from the air',
                'the oldest tree is over 5,000 years old',
                'trees store 3 times more carbon than shrubs',
                'forests cover 31% of Earth but are rapidly disappearing',
                'tree roots prevent soil erosion and save millions in infrastructure'
            ],
            'insights': [
                'one tree creates a ripple effect through entire ecosystems',
                'trees are literally the lungs of our planet',
                'planting trees today saves future generations',
                'nature designed the perfect carbon capture system',
                'green spaces increase property value by 15-20%',
                'forest therapy reduces stress by up to 37%',
                'every single tree matters for biodiversity'
            ],
            'actions': ['absorbs carbon dioxide', 'purifies the air', 'provides shelter', 'creates ecosystems', 'prevents erosion', 'cools the planet'],
            'benefits': ['clean air for 2 people', 'natural shade and cooling', 'habitat for wildlife', 'reduced air pollution', 'massive environmental impact', 'long-term health benefits'],
            'benefit_details': [
                'trees actively combat climate change by absorbing greenhouse gases',
                'they provide immense health benefits through shade and improved air quality',
                'forests sustain 80% of land animals and support biodiversity',
                'urban trees increase quality of life and mental wellbeing significantly',
                'tree planting prevents soil degradation and protects water sources',
                'green cover reduces urban heat island effect by up to 8 degrees'
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
                'transportation accounts for 27% of global emissions'
            ],
            'insights': [
                'every small action compounds into massive global change',
                'sustainability is not optional anymore',
                'nature provides everything we need',
                'we need urgent collective action',
                'your choices directly impact the planet',
                'the time for action is literally NOW',
                'environmental protection is self-preservation'
            ],
            'actions': ['changes daily', 'affects every living thing', 'requires immediate action', 'impacts your future', 'is calling for solutions'],
            'benefits': ['breathable air', 'clean water supply', 'sustainable future', 'thriving biodiversity', 'stable climate', 'healthy ecosystems'],
            'benefit_details': [
                'environmental action creates cascading effects across all ecosystems and human welfare',
                'protecting the planet secures resources and wellbeing for future generations',
                'sustainability is the blueprint for surviving and thriving long-term',
                'every environmental choice multiplies impacts across communities and continents',
                'green initiatives create economic opportunities and innovation breakthroughs',
                'conscious environmental practices preserve the beauty and resources we cherish'
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
                'stress management extends life expectancy by 10+ years'
            ],
            'insights': [
                'your body is an incredible machine that heals itself',
                'small daily habits create massive life transformations',
                'consistency beats intensity every single time',
                'prevention is infinitely better than treatment',
                'taking care of yourself is the best investment',
                'health is truly wealth in every dimension',
                'your future self will thank you for starting today'
            ],
            'actions': ['transforms your entire life', 'starts with today', 'changes everything forever', 'is absolutely possible', 'begins right now'],
            'benefits': ['boundless energy', 'mental clarity', 'emotional peace', 'physical strength', 'longevity', 'confidence and joy'],
            'benefit_details': [
                'health practices compound over time creating exponential benefits for your future',
                'prioritizing wellness is the single best investment you can make',
                'consistent health habits rebuild your body and mind at cellular levels',
                'better health unlocks potential you never knew existed within yourself',
                'wellness practices reduce disease risk while maximizing quality of life',
                'taking care of yourself validates your worth and enables greatness'
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
                'entrepreneurship teaches you life lessons'
            ],
            'insights': [
                'success leaves detailed clues',
                'your mindset determines your ceiling',
                'action beats perfect planning',
                'every failure is premium education',
                'you can scale beyond your wildest dreams',
                'the opportunity window is NOW',
                'your network truly equals your net worth'
            ],
            'actions': ['creates wealth systems', 'builds generational wealth', 'transforms financial reality', 'scales infinitely', 'opens unlimited possibilities'],
            'benefits': ['financial freedom', 'personal independence', 'passive income streams', 'unlimited earning potential', 'time flexibility', 'legacy building'],
            'benefit_details': [
                'business success creates wealth that extends far beyond individual circumstances',
                'entrepreneurship builds assets that generate income while you sleep or travel',
                'financial independence enables freedom to pursue your passions and purpose',
                'business knowledge becomes your most valuable and transferable asset',
                'success systems replicate and scale creating exponential growth trajectories',
                'building enterprise creates employment and value for entire ecosystems'
            ]
        }
    }
    
    @staticmethod
    def generate(keyword, style='motivational', length='short'):
        """
        Generate a script based on keyword and style.
        
        Args:
            keyword (str): Main topic for the script
            style (str): Style of script (motivational, educational, entertaining, trending)
            length (str): Length preset (short, medium, long)
            
        Returns:
            dict: Script data with text, hook, and metadata
        """
        try:
            logger.info(f"Generating script: keyword='{keyword}', style='{style}'")
            
            # Get style template (fallback to motivational if not found)
            style_lower = style.lower()
            if style_lower not in ScriptGenerator.TEMPLATES:
                logger.warning(f"Style '{style}' not found, using 'motivational'")
                style_lower = 'motivational'
            
            templates = ScriptGenerator.TEMPLATES[style_lower]
            template = random.choice(templates)
            
            # Get keyword data or use defaults
            keyword_lower = keyword.lower()
            if keyword_lower not in ScriptGenerator.KEYWORD_DATA:
                # Find closest match by substring
                for key in ScriptGenerator.KEYWORD_DATA:
                    if key in keyword_lower or keyword_lower in key:
                        keyword_lower = key
                        break
            
            keyword_data = ScriptGenerator.KEYWORD_DATA.get(
                keyword_lower,
                ScriptGenerator.KEYWORD_DATA['tree']  # Default fallback
            )
            
            # Extract components
            fact = random.choice(keyword_data['facts'])
            insight = random.choice(keyword_data['insights'])
            action = random.choice(keyword_data['actions'])
            benefit = random.choice(keyword_data['benefits'])
            benefit_detail = random.choice(keyword_data.get('benefit_details', keyword_data['benefits']))
            
            keyword_short = keyword.split()[0] if len(keyword.split()) > 1 else keyword
            
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
            
            # Create hook (first 10-15 words for big text overlay)
            words = script.split()
            hook = ' '.join(words[:3])
            if len(hook) < 5:
                hook = ' '.join(words[:5])
            
            result = {
                'script': script,
                'hook': hook,
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
                'keyword': keyword,
                'style': style,
                'length': length
            }


def generate_script(keyword, style='motivational', length='short'):
    """Convenience function to generate a script."""
    return ScriptGenerator.generate(keyword, style, length)
