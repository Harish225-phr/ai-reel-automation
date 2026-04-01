"""
AI-Powered Script Engine using HuggingFace API
Generates professional, non-repetitive Instagram reel scripts
Supports Hindi and English
"""

import os
import re
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)

HAS_HUGGINGFACE = False  # Disable for production stability
HAS_INTERNET = True


class ScriptCleaner:
    """Clean and optimize generated scripts."""
    
    @staticmethod
    def remove_repetition(sentences: List[str]) -> List[str]:
        """Remove repeated words and phrases within and between sentences."""
        cleaned = []
        
        for sentence in sentences:
            # Remove repeated words (e.g., "very very" → "very")
            words = sentence.split()
            unique_words = []
            prev_word = None
            
            for word in words:
                if word.lower() != prev_word:
                    unique_words.append(word)
                    prev_word = word.lower()
            
            cleaned_sentence = ' '.join(unique_words)
            cleaned.append(cleaned_sentence)
        
        # Remove duplicate sentences
        unique_sentences = []
        seen = set()
        
        for sentence in cleaned:
            sentence_lower = sentence.lower().strip()
            if sentence_lower not in seen:
                unique_sentences.append(sentence)
                seen.add(sentence_lower)
        
        return unique_sentences
    
    @staticmethod
    def trim_long_sentences(sentences: List[str], max_length: int = 150) -> List[str]:
        """Trim sentences that are too long for subtitle display."""
        trimmed = []
        
        for sentence in sentences:
            if len(sentence) > max_length:
                # Try to split at natural boundaries
                parts = re.split(r'(?<=[.!?])\s+', sentence)
                for part in parts:
                    if part.strip():
                        trimmed.append(part.strip())
            else:
                trimmed.append(sentence)
        
        return trimmed
    
    @staticmethod
    def clean_script(script: str) -> List[str]:
        """
        Clean entire script:
        1. Split into sentences
        2. Remove repetition
        3. Trim long sentences
        
        Returns:
            List of clean sentences
        """
        # Split into sentences - include Hindi punctuation
        # ।  = Devanagari danda (Hindi period)
        sentences = re.split(r'(?<=[.!?\u0964।])\s+', script.strip())
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Remove repetition
        sentences = ScriptCleaner.remove_repetition(sentences)
        
        # Trim long sentences
        sentences = ScriptCleaner.trim_long_sentences(sentences)
        
        # Ensure max 6 sentences for reel
        return sentences[:6]


