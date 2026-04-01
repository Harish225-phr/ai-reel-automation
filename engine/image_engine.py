"""
Image-to-Video Engine for AI Reel Automation.
Converts static images into attractive video clips with animations.

Features:
- Zoom-in effect (Ken Burns style)
- Pan effects (left-right, top-bottom)
- Fade transitions
- Crop to vertical format (1080x1920)
"""

import os
import numpy as np
from pathlib import Path
from PIL import Image
import tempfile
from moviepy.editor import ImageClip, concatenate_videoclips, vfx, ColorClip
from utils import logger
import config

# Pillow 10+ compatibility: Patch Image.ANTIALIAS to work with Pillow 11
try:
    Image.ANTIALIAS = Image.Resampling.LANCZOS
except AttributeError:
    # Already has ANTIALIAS (Pillow <10)
    pass


class ImageEngine:
    """Convert images to animated video clips."""
    
    @staticmethod
    def resize_image_to_vertical(image_path, width=config.VIDEO_WIDTH, height=config.VIDEO_HEIGHT):
        """
        Resize and crop image to vertical format (1080x1920).
        
        Strategies:
        1. If image is landscape: Center crop to vertical
        2. If image is portrait: Resize to fit
        3. Add black borders if needed for aspect ratio
        """
        try:
            img = Image.open(image_path)
            original_w, original_h = img.size
            
            target_aspect = width / height  # 1080/1920 = 0.5625
            original_aspect = original_w / original_h
            
            if original_aspect > target_aspect:
                # Image is wider than target - crop horizontally
                new_w = int(original_h * target_aspect)
                left = (original_w - new_w) // 2
                img = img.crop((left, 0, left + new_w, original_h))
            else:
                # Image is taller than target - crop vertically
                new_h = int(original_w / target_aspect)
                top = (original_h - new_h) // 2
                img = img.crop((0, top, original_w, top + new_h))
            
            # Resize to exact dimensions
            img = img.resize((width, height))
            
            return img
            
        except Exception as e:
            logger.warning(f"[IMAGE] Error resizing {image_path}: {e}")
            return None
    
    @staticmethod
    def create_image_video_clip(
        image_path,
        duration=3.0,
        effect='static',
        fade_in=0.5,
        fade_out=0.5
    ):
        """
        Create video clip from image - SIMPLE, MINIMAL approach.
        Pre-resized PIL images → ImageClip → fade → done.
        """
        try:
            # Resize image to vertical format using PIL (simpler)
            img = ImageEngine.resize_image_to_vertical(image_path)
            if img is None:
                return None
            
            # Save to temp
            temp_path = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
            img.save(temp_path)
            
            # Create image clip from pre-resized PIL image
            # Convert PIL image directly to ImageClip
            clip = ImageClip(temp_path)
            clip = clip.set_duration(duration)
            
            # Apply fades
            if fade_in > 0:
                try:
                    clip = clip.fadein(fade_in)
                except:
                    pass
            
            if fade_out > 0:
                try:
                    clip = clip.fadeout(fade_out)
                except:
                    pass
            
            logger.debug(f"[IMAGE] ✓ Created clip: {duration:.1f}s")
            return clip
            
        except Exception as e:
            logger.error(f"[IMAGE] Error clip creation: {e}")
            return None
    
    @staticmethod
    def images_to_video_base(image_paths, total_duration, effect='static'):
        """
        Convert images to video - SIMPLE & RELIABLE.
        """
        try:
            if not image_paths:
                logger.warning("[IMAGE] No images provided")
                return ColorClip(
                    size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT),
                    color=(0, 0, 0)
                ).set_duration(total_duration)
            
            per_image_duration = total_duration / len(image_paths)
            logger.info(f"[IMAGE] {len(image_paths)} images → {per_image_duration:.2f}s each video")
            
            clips = []
            for idx, img_path in enumerate(image_paths):
                if not os.path.exists(img_path):
                    logger.warning(f"[IMAGE] Skip: {img_path}")
                    continue
                
                # Simple: create clip with minimal fades
                clip = ImageEngine.create_image_video_clip(
                    img_path,
                    duration=per_image_duration,
                    effect='static',
                    fade_in=0.2,
                    fade_out=0.2
                )
                
                if clip:
                    clips.append(clip)
                    logger.debug(f"[IMAGE] Image {idx+1}: ✓")
            
            if not clips:
                logger.warning("[IMAGE] No clips created")
                return ColorClip(
                    size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT),
                    color=(0, 0, 0)
                ).set_duration(total_duration)
            
            # Simple concatenation
            video = concatenate_videoclips(clips)
            video = video.subclip(0, total_duration)
            
            logger.info(f"[IMAGE] Video created: {video.duration:.1f}s")
            return video
            
        except Exception as e:
            logger.error(f"[IMAGE] Error base creation: {e}")
            return ColorClip(
                size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT),
                color=(0, 0, 0)
            ).set_duration(total_duration)
    
    @staticmethod
    def find_images_for_keyword(keyword, image_dir='images', max_count=10):
        """
        Find relevant images for keyword.
        
        Strategy:
        1. Look for images with keyword in filename
        2. Fall back to any available images
        3. Return list of paths
        """
        try:
            image_path = Path(image_dir)
            if not image_path.exists():
                logger.warning(f"[IMAGE] Directory not found: {image_dir}")
                return []
            
            # Get supported image extensions
            extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
            
            # Strategy 1: Exact keyword match
            keyword_lower = keyword.lower()
            matching_images = []
            
            for img_file in image_path.glob('*'):
                if img_file.suffix.lower() in extensions:
                    if keyword_lower in img_file.stem.lower():
                        matching_images.append(str(img_file))
            
            if matching_images:
                logger.info(f"[IMAGE] Found {len(matching_images)} images for '{keyword}'")
                return sorted(matching_images)[:max_count]
            
            # Strategy 2: Get first available images
            all_images = []
            for img_file in sorted(image_path.glob('*')):
                if img_file.suffix.lower() in extensions:
                    all_images.append(str(img_file))
            
            if all_images:
                logger.info(f"[IMAGE] Using {min(max_count, len(all_images))} generic images")
                return all_images[:max_count]
            
            logger.warning(f"[IMAGE] No images found in {image_dir}")
            return []
            
        except Exception as e:
            logger.error(f"[IMAGE] Error finding images: {e}")
            return []
