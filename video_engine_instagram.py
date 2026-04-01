"""
Instagram-Style Professional Reel Engine
Complete refactor for cinematic reels with synced subtitles and music.
"""

import os
import sys
from pathlib import Path
from PIL import Image

# ============================================================================
# PILLOW 11+ COMPATIBILITY - CRITICAL
# ============================================================================
try:
    RESAMPLE = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLE = Image.LANCZOS

try:
    Image.ANTIALIAS = Image.Resampling.LANCZOS
except AttributeError:
    pass

# ============================================================================
# MOVIEPY IMPORTS (AFTER PIL PATCH)
# ============================================================================
from moviepy.editor import (
    VideoFileClip, AudioFileClip, TextClip, ColorClip,
    concatenate_videoclips, concatenate_audioclips,
    CompositeVideoClip, CompositeAudioClip, vfx
)

from utils import logger


class InstagramReelEngine:
    """
    Professional Instagram reel generation engine.
    Creates cinematic vertical reels with synced subtitles and music.
    """

    REEL_WIDTH = 1080
    REEL_HEIGHT = 1920
    FPS = 30

    def __init__(self, output_dir='output'):
        """Initialize Instagram reel engine."""
        self.output_dir = output_dir
        Path(output_dir).mkdir(exist_ok=True, parents=True)
        logger.info(f"[INSTAGRAM] Engine initialized: {output_dir}")

    @staticmethod
    def split_script_to_sentences(script):
        """
        Split script into sentences for subtitle display.
        
        Args:
            script (str): Full script text
            
        Returns:
            list: Sentences without empty strings
        """
        sentences = [s.strip() for s in script.split('.') if s.strip()]
        logger.info(f"[SCRIPT] Split into {len(sentences)} sentences")
        return sentences

    @staticmethod
    def validate_and_load_video(video_path, duration_needed):
        """
        Load and validate video clip.
        
        Args:
            video_path (str): Path to video file
            duration_needed (float): Duration needed in seconds
            
        Returns:
            VideoFileClip or None
        """
        try:
            if not os.path.exists(video_path):
                logger.warning(f"[VIDEO] File not found: {video_path}")
                return None

            clip = VideoFileClip(video_path)
            
            if clip.duration < 1:
                logger.warning(f"[VIDEO] Clip too short: {clip.duration:.1f}s")
                clip.close()
                return None

            logger.debug(f"[VIDEO] Loaded: {video_path} ({clip.duration:.1f}s)")
            return clip

        except Exception as e:
            logger.warning(f"[VIDEO] Error loading {video_path}: {e}")
            return None

    @staticmethod
    def apply_cinematic_zoom(clip, duration):
        """
        Apply slow zoom effect for cinematic look.
        
        Args:
            clip: VideoFileClip
            duration (float): Duration in seconds
            
        Returns:
            VideoFileClip with zoom effect
        """
        try:
            # Slow zoom in: scale from 1.0 to 1.2 over duration
            def zoom_effect(t):
                zoom_factor = 1.0 + (0.2 * t / duration)
                return zoom_factor
            
            zoomed = clip.resize(lambda t: zoom_effect(t))
            logger.debug(f"[EFFECT] Cinematic zoom applied: {duration:.1f}s")
            return zoomed

        except Exception as e:
            logger.warning(f"[EFFECT] Zoom failed: {e}")
            return clip

    @staticmethod
    def resize_to_vertical(clip):
        """
        Resize video to 1080x1920 vertical format.
        
        Args:
            clip: VideoFileClip
            
        Returns:
            VideoFileClip resized to 1080x1920
        """
        try:
            # Resize to match height
            clip = clip.resize(height=InstagramReelEngine.REEL_HEIGHT)

            # Crop width if needed
            if clip.w > InstagramReelEngine.REEL_WIDTH:
                x_center = (clip.w - InstagramReelEngine.REEL_WIDTH) / 2
                clip = clip.crop(
                    x1=x_center,
                    y1=0,
                    x2=x_center + InstagramReelEngine.REEL_WIDTH,
                    y2=InstagramReelEngine.REEL_HEIGHT
                )

            logger.debug(f"[RESIZE] Resized to {clip.w}x{clip.h}")
            return clip

        except Exception as e:
            logger.warning(f"[RESIZE] Error: {e}")
            return clip

    @staticmethod
    def create_subtitle_clip(text, duration, start_time):
        """
        Create subtitle clip for sentence using numpy arrays (no external dependencies).
        
        Args:
            text (str): Sentence text
            duration (float): Duration in seconds
            start_time (float): Start time in seconds
            
        Returns:
            ImageClip or None
        """
        try:
            if not text or not text.strip():
                return None

            from PIL import Image, ImageDraw, ImageFont
            import numpy as np

            # Create subtitle image using PIL
            width, height = 1080, 1920
            img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Load font - try Arial first, fall back to default
            font_size = 45
            font = None
            font_paths = [
                "C:\\Windows\\Fonts\\arial.ttf",
                "C:\\Windows\\Fonts\\ArialBD.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            ]
            for font_path in font_paths:
                try:
                    font = ImageFont.truetype(font_path, font_size)
                    break
                except:
                    pass
            
            if font is None:
                font = ImageFont.load_default()
            
            # Wrap text
            words = text.split()
            lines = []
            current_line = []
            max_width = 960
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                try:
                    bbox = draw.textbbox((0, 0), test_line, font=font)
                    line_width = bbox[2] - bbox[0]
                except:
                    line_width = len(test_line) * 25  # Rough estimate
                
                if line_width > max_width and current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    current_line.append(word)
            
            if current_line:
                lines.append(' '.join(current_line))
            
            wrapped_text = '\n'.join(lines)
            
            # Calculate text dimensions
            try:
                bbox = draw.textbbox((0, 0), wrapped_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            except:
                text_width = len(wrapped_text) * 15
                text_height = len(lines) * 50
            
            # Position text at bottom center
            x = (width - text_width) // 2
            y = height - text_height - 120
            
            # Draw text with black stroke for visibility
            # Draw stroke by drawing text multiple times offset
            for adj_x in [-2, -1, 0, 1, 2]:
                for adj_y in [-2, -1, 0, 1, 2]:
                    if adj_x != 0 or adj_y != 0:
                        draw.text((x + adj_x, y + adj_y), wrapped_text, font=font, fill=(0, 0, 0, 200))
            
            # Draw white text
            draw.text((x, y), wrapped_text, font=font, fill=(255, 255, 255, 255))
            
            # Convert to numpy array
            img_array = np.array(img)
            
            # Create ImageClip from array
            clip = ImageClip(img_array)
            clip = clip.set_duration(duration)
            clip = clip.set_position(('center', 'bottom'))
            clip = clip.set_start(start_time)

            logger.debug(f"[SUBTITLE] Created: {len(text)} chars @ {start_time:.1f}s")
            return clip

        except Exception as e:
            logger.warning(f"[SUBTITLE] Error: {e}")
            import traceback
            logger.debug(f"[SUBTITLE] Trace: {traceback.format_exc()}")
            return None

    @staticmethod
    def create_hook_text(hook_text, duration=3.0):
        """
        Create large hook text for opening using PIL (no ImageMagick needed).
        
        Args:
            hook_text (str): Hook text
            duration (float): Duration in seconds
            
        Returns:
            ImageClip or None
        """
        try:
            if not hook_text:
                return None

            from PIL import Image, ImageDraw, ImageFont
            import tempfile

            # Create hook image using PIL
            width, height = 1080, 1920
            img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Load font - try to find bold variant
            font_size = 80
            try:
                font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
                except:
                    font = ImageFont.load_default()
            
            # Wrap text
            words = hook_text.split()
            lines = []
            current_line = []
            max_width = 1000
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                try:
                    bbox = draw.textbbox((0, 0), test_line, font=font)
                    if bbox[2] - bbox[0] > max_width and current_line:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        current_line.append(word)
                except:
                    current_line.append(word)
            
            if current_line:
                lines.append(' '.join(current_line))
            
            wrapped_text = '\n'.join(lines)
            
            # Position text at center
            bbox = draw.textbbox((0, 0), wrapped_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (width - text_width) // 2
            y = (height - text_height) // 2
            
            # Draw with strong stroke (black shadow + white text)
            for adj_x in range(-3, 4):
                for adj_y in range(-3, 4):
                    if adj_x != 0 or adj_y != 0:
                        draw.text((x + adj_x, y + adj_y), wrapped_text, font=font, fill=(0, 0, 0, 220))
            draw.text((x, y), wrapped_text, font=font, fill=(255, 255, 255, 255))
            
            # Convert to numpy array
            import numpy as np
            img_array = np.array(img)
            
            # Create ImageClip from array
            hook = ImageClip(img_array)
            hook = hook.set_duration(duration)
            hook = hook.set_position(('center', 'center'))
            hook = hook.set_start(0)

            logger.info(f"[HOOK] Created: {len(hook_text)} chars, {duration:.1f}s")
            return hook

        except Exception as e:
            logger.warning(f"[HOOK] Error: {e}")
            return None

    @staticmethod
    def find_music_file(fallback_dir='assets/music'):
        """
        Find background music file locally.
        
        Args:
            fallback_dir (str): Directory to search for music
            
        Returns:
            str: Path to music file or None
        """
        if not os.path.exists(fallback_dir):
            logger.warning(f"[MUSIC] Fallback dir not found: {fallback_dir}")
            return None

        audio_extensions = ['.mp3', '.wav', '.aac', '.m4a']
        for file in os.listdir(fallback_dir):
            if any(file.lower().endswith(ext) for ext in audio_extensions):
                path = os.path.join(fallback_dir, file)
                logger.info(f"[MUSIC] Found local music: {file}")
                return path

        logger.warning(f"[MUSIC] No music files in {fallback_dir}")
        return None

    def create_instagram_reel(
        self,
        script,
        audio_path,
        hook_text,
        video_paths,
        background_music_path=None,
        output_name='reel.mp4',
        keyword=''
    ):
        """
        Create professional Instagram reel with cinematic effects.

        PIPELINE:
        1. Load voice (MASTER TIMELINE)
        2. Split script into sentences
        3. Match sentences to video clips
        4. Apply cinematic effects (zoom, resize)
        5. Sync subtitles to clips
        6. Add hook text (first 3s)
        7. Mix audio (voice + music)
        8. Composite all layers
        9. Export as H.264 MP4

        Args:
            script (str): Full script for subtitles
            audio_path (str): Voice audio path
            hook_text (str): Hook text (first 3 seconds)
            video_paths (list): Pexels video paths
            background_music_path (str): Music file path
            output_name (str): Output filename
            keyword (str): Keyword for logging

        Returns:
            str: Path to created reel
        """
        logger.info("\n" + "=" * 70)
        logger.info("INSTAGRAM REEL GENERATION - CINEMATIC STYLE")
        logger.info("=" * 70)

        clips = []
        text_clips = []
        temp_files = []

        try:
            # ================================================================
            # STEP 1: Load voice (MASTER TIMELINE)
            # ================================================================
            logger.info("\n[STEP 1/9] Loading voice audio...")

            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Voice not found: {audio_path}")

            voice = AudioFileClip(audio_path)
            voice_duration = voice.duration
            logger.info(f"[MASTER] Voice duration: {voice_duration:.2f}s")

            # ================================================================
            # STEP 2: Split script to sentences
            # ================================================================
            logger.info("\n[STEP 2/9] Splitting script to sentences...")

            sentences = self.split_script_to_sentences(script)
            if not sentences:
                raise ValueError("No sentences extracted from script")

            logger.info(f"[SCRIPT] Extracted {len(sentences)} sentences")

            # ================================================================
            # STEP 3: Match sentences to video clips
            # ================================================================
            logger.info("\n[STEP 3/9] Matching clips to sentences...")

            if not video_paths:
                raise ValueError("No video paths provided")

            clip_duration = voice_duration / len(sentences)
            logger.info(f"[CLIP] {len(sentences)} clips @ {clip_duration:.2f}s each")

            # Load and prepare clips
            video_clips = []
            for idx, video_path in enumerate(video_paths):
                clip = self.validate_and_load_video(video_path, clip_duration)
                if clip:
                    video_clips.append(clip)

            if not video_clips:
                raise Exception("[ERROR] No valid video clips loaded!")

            logger.info(f"[VIDEO] Loaded {len(video_clips)} clips")

            # ================================================================
            # STEP 4: Create timed clips with effects
            # ================================================================
            logger.info("\n[STEP 4/9] Applying cinematic effects...")

            timed_clips = []
            clip_idx = 0

            for sentence_idx, sentence in enumerate(sentences):
                # Get next available clip (cycle if needed)
                if clip_idx >= len(video_clips):
                    clip_idx = 0

                source_clip = video_clips[clip_idx]
                clip_idx += 1

                try:
                    # Cut to exact duration
                    if source_clip.duration > clip_duration:
                        start = (source_clip.duration - clip_duration) / 2
                        clip = source_clip.subclip(start, start + clip_duration)
                    else:
                        clip = source_clip.subclip(0, min(source_clip.duration, clip_duration))

                    # Resize to vertical
                    clip = self.resize_to_vertical(clip)

                    # Apply cinematic zoom
                    clip = self.apply_cinematic_zoom(clip, clip_duration)

                    # Add crossfade transition
                    if sentence_idx > 0 and sentence_idx < len(sentences):
                        clip = clip.crossfadein(0.5)

                    timed_clips.append(clip)
                    logger.debug(f"[CLIP] {sentence_idx+1}: Added with zoom effect")

                except Exception as e:
                    logger.warning(f"[CLIP] Error processing clip {sentence_idx}: {e}")
                    continue

            if not timed_clips:
                raise Exception("[ERROR] No clips survived processing!")

            logger.info(f"[EFFECT] Applied cinematic effects to {len(timed_clips)} clips")

            # ================================================================
            # STEP 5: Concatenate clips
            # ================================================================
            logger.info("\n[STEP 5/9] Concatenating video clips...")

            video_base = concatenate_videoclips(timed_clips, method='compose')
            logger.info(f"[VIDEO] Concatenated: {video_base.duration:.2f}s")

            # Trim to exact voice duration
            if video_base.duration > voice_duration:
                video_base = video_base.subclip(0, voice_duration)

            # ================================================================
            # STEP 6: Create synchronized subtitles
            # ================================================================
            logger.info("\n[STEP 6/9] Creating synchronized subtitles...")

            subtitle_clips = []
            for idx, sentence in enumerate(sentences):
                start_time = idx * clip_duration
                subtitle = self.create_subtitle_clip(
                    text=sentence,
                    duration=clip_duration,
                    start_time=start_time
                )
                if subtitle:
                    subtitle_clips.append(subtitle)

            logger.info(f"[SUBTITLE] Created {len(subtitle_clips)} subtitle clips")

            # ================================================================
            # STEP 7: Create hook text
            # ================================================================
            logger.info("\n[STEP 7/9] Adding hook text...")

            hook_clip = self.create_hook_text(hook_text, duration=3.0)
            if hook_clip:
                subtitle_clips.insert(0, hook_clip)
                logger.info("[HOOK] Added opening hook")

            # ================================================================
            # STEP 8: Prepare audio (voice + music)
            # ================================================================
            logger.info("\n[STEP 8/9] Mixing audio...")

            # Voice at 100%
            voice_audio = voice.volumex(1.0)
            final_audio = voice_audio
            logger.info("[AUDIO] Voice: 100%")

            # Add background music
            music_path = background_music_path or self.find_music_file()
            
            if music_path and os.path.exists(music_path):
                try:
                    logger.info(f"[MUSIC] Loading: {os.path.basename(music_path)}")
                    music = AudioFileClip(music_path)

                    # Loop music to match voice duration
                    if music.duration < voice_duration:
                        repeat_count = int(voice_duration / music.duration) + 1
                        music_list = [music] * repeat_count
                        music = concatenate_audioclips(music_list)

                    # Trim to exact duration
                    music = music.subclip(0, voice_duration)

                    # Set to 15% volume
                    music = music.volumex(0.15)
                    logger.info("[MUSIC] Added at 15% volume")

                    # Mix: voice (100%) + music (15%)
                    final_audio = CompositeAudioClip([voice_audio, music])

                except Exception as e:
                    logger.warning(f"[MUSIC] Error: {e}")
                    logger.info("[MUSIC] Continuing with voice only")
            else:
                logger.info("[MUSIC] No music available - voice only")

            # Attach audio to video
            video_with_audio = video_base.set_audio(final_audio)
            logger.info(f"[AUDIO] ✓ Audio attached: {video_with_audio.duration:.2f}s")

            # ================================================================
            # STEP 9: Composite all layers and export
            # ================================================================
            logger.info("\n[STEP 9/9] Compositing and exporting...")

            # Composite: video + subtitles
            composite_clips = [video_with_audio] + subtitle_clips
            final_video = CompositeVideoClip(
                composite_clips,
                size=(self.REEL_WIDTH, self.REEL_HEIGHT)
            )

            # Re-attach audio to composite
            final_video = final_video.set_audio(final_audio)

            logger.info(f"[COMPOSITE] Created: {len(composite_clips)-1} text layers")

            # Export
            output_path = os.path.join(self.output_dir, output_name)
            logger.info(f"[EXPORT] Saving: {output_path}")
            logger.info(f"[EXPORT] Format: {self.REEL_WIDTH}x{self.REEL_HEIGHT}, {self.FPS}fps, H.264")

            final_video.write_videofile(
                output_path,
                fps=self.FPS,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None,
                preset='medium'
            )

            # Verify
            if not os.path.exists(output_path):
                raise FileNotFoundError(f"Export failed: {output_path}")

            file_size_mb = os.path.getsize(output_path) / (1024 * 1024)

            logger.info("\n" + "=" * 70)
            logger.info("[SUCCESS] Instagram reel created!")
            logger.info(f"[OK] {output_path}")
            logger.info(f"[OK] Size: {file_size_mb:.2f} MB")
            logger.info(f"[OK] Duration: {final_video.duration:.1f}s")
            logger.info(f"[OK] Format: {self.REEL_WIDTH}x{self.REEL_HEIGHT} @ {self.FPS}fps")
            logger.info("=" * 70)

            return output_path

        except Exception as e:
            logger.error(f"\n[ERROR] Reel creation failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise

        finally:
            # Cleanup
            try:
                for clip in clips + timed_clips + [video_base]:
                    if clip:
                        clip.close()
            except:
                pass


# ============================================================================
# CONVENIENCE FUNCTION
# ============================================================================

def create_instagram_reel(
    script,
    audio_path,
    hook_text,
    video_paths,
    background_music_path=None,
    output_dir='output',
    output_name='reel.mp4',
    keyword=''
):
    """
    Create Instagram reel from provided assets.

    Args:
        script (str): Script text for subtitles
        audio_path (str): Path to voice audio
        hook_text (str): Opening hook text
        video_paths (list): List of Pexels video paths
        background_music_path (str): Optional music path
        output_dir (str): Output directory
        output_name (str): Output filename
        keyword (str): Keyword for logging

    Returns:
        str: Path to created reel
    """
    engine = InstagramReelEngine(output_dir=output_dir)
    return engine.create_instagram_reel(
        script=script,
        audio_path=audio_path,
        hook_text=hook_text,
        video_paths=video_paths,
        background_music_path=background_music_path,
        output_name=output_name,
        keyword=keyword
    )
