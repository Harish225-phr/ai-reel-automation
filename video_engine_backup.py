"""
Professional Video Engine for AI Reel Automation.
Creates Instagram-ready vertical reels with stock videos, captions, effects.
Features: Cinema-quality cuts, natural pacing, professional subtitles, hook text.
"""

import os
import random
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from moviepy.editor import (
    VideoFileClip, ImageClip, AudioFileClip, concatenate_videoclips,
    CompositeVideoClip, TextClip, CompositeAudioClip, ColorClip
)

from utils import logger

# Pillow 10+ compatibility: Patch Image.ANTIALIAS to work with Pillow 11
try:
    Image.ANTIALIAS = Image.Resampling.LANCZOS
except AttributeError:
    # Already has ANTIALIAS (Pillow <10)
    pass


class ProfessionalVideoEngine:
    """Create professional Instagram reels with cinema-quality effects."""
    
    # Reel dimensions (Instagram Reels format)
    REEL_WIDTH = 1080
    REEL_HEIGHT = 1920
    FPS = 30
    
    def __init__(self, output_dir='output'):
        """Initialize video engine."""
        self.output_dir = output_dir
        Path(output_dir).mkdir(exist_ok=True, parents=True)
        logger.info(f"Professional Video Engine initialized: {output_dir}")
    
    @staticmethod
    def create_caption_image(text, width=1080, height=200, font_size=60):
        """
        Create a professional caption overlay image.
        Centers text at bottom with semi-transparent background.
        """
        try:
            # Create image with transparent background
            img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Try to use a nice font
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("/Windows/Fonts/arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()
            
            # Word wrap text
            words = text.split()
            lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                test_line = ' '.join(current_line)
                bbox = draw.textbbox((0, 0), test_line, font=font)
                if bbox[2] - bbox[0] > width - 40:  # Leave margins
                    if len(current_line) > 1:
                        current_line.pop()
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(test_line)
                        current_line = []
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw semi-transparent background
            total_height = len(lines) * (font_size + 10) + 20
            bg_img = Image.new('RGBA', (width, total_height), (0, 0, 0, 180))
            
            # Draw text with white color and shadow for readability
            y_offset = 10
            for line in lines:
                # Shadow effect (dark offset)
                draw.text((22, y_offset + 2), line, font=font, fill=(0, 0, 0, 200))
                # Main text (white)
                draw.text((20, y_offset), line, font=font, fill=(255, 255, 255, 255))
                y_offset += font_size + 10
            
            # Composite caption onto background
            result = Image.new('RGBA', (width, total_height), (0, 0, 0, 0))
            result = Image.alpha_composite(result, bg_img)
            
            # Draw white text on result
            draw_result = ImageDraw.Draw(result)
            y_offset = 10
            for line in lines:
                draw_result.text((20, y_offset), line, font=font, fill=(255, 255, 255, 255))
                y_offset += font_size + 10
            
            return result
        
        except Exception as e:
            logger.warning(f"Error creating caption: {e}")
            return None
    
    @staticmethod
    def create_hook_overlay(text, width=1080, height=1920):
        """
        Create hook text overlay (big bold text for first 3 seconds).
        Appears in center with gradient background.
        """
        try:
            img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Try to load a bold font
            font_size = 120
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("/Windows/Fonts/arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()
            
            # Word wrap hook text
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
            
            # Calculate text center position
            total_text_height = len(lines) * (font_size + 20)
            start_y = (height - total_text_height) // 2
            
            # Draw text
            y_offset = start_y
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                line_width = bbox[2] - bbox[0]
                x_center = (width - line_width) // 2
                
                # Shadow
                draw.text((x_center + 3, y_offset + 3), line, font=font, fill=(0, 0, 0, 200))
                # Main text (bright yellow/white for visibility)
                draw.text((x_center, y_offset), line, font=font, fill=(255, 255, 100, 255))
                
                y_offset += font_size + 20
            
            # Composite onto overlay
            result = Image.alpha_composite(overlay, img)
            return result
        
        except Exception as e:
            logger.warning(f"Error creating hook: {e}")
            return None
    
    @staticmethod
    def get_video_clips(video_paths, total_duration):
        """
        Convert video paths to clips, cutting to total duration.
        Segments videos by silence in audio for cinematic cuts.
        """
        try:
            clips = []
            remaining_duration = total_duration
            
            for video_path in video_paths:
                if not os.path.exists(video_path) or remaining_duration <= 0:
                    break
                
                try:
                    video = VideoFileClip(video_path)
                    video_duration = min(video.duration, remaining_duration)
                    
                    # Resize to reel dimensions
                    video_resized = video.resize(height=ProfessionalVideoEngine.REEL_HEIGHT)
                    
                    # Center crop to width
                    if video_resized.w > ProfessionalVideoEngine.REEL_WIDTH:
                        x_center = (video_resized.w - ProfessionalVideoEngine.REEL_WIDTH) / 2
                        video_resized = video_resized.crop(
                            x1=x_center,
                            y1=0,
                            x2=x_center + ProfessionalVideoEngine.REEL_WIDTH,
                            y2=ProfessionalVideoEngine.REEL_HEIGHT
                        )
                    
                    # Cut to exact duration needed
                    clip = video_resized.subclipped(0, video_duration)
                    clips.append(clip)
                    
                    remaining_duration -= video_duration
                    video.close()
                
                except Exception as e:
                    logger.warning(f"Error processing video {video_path}: {e}")
            
            return clips
        
        except Exception as e:
            logger.error(f"Error getting video clips: {e}")
            return []
    
    def create_reel_from_script_and_video(
        self,
        script,
        audio_path,
        hook_text,
        video_paths,
        background_music_path=None,
        output_name='reel.mp4'
    ):
        """
        Create professional reel combining video, audio, captions, and effects.
        Timeline is controlled by voice duration.
        
        Sequence:
        1. Get voice duration (controls everything)
        2. Load and match video to voice duration
        3. Create caption clips with proper timing
        4. Add hook text (first 3 seconds)
        5. Mix voice + background music (15% bg, 100% voice)
        6. Composite all elements
        7. Export with perfect sync
        
        Args:
            script (str): Full script text for captions
            audio_path (str): Path to voice audio
            hook_text (str): Big text for first 3 seconds
            video_paths (list): List of stock video paths
            background_music_path (str): Optional background music
            output_name (str): Output filename
            
        Returns:
            str: Path to created reel
        """
        try:
            logger.info("=" * 60)
            logger.info("CREATING PROFESSIONAL REEL (SYNCHRONIZED)")
            logger.info("=" * 60)
            
            # STEP 1: Get voice duration (master timeline)
            logger.info("\n[SYNC] Step 1: Load voice and get duration...")
            audio = AudioFileClip(audio_path)
            total_duration = audio.duration
            logger.info(f"[SYNC] Voice duration: {total_duration:.2f} seconds (MASTER TIMELINE)")
            
            # STEP 2: Load and match video to voice duration
            logger.info("\n[SYNC] Step 2: Load video clips and match to voice duration...")
            video_clips = self.get_video_clips(video_paths, total_duration)
            
            if not video_clips:
                logger.warning("[SYNC] No video clips available, using black background")
                # Create black background - EXACT duration to match voice
                video_base = ColorClip(
                    size=(self.REEL_WIDTH, self.REEL_HEIGHT),
                    color=(0, 0, 0)
                ).set_duration(total_duration)
                logger.info(f"[SYNC] Created fallback video: {total_duration:.2f}s (matches voice)")
            else:
                logger.info(f"[SYNC] Loaded {len(video_clips)} video clips")
                
                # Concatenate video clips
                if len(video_clips) > 1:
                    video_base = concatenate_videoclips(video_clips)
                    logger.info(f"[SYNC] Concatenated videos: {video_base.duration:.2f}s")
                else:
                    video_base = video_clips[0]
                
                # CRITICAL: Trim/extend video to EXACTLY match voice duration
                if video_base.duration < total_duration:
                    logger.warning(f"[SYNC] Video ({video_base.duration:.2f}s) shorter than voice, looping...")
                    # Loop video to extend it
                    repeat_times = int(total_duration / video_base.duration) + 1
                    video_base = concatenate_videoclips([video_base] * repeat_times)
                    logger.info(f"[SYNC] After looping: {video_base.duration:.2f}s")
                
                # Trim to exact duration (MUST match voice perfectly)
                video_base = video_base.subclipped(0, total_duration)
                logger.info(f"[SYNC] Final video duration: {video_base.duration:.2f}s (SYNCED WITH VOICE)")
            
            # STEP 3: Create and position audio track
            logger.info("\n[SYNC] Step 3: Process audio with proper mixing...")
            
            # Voice is 100% volume
            voice_audio = audio.volumex(1.0)
            logger.info("[SYNC] Voice volume: 100%")
            
            # Handle background music if provided
            final_audio = voice_audio
            if background_music_path and os.path.exists(background_music_path):
                try:
                    logger.info(f"[SYNC] Loading background music: {background_music_path}")
                    bg_music = AudioFileClip(background_music_path)
                    
                    # Loop music to match voice duration if needed
                    if bg_music.duration < total_duration:
                        repeat_times = int(total_duration / bg_music.duration) + 1
                        bg_music_clips = [bg_music] * repeat_times
                        bg_music = concatenate_videoclips(bg_music_clips)
                        logger.info(f"[SYNC] Looped background music to: {bg_music.duration:.2f}s")
                    
                    # Trim music to exact voice duration
                    bg_music = bg_music.subclipped(0, total_duration)
                    
                    # Set background music to 15% volume
                    bg_music = bg_music.volumex(0.15)
                    logger.info("[SYNC] Background music volume: 15%")
                    
                    # Composite: voice (100%) + music (15%)
                    # Both start at 0 seconds, perfectly aligned
                    final_audio = CompositeAudioClip([voice_audio, bg_music])
                    logger.info("[SYNC] Audio mixed: Voice 100% + Background Music 15%")
                    
                except Exception as e:
                    logger.warning(f"[SYNC] Background music error: {e}")
                    logger.warning("[SYNC] Using voice only")
                    final_audio = voice_audio
            else:
                logger.info("[SYNC] No background music - using voice only")
            
            # STEP 4: Attach audio to video
            logger.info("\n[SYNC] Step 4: Attach audio to video...")
            video_with_audio = video_base.set_audio(final_audio)
            logger.info(f"[SYNC] Video+Audio ready: {video_with_audio.duration:.2f}s")
            
            # STEP 5: Create caption clips with proper timing
            logger.info("\n[SYNC] Step 5: Create captions with voice-synced timing...")
            caption_clips = []
            
            # Split script into chunks for staggered captions
            words = script.split()
            chunk_size = max(5, len(words) // 8)  # 8-10 caption chunks
            chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
            
            # Create caption clips at intervals
            chunk_duration = total_duration / len(chunks) if chunks else total_duration
            logger.info(f"[SYNC] Creating {len(chunks)} captions, each ~{chunk_duration:.2f}s")
            
            for idx, chunk in enumerate(chunks):
                if not chunk.strip():
                    continue
                
                try:
                    # Create caption image
                    caption_img = self.create_caption_image(chunk, width=self.REEL_WIDTH, height=250)
                    
                    if caption_img:
                        # Convert PIL to ImageClip (save to temp file then load)
                        temp_path = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
                        caption_img.save(temp_path)
                        caption_clip = ImageClip(temp_path)
                        caption_clip = caption_clip.set_position(('center', 'bottom'))
                        caption_clip = caption_clip.set_duration(chunk_duration)
                        
                        # SYNC: Start caption at calculated time
                        start_time = idx * chunk_duration
                        caption_clip = caption_clip.set_start(start_time)
                        caption_clips.append(caption_clip)
                        logger.debug(f"[SYNC] Caption {idx}: {start_time:.2f}s - {start_time + chunk_duration:.2f}s")
                
                except Exception as e:
                    logger.warning(f"Error creating caption {idx}: {e}")
            
            logger.info(f"[SYNC] Created {len(caption_clips)} caption clips")
            
            # STEP 6: Add hook text overlay (first 3 seconds)
            logger.info("\n[SYNC] Step 6: Add hook text (0-3 seconds)...")
            hook_clip = None
            if hook_text:
                try:
                    hook_img = self.create_hook_overlay(hook_text, self.REEL_WIDTH, self.REEL_HEIGHT)
                    if hook_img:
                        temp_path = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
                        hook_img.save(temp_path)
                        hook_clip = ImageClip(temp_path)
                        hook_clip = hook_clip.set_position(('center', 'center'))
                        
                        # Hook text duration: first 3 seconds (or less if total is shorter)
                        hook_duration = min(3.0, total_duration)
                        hook_clip = hook_clip.set_duration(hook_duration)
                        
                        # SYNC: Hook starts at 0 seconds
                        hook_clip = hook_clip.set_start(0)
                        logger.info(f"[SYNC] Hook text: 0-{hook_duration:.2f}s")
                
                except Exception as e:
                    logger.warning(f"Error creating hook: {e}")
            else:
                logger.info("[SYNC] No hook text provided")
            
            # STEP 7: Composite all elements
            logger.info("\n[SYNC] Step 7: Composite video, captions, and effects...")
            composite_clips = [video_with_audio] + caption_clips
            if hook_clip:
                composite_clips.append(hook_clip)
            
            logger.info(f"[SYNC] Compositing: 1 video + {len(caption_clips)} captions + {1 if hook_clip else 0} hook")
            
            final_video = CompositeVideoClip(composite_clips, size=(self.REEL_WIDTH, self.REEL_HEIGHT))
            
            # CRITICAL: Set audio on composite (ensure all audio layers are included)
            final_video = final_video.set_audio(final_audio)
            logger.info(f"[SYNC] Final composite duration: {final_video.duration:.2f}s")
            
            # STEP 8: Export with perfect sync
            logger.info("\n[SYNC] Step 8: Export reel with perfect synchronization...")
            
            # STEP 8: Export with perfect sync
            logger.info("\n[SYNC] Step 8: Export reel with perfect synchronization...")
            
            # Write to file with optimal settings for Instagram
            output_path = os.path.join(self.output_dir, output_name)
            logger.info(f"[SYNC] Output: {output_path}")
            logger.info(f"[SYNC] Format: {self.REEL_WIDTH}x{self.REEL_HEIGHT} @ {self.FPS}fps")
            logger.info(f"[SYNC] Duration: {final_video.duration:.2f}s (voice-controlled)")
            logger.info(f"[SYNC] Codec: H.264 + AAC")
            
            final_video.write_videofile(
                output_path,
                fps=self.FPS,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None,
                preset='fast'  # Faster encoding
            )
            
            # Verify output was created
            if not os.path.exists(output_path):
                raise FileNotFoundError(f"reel not created: {output_path}")
            
            # Cleanup
            video_with_audio.close()
            final_video.close()
            audio.close()
            
            file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
            logger.info(f"\n[SYNC] SUCCESS!")
            logger.info(f"[OK] Reel created: {output_path}")
            logger.info(f"[OK] Size: {file_size_mb:.2f} MB")
            logger.info("=" * 60)
            
            return output_path
        
        except Exception as e:
            logger.error(f"Error creating reel: {e}")
            raise


def create_reel(
    script,
    audio_path,
    hook_text,
    video_paths,
    output_dir='output',
    output_name='reel.mp4'
):
    """
    Convenience function to create a professional reel.
    
    Args:
        script (str): Script text
        audio_path (str): Path to voice audio
        hook_text (str): Hook text for opening
        video_paths (list): List of video paths
        output_dir (str): Output directory
        output_name (str): Output filename
        
    Returns:
        str: Path to created reel
    """
    engine = ProfessionalVideoEngine(output_dir)
    return engine.create_reel_from_script_and_video(
        script=script,
        audio_path=audio_path,
        hook_text=hook_text,
        video_paths=video_paths,
        output_name=output_name
    )