class HuggingFaceScriptGenerator:
    """Generate scripts using HuggingFace Mistral model."""
    
    HINDI_PROMPT_TEMPLATE = """You are a professional Instagram reel script writer for Hindi content.

Write a 25-second Instagram reel script about: {keyword}

Rules:
- No repetition of words or phrases
- Short, punchy sentences (8-12 words max)
- Natural, conversational Hindi tone
- Motivational storytelling style
- Professional and engaging

Structure:
1. Hook question (surprising or curiosity-driven)
2. First benefit
3. Second benefit
4. Third benefit
5. One emotional line (inspiring, powerful)
6. Call to action (motivational)

Return ONLY the script, 5-6 sentences, no numbering, no extra text.
Separate each sentence with a period and space."""

    ENGLISH_PROMPT_TEMPLATE = """You are a professional Instagram reel script writer.

Write a 25-second Instagram reel script about: {keyword}

Rules:
- No repetition of words or phrases
- Short, punchy sentences (8-12 words max)
- Natural, conversational English tone
- Motivational storytelling style
- Professional and engaging

Structure:
1. Hook question (surprising or curiosity-driven)
2. First benefit
3. Second benefit
4. Third benefit
5. One emotional line (inspiring, powerful)
6. Call to action (motivational)

Return ONLY the script, 5-6 sentences, no numbering, no extra text.
Separate each sentence with a period and space."""

    def __init__(self):
        """Initialize generator."""
        self.use_huggingface = HAS_HUGGINGFACE
        self.pipeline = None
        
        if self.use_huggingface:
            try:
                logger.info("[SCRIPT] Loading HuggingFace Mistral model (CPU mode)...")
                self.pipeline = pipeline(
                    "text-generation",
                    model="mistralai/Mistral-7B-Instruct-v0.2",
                    device=-1  # CPU mode
                )
                logger.info("[SCRIPT] ✓ HuggingFace model loaded successfully")
            except Exception as e:
                logger.warning(f"[SCRIPT] HuggingFace init failed: {e}. Using fallback.")
                logger.warning(f"[SCRIPT] Error details: {type(e).__name__}")
                self.use_huggingface = False
    
    def generate(self, keyword: str, language: str = 'english') -> Tuple[str, List[str]]:
        """
        Generate script using HuggingFace API.
        
        Args:
            keyword (str): Topic for the script
            language (str): 'english' or 'hindi'
            
        Returns:
            Tuple of (full_script, list_of_sentences)
        """
        
        # Select template based on language
        prompt_template = (
            self.HINDI_PROMPT_TEMPLATE if language == 'hindi'
            else self.ENGLISH_PROMPT_TEMPLATE
        )
        
        prompt = prompt_template.format(keyword=keyword)
        
        if self.use_huggingface and self.pipeline:
            try:
                logger.info(f"[SCRIPT] Generating {language} script with HuggingFace: {keyword}")
                
                # Generate with Mistral
                outputs = self.pipeline(
                    prompt,
                    max_new_tokens=200,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    return_full_text=False
                )
                
                script = outputs[0]["generated_text"].strip()
                logger.info(f"[SCRIPT] ✓ Generated (HuggingFace): {len(script)} chars")
                
            except Exception as e:
                logger.warning(f"[SCRIPT] HuggingFace generation failed: {e}. Using fallback.")
                script = self._generate_fallback(keyword, language)
        else:
            logger.info(f"[SCRIPT] Using fallback generator for: {keyword}")
            script = self._generate_fallback(keyword, language)
        
        # Clean script
        sentences = ScriptCleaner.clean_script(script)
        
        # Ensure we have at least 4 sentences
        if len(sentences) < 4:
            logger.warning(f"[SCRIPT] Only {len(sentences)} sentences generated. Using fallback.")
            script = self._generate_fallback(keyword, language)
            sentences = ScriptCleaner.clean_script(script)
        
        # Log sentences
        full_script = ' '.join(sentences)
        logger.info(f"[SCRIPT] Final: {len(sentences)} sentences, {len(full_script)} chars")
        for i, sent in enumerate(sentences, 1):
            logger.info(f"  {i}. {sent[:60]}...")
        
        return full_script, sentences
    
    def _generate_fallback(self, keyword: str, language: str = 'english') -> str:
        """
        Fallback script generation when HuggingFace is unavailable.
        Uses template-based approach - returns individual sentences.
        """
        
        if language == 'hindi':
            sentences = [
                f"क्या आप जानते हैं कि {keyword} आपके जीवन को बदल सकता है?",
                f"पहला फायदा: {keyword} से आपकी ऊर्जा बढ़ती है।",
                f"दूसरा लाभ: {keyword} आपके मन को शांत करता है।",
                f"तीसरा: {keyword} से आप अपने लक्ष्य हासिल कर सकते हैं।",
                f"लेकिन याद रखें, {keyword} का सच्चा फायदा पाने के लिए निरंतरता ज़रूरी है।",
                f"तो आज ही शुरू करें और अपने सपनों को सच करने का यह सही समय है।"
            ]
        else:
            sentences = [
                f"Do you know what {keyword} can really do for you?",
                f"First, {keyword} gives you incredible energy.",
                f"Second, {keyword} brings clarity and deep peace.",
                f"Third, {keyword} helps you achieve your biggest goals.",
                f"But remember, the real power of {keyword} comes from consistency.",
                f"Start today. This is your moment to transform."
            ]
        
        # Join with proper spacing
        script = ' '.join(sentences)
        return script


class ScriptEngine:
    """Main script generation engine."""
    
    def __init__(self):
        """Initialize script engine."""
        self.generator = HuggingFaceScriptGenerator()
    
    def generate(self, keyword: str, language: str = 'english') -> Tuple[str, List[str]]:
        """
        Generate complete script.
        
        Args:
            keyword (str): Topic
            language (str): 'english' or 'hindi'
            
        Returns:
            Tuple of (full_script, sentences)
        """
        return self.generator.generate(keyword, language)
    
    def split_script(self, script: str) -> List[str]:
        """Split script into sentences."""
        return ScriptCleaner.clean_script(script)
