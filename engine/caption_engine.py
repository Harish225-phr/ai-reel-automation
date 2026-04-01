"""
Caption Engine for Professional AI Reel Automation.
Renders professional subtitles, hooks, and CTA overlays.
"""

import os
from PIL import Image, ImageDraw, ImageFont
from utils import logger
import config

# Pillow 10+ compatibility: Patch Image.ANTIALIAS to work with Pillow 11
try:
    Image.ANTIALIAS = Image.Resampling.LANCZOS
except AttributeError:
    # Already has ANTIALIAS (Pillow <10)
    pass


class CaptionEngine:
    """Generate professional caption and text overlays."""
    
    @staticmethod
    def load_font(font_size):
        """
        Try to load a good font, with fallbacks for different systems.
        Prioritizes bold fonts for better visibility.
        """
        # Font priority (Windows)
        font_paths = [
            "C:\\Windows\\Fonts\\ariblk.ttf",    # Arial Black (best for hooks)
            "C:\\Windows\\Fonts\\arial.ttf",     # Arial
            "C:\\Windows\\Fonts\\calibrib.ttf",  # Calibri Bold
            "C:\\Windows\\Fonts\\verdanab.ttf",  # Verdana Bold
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
            "/System/Library/Fonts/Helvetica.ttc",  # macOS
        ]
        
        # Try each path
        for font_path in font_paths:
            try:
                if os.path.exists(font_path):
                    return ImageFont.truetype(font_path, font_size)
            except:
                pass
        
        # Fallback: generic names
        try:
            return ImageFont.truetype("arial", font_size)
        except:
            pass
        
        # Last resort: default
        logger.debug(f"[FONT] Using default for size {font_size}")
        return ImageFont.load_default()
    
    @staticmethod
    def create_hook(text, width=1080, height=1920):
        """
        Create professional hook overlay (first 3 seconds).
        Big bold text with semi-transparent background.
        """
        try:
            img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Load bold font
            font_size = config.HOOK_FONT_SIZE
            font = CaptionEngine.load_font(font_size)
            
            # Word wrap
            words = text.split()
            lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                test_line = ' '.join(current_line)
                bbox = draw.textbbox((0, 0), test_line, font=font)
                if bbox[2] - bbox[0] > width - 80:
                    if len(current_line) > 1:
                        current_line.pop()
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(test_line)
                        current_line = []
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Create semi-transparent dark overlay
            overlay = Image.new('RGBA', (width, height), (0, 0, 0, 150))
            
            # Calculate text center
            total_height = len(lines) * (font_size + 20)
            start_y = (height - total_height) // 2
            
            # Draw text
            y_offset = start_y
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                line_width = bbox[2] - bbox[0]
                x_center = (width - line_width) // 2
                
                # Shadow
                draw.text((x_center + 3, y_offset + 3), line, font=font, fill=(0, 0, 0, 200))
                # Main text (bright yellow)
                draw.text((x_center, y_offset), line, font=font, fill=(255, 255, 100, 255))
                
                y_offset += font_size + 20
            
            # Composite
            result = Image.alpha_composite(overlay, img)
            logger.debug(f"[CAPTION] Created hook: {len(lines)} lines")
            return result
            
        except Exception as e:
            logger.warning(f"Error creating hook: {e}")
            return None
    
    @staticmethod
    def create_caption(text, width=1080, height=200):
        """
        Create professional subtitle overlay (bottom center).
        Semi-transparent background with white text.
        """
        try:
            img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Load font
            font_size = config.CAPTION_FONT_SIZE
            font = CaptionEngine.load_font(font_size)
            
            # Word wrap
            words = text.split()
            lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                test_line = ' '.join(current_line)
                bbox = draw.textbbox((0, 0), test_line, font=font)
                if bbox[2] - bbox[0] > width - 40:
                    if len(current_line) > 1:
                        current_line.pop()
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(test_line)
                        current_line = []
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Calculate height needed
            total_height = len(lines) * (font_size + 10) + 20
            
            # Create background
            bg_img = Image.new('RGBA', (width, total_height), (0, 0, 0, config.TEXT_BG_OPACITY))
            bg_draw = ImageDraw.Draw(bg_img)
            
            # Draw text on background
            y_offset = 10
            for line in lines:
                # Shadow
                bg_draw.text((22, y_offset + 2), line, font=font, fill=(0, 0, 0, 200))
                # Main text (white)
                bg_draw.text((20, y_offset), line, font=font, fill=(255, 255, 255, 255))
                y_offset += font_size + 10
            
            logger.debug(f"[CAPTION] Created subtitle: {len(lines)} lines")
            return bg_img
            
        except Exception as e:
            logger.warning(f"Error creating caption: {e}")
            return None
    
    @staticmethod
    def create_cta(text, width=1080, height=300):
        """
        Create professional Call-To-Action overlay (last 2 seconds).
        """
        try:
            img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            font_size = config.CTA_FONT_SIZE
            font = CaptionEngine.load_font(font_size)
            
            # Center text
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            x_center = (width - text_width) // 2
            y_center = (height // 2) - (font_size // 2)
            
            # Background
            bg_color = (220, 50, 80, 200)  # Red-ish
            padding = 20
            bg_bbox = [x_center - padding, y_center - padding, 
                      x_center + text_width + padding, y_center + font_size + padding]
            draw.rectangle(bg_bbox, fill=bg_color)
            
            # Text
            draw.text((x_center, y_center), text, font=font, fill=(255, 255, 255, 255))
            
            logger.debug(f"[CAPTION] Created CTA: {text}")
            return img
            
        except Exception as e:
            logger.warning(f"Error creating CTA: {e}")
            return None
