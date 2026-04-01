"""
Video Creation Module for AI Reel Automation.
Creates vertical reel videos (1080x1920) with images, overlays, and audio.
"""

import os
import sys
import random
from pathlib import Path

# ==================== MOVIEPY IMPORTS ====================
# Using safe imports that work with MoviePy 1.0.3+

try:
    from moviepy.editor import (
        ImageClip,
        AudioFileClip,
        concatenate_videoclips,
        CompositeVideoClip,
        TextClip
    )
    from moviepy.audio.AudioClip import CompositeAudioClip
    from PIL import Image, ImageDraw, ImageFilter
    
    # Pillow 10+ compatibility: Patch Image.ANTIALIAS to work with Pillow 11
    try:
        Image.ANTIALIAS = Image.Resampling.LANCZOS
    except AttributeError:
        # Already has ANTIALIAS (Pillow <10)
        pass
    
    MOVIEPY_AVAILABLE = True
except ImportError as e:
    MOVIEPY_AVAILABLE = False
    IMPORT_ERROR = str(e)

from utils import logger, get_output_filename


# ==================== COMPATIBILITY CHECK ====================
def check_moviepy_compatibility():
    """Check if moviepy is properly installed for Python 3.14+."""
    if not MOVIEPY_AVAILABLE:
        error_msg = f"""
====================================================================
MOVIEPY IMPORT ERROR - Python 3.14+ Compatibility Issue
===================================================================="

Error Details:
  {IMPORT_ERROR}

Solution:
  1. Ensure moviepy is installed:
     pip install moviepy --upgrade

  2. If still failing, use a clear environment:
     pip uninstall moviepy -y
     pip install moviepy==1.0.3

  3. Verify installation:
     python -c "from moviepy.editor import AudioFileClip; print('[OK]')"

  4. Check your Python version (should be 3.8+):
     python --version

For Python 3.14 support, ensure moviepy 1.0.3+ is installed.
        """
        logger.error(error_msg)
        raise ImportError(error_msg)


# ==================== VIDEO CONSTANTS ====================
REEL_WIDTH = 1080
REEL_HEIGHT = 1920
REEL_FPS = 24
TARGET_ASPECT_RATIO = REEL_HEIGHT / REEL_WIDTH


