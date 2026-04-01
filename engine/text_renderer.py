"""
PIL-based text rendering for video overlays (no ImageMagick needed)
This module creates text images using PIL and converts them to video clips.
"""

import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy.editor import ImageClip, TextClip
import logging

logger = logging.getLogger(__name__)

class PILTextRenderer:
    """Render text to images using PIL instead of MoviePy's TextClip (which needs ImageMagick)"""
    
    def __init__(self, width=1080, height=1920):
        self.width = width
        self.height = height
        self.temp_dir = "content/temp_text"
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Try to load a good font, fall back to default
        self.font_large = self._load_font(size=60)
        self.font_medium = self._load_font(size=48)
        self.font_small = self._load_font(size=36)
    
    def _load_font(self, size=48):
        """Load font with fallback"""
        font_paths = [
            "C:\\Windows\\Fonts\\arial.ttf",
            "C:\\Windows\\Fonts\\ArialBD.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/System/Library/Fonts/Arial.ttf",
        ]
        
        for path in font_paths:
            try:
                if os.path.exists(path):
                    return ImageFont.truetype(path, size)
            except:
                pass
        
        # Fallback to default
        try:
            return ImageFont.load_default()
        except:
            return None
    
    def _wrap_text(self, text, max_width=900, font=None):
        """Wrap text to fit within max_width"""
        if not font or not hasattr(font, 'getbbox'):
            # Can't measure text with default font, just add newlines
            words = text.split()
            lines = []
            current_line = []
            for word in words:
                if len(' '.join(current_line + [word])) > 60:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    current_line.append(word)
            if current_line:
                lines.append(' '.join(current_line))
            return '\n'.join(lines)
        
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            text_width = bbox[2] - bbox[0]
            
            if text_width > max_width and current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                current_line.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)
    
    def create_subtitle_clip(self, text, duration, start_time=0, font_size=48, color=(255, 255, 255)):
        """Create a subtitle as an ImageClip"""
        try:
            font = self.font_medium if font_size == 48 else self._load_font(size=font_size)
            wrapped_text = self._wrap_text(text, max_width=900, font=font)
            
            # Create image with text
            img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Get text bounding box to center it
            bbox = draw.textbbox((0, 0), wrapped_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Position at bottom with padding
            x = (self.width - text_width) // 2
            y = self.height - text_height - 100
            
            # Draw text with white color and black shadow for readability
            shadow_offset = 3
            draw.text((x + shadow_offset, y + shadow_offset), wrapped_text, 
                     font=font, fill=(0, 0, 0, 180))  # Black shadow
            draw.text((x, y), wrapped_text, font=font, fill=color + (255,))  # White text
            
            # Save temporary image
            temp_path = os.path.join(self.temp_dir, f"subtitle_{start_time:.2f}.png")
            img.save(temp_path, 'PNG')
            
            # Create ImageClip
            clip = ImageClip(temp_path).set_duration(duration).set_start(start_time)
            return clip
            
        except Exception as e:
            logger.error(f"Error creating subtitle clip: {e}")
            return None
    
    def create_hook_clip(self, text, duration, hook_type="top", color=(255, 215, 0)):
        """Create a hook/title text clip"""
        try:
            font = self.font_large
            wrapped_text = self._wrap_text(text, max_width=900, font=font)
            
            # Create image
            img = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Get text bounding box
            bbox = draw.textbbox((0, 0), wrapped_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Position based on type
            x = (self.width - text_width) // 2
            if hook_type == "top":
                y = 100
            elif hook_type == "center":
                y = (self.height - text_height) // 2
            else:  # bottom
                y = self.height - text_height - 100
            
            # Draw text with golden color and shadow
            shadow_offset = 4
            draw.text((x + shadow_offset, y + shadow_offset), wrapped_text, 
                     font=font, fill=(0, 0, 0, 200))  # Black shadow
            draw.text((x, y), wrapped_text, font=font, fill=color + (255,))  # Golden text
            
            # Save temporary image
            temp_path = os.path.join(self.temp_dir, f"hook_{hook_type}.png")
            img.save(temp_path, 'PNG')
            
            # Create ImageClip
            clip = ImageClip(temp_path).set_duration(duration)
            return clip
            
        except Exception as e:
            logger.error(f"Error creating hook clip: {e}")
            return None
    
    def cleanup(self):
        """Clean up temporary image files"""
        try:
            import shutil
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
        except:
            pass