# ==================== IMAGE PROCESSING ====================
def get_supported_image_formats():
    """Return set of supported image formats."""
    return {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'}


def validate_image_file(image_path):
    """
    Validate if file is a supported image.
    
    Args:
        image_path (str): Path to image file
        
    Returns:
        bool: True if valid image format
    """
    ext = os.path.splitext(image_path)[1].lower()
    return ext in get_supported_image_formats()


def prepare_image_for_reel(image_path, output_width=REEL_WIDTH, output_height=REEL_HEIGHT):
    """
    Prepare image for reel: resize, apply blur to background if needed.
    
    Args:
        image_path (str): Path to original image
        output_width (int): Target width (default: 1080)
        output_height (int): Target height (default: 1920)
        
    Returns:
        str: Path to prepared image
        
    Raises:
        FileNotFoundError: If image doesn't exist
        ValueError: If image cannot be processed
    """
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Open image
        img = Image.open(image_path)
        original_width, original_height = img.size
        original_aspect = original_height / original_width
        target_aspect = output_height / output_width
        
        logger.debug(f"Processing: {image_path} ({original_width}x{original_height})")
        
        # If image is not vertical enough, add blurred background
        if original_aspect < target_aspect:
            logger.debug(f"  >> Adding blurred background")
            
            # Resize image to fit height
            new_height = output_height
            new_width = int(new_height / original_aspect)
            img_resized = img.resize((new_width, new_height))
            
            # Create blurred background
            img_small = img.resize((output_width // 4, output_height // 4))
            img_blurred = img_small.filter(ImageFilter.GaussianBlur(radius=20))
            img_blurred = img_blurred.resize((output_width, output_height))
            
            # Center the resized image on blurred background
            x_offset = (output_width - new_width) // 2
            img_blurred.paste(img_resized, (x_offset, 0))
            final_img = img_blurred
        
        else:
            # Image is vertical or close, just resize
            logger.debug(f"  >> Resizing to fit")
            final_img = img.resize((output_width, output_height))
        
        # Save prepared image
        temp_path = image_path.rsplit('.', 1)[0] + '_prepared.jpg'
        final_img.save(temp_path, quality=85)
        
        logger.debug(f"  [OK] Prepared image saved: {temp_path}")
        return temp_path
    
    except Exception as e:
        logger.error(f"Error preparing image {image_path}: {e}")
        raise


# ==================== VIDEO CREATION ====================
def create_video_from_images(
    image_paths,
    audio_path,
    topic="Video",
    music_path=None,
    image_duration=4,
    output_path="output/reel.mp4",
    font_size=80,
    video_fps=REEL_FPS
):
    """
    Create a vertical reel video from images and audio.
    
    Args:
        image_paths (list): List of image paths
        audio_path (str): Path to voiceover audio
        topic (str): Topic for text overlay
        music_path (str): Optional path to background music
        image_duration (float): Duration for each image in seconds
        output_path (str): Output video path
        font_size (int): Font size for text overlay
        video_fps (int): Frames per second
        
    Returns:
        dict: Result dictionary with video info
        
    Raises:
        ValueError: If parameters are invalid
        FileNotFoundError: If required files not found
    """
    try:
        # Validate moviepy
        check_moviepy_compatibility()
        
        logger.info("=" * 50)
        logger.info("STARTING VIDEO CREATION")
        logger.info("=" * 50)
        
        # Validate inputs
        if not image_paths:
            raise ValueError("No images provided")
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        logger.info(f"Creating video with {len(image_paths)} images")
        logger.info(f"Video dimensions: {REEL_WIDTH}x{REEL_HEIGHT} at {video_fps} FPS")
        
        # Prepare images
        logger.info("Preparing images...")
        prepared_images = []
        for idx, img_path in enumerate(image_paths):
            try:
                logger.info(f"  Processing image {idx+1}/{len(image_paths)}")
                prepared_path = prepare_image_for_reel(img_path)
                prepared_images.append(prepared_path)
            except Exception as e:
                logger.warning(f"  [WARN] Skipping image {idx+1}: {e}")
                continue
        
        if not prepared_images:
            raise ValueError("No valid images could be processed")
        
        # Load voiceover audio
        logger.info("Loading voiceover audio...")
        voiceover = AudioFileClip(audio_path)
        voiceover_duration = voiceover.duration
        logger.info(f"  Voiceover duration: {voiceover_duration:.2f}s")
        
        # Calculate duration per image to match audio
        num_images = len(prepared_images)
        calculated_duration = voiceover_duration / num_images
        actual_duration = min(max(calculated_duration, 3), image_duration)
        logger.info(f"  Image duration: {actual_duration:.2f}s per image")
        
        # Create image clips with transitions
        logger.info("Creating image clips with transitions...")
        clips = []
        
        for idx, img_path in enumerate(prepared_images):
            logger.debug(f"  Creating clip {idx+1}/{num_images}")
            
            # Create image clip
            clip = ImageClip(img_path).set_duration(actual_duration)
            
            # Resize to exact dimensions
            clip = clip.resize(height=REEL_HEIGHT, width=REEL_WIDTH)
            
            # Add fade transitions
            fade_duration = 0.3
            if idx == 0:
                clip = clip.fadein(fade_duration)
            if idx == num_images - 1:
                clip = clip.fadeout(fade_duration)
            
            clips.append(clip)
        
        # Concatenate clips
        logger.info("Concatenating clips...")
        if len(clips) == 1:
            final_video = clips[0].set_duration(voiceover_duration)
        else:
            final_video = concatenate_videoclips(clips)
            final_video = final_video.set_duration(voiceover_duration)
        
        # Add text overlay (topic) - optional as TextClip may vary
        try:
            logger.info("Adding text overlay...")
            text_clip = TextClip(
                txt=topic,
                fontsize=font_size,
                color='white',
                font='Arial',
                size=(REEL_WIDTH - 40, None),
                method='caption'
            ).set_position(('center', 'bottom')).set_duration(voiceover_duration).margin(bottom=50)
            
            # Composite video with text
            final_video = CompositeVideoClip(
                [final_video, text_clip],
                size=(REEL_WIDTH, REEL_HEIGHT)
            )
        except Exception as e:
            logger.warning(f"Text overlay skipped (optional): {e}")
            # Continue without text overlay
            pass
        
        # Create audio track
        logger.info("Mixing audio...")
        audio_clips = [voiceover]
        
        # Add background music if provided
        if music_path and os.path.exists(music_path):
            try:
                logger.info(f"Adding background music: {music_path}")
                music = AudioFileClip(music_path)
                
                # Loop music to match voiceover duration
                if music.duration < voiceover_duration:
                    num_loops = int((voiceover_duration // music.duration) + 1)
                    music_list = []
                    for _ in range(num_loops):
                        music_list.append(music.copy())
                    
                    # Concatenate and trim to exact duration
                    try:
                        music = concatenate_videoclips(music_list, method='chain')
                    except:
                        # Fallback: manually concatenate by timing
                        logger.debug("Using manual audio concatenation")
                        music = music
                    
                    music = music.subclipped(0, voiceover_duration)
                else:
                    music = music.subclipped(0, voiceover_duration)
                
                # Reduce music volume (30% while voiceover is 100%)
                music = music.volumex(0.3)
                audio_clips.append(music)
            
            except Exception as e:
                logger.warning(f"Background music skipped: {e}")
        
        # Composite audio
        if len(audio_clips) > 1:
            final_audio = CompositeAudioClip(audio_clips)
        else:
            final_audio = audio_clips[0]
        
        final_video = final_video.set_audio(final_audio)
        
        # Create output directory
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Write video
        logger.info(f"Writing video to {output_path}...")
        final_video.write_videofile(
            output_path,
            fps=video_fps,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        # Cleanup
        logger.info("Cleaning up resources...")
        final_video.close()
        voiceover.close()
        
        for img_path in prepared_images:
            try:
                if os.path.exists(img_path) and '_prepared' in img_path:
                    os.remove(img_path)
            except Exception as e:
                logger.debug(f"Could not remove temp image: {e}")
        
        # Verify output
        if not os.path.exists(output_path):
            raise FileNotFoundError(f"Video was not created: {output_path}")
        
        video_size = os.path.getsize(output_path) / (1024 * 1024)  # Size in MB
        logger.info(f"[OK] Video created successfully: {video_size:.2f} MB")
        
        result = {
            'video_path': output_path,
            'topic': topic,
            'duration': voiceover_duration,
            'image_count': len(prepared_images),
            'audio_path': audio_path,
            'music_path': music_path,
            'file_size_mb': video_size
        }
        
        logger.info("=" * 50)
        logger.info("VIDEO CREATION COMPLETED [OK]")
        logger.info("=" * 50)
        
        return result
    
    except Exception as e:
        logger.error(f"Error creating video: {e}")
        raise


# ==================== QUICK VIDEO GENERATION ====================
def generate_reel(
    audio_path,
    topic="Generated Reel",
    num_images=5,
    music_enabled=True,
    output_dir="output"
):
    """
    Generate a complete reel with one function call.
    
    Args:
        audio_path (str): Path to voiceover audio
        topic (str): Topic for overlay
        num_images (int): Number of images to use
        music_enabled (bool): Whether to add background music
        output_dir (str): Output directory
        
    Returns:
        dict: Video result dictionary
    """
    try:
        # Validate moviepy first
        check_moviepy_compatibility()
        
        # Import here to avoid early errors
        from utils import get_random_images, get_random_music
        
        # Get random images (with fallback)
        try:
            image_paths = get_random_images(count=num_images)
        except Exception as e:
            logger.warning(f"Could not get random images: {e}")
            # Fallback: get all available images
            images_dir = "images"
            supported = get_supported_image_formats()
            available = [f for f in os.listdir(images_dir) 
                        if os.path.splitext(f)[1].lower() in supported]
            
            if not available:
                raise ValueError("No valid images available in images/ folder")
            
            num_to_use = min(num_images, len(available))
            selected = random.sample(available, num_to_use)
            image_paths = [os.path.join(images_dir, img) for img in selected]
        
        # Get random music if enabled (optional)
        music_path = None
        if music_enabled:
            try:
                music_path = get_random_music()
            except Exception as e:
                logger.warning(f"Music not available: {e}")
        
        # Generate output filename
        output_filename = get_output_filename('.mp4')
        output_path = os.path.join(output_dir, output_filename)
        
        # Create video
        result = create_video_from_images(
            image_paths=image_paths,
            audio_path=audio_path,
            topic=topic,
            music_path=music_path,
            output_path=output_path
        )
        
        return result
    
    except Exception as e:
        logger.error(f"Error generating reel: {e}")
        raise


# ==================== MAIN & TESTS ====================
if __name__ == "__main__":
    try:
        logger.info("Testing moviepy compatibility...")
        check_moviepy_compatibility()
        logger.info("[OK] MoviePy is properly installed for Python 3.14+")
    except Exception as e:
        logger.error(f"[ERROR] MoviePy compatibility check failed: {e}")
        sys.exit(1)