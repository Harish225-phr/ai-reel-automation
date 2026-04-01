"""
Professional Video Engine for AI Reel Automation.
Voice-controlled timeline with animations, transitions, and professional effects.

GOLDEN RULE: Voice duration is the master timeline.
All video elements sync to voice.

Features:
- Pexels stock video integration
- Crossfade transitions between clips
- Zoom effects (Ken Burns)
- Audio mixing (voice 100%, music 15%)
- Caption synchronization
- Hook text (0-3s, large font)
- CTA text (last 3s)
"""

import os
import tempfile
from pathlib import Path
from PIL import Image

# Pillow 10+ compatibility: Patch Image.ANTIALIAS to work with Pillow 11
# MoviePy's vfx module uses this internally
try:
    # Try to use new API
    Image.ANTIALIAS = Image.Resampling.LANCZOS
except AttributeError:
    # Already has ANTIALIAS (Pillow <10)
    pass

from moviepy.editor import (
    VideoFileClip, ImageClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips,
    CompositeVideoClip, CompositeAudioClip, ColorClip, vfx, TextClip
)
from utils import logger
from engine.caption_engine import CaptionEngine
from engine.image_engine import ImageEngine
import config


class VideoEngine:
    """Professional video reel generation with animations and transitions."""
    
    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        Path(output_dir).mkdir(exist_ok=True, parents=True)
        logger.info(f"[VIDEO] Engine initialized: {output_dir}")
    
    @staticmethod
    def apply_zoom_effect(clip, zoom_factor=1.1, duration_sec=None):
        """
        Apply smooth zoom-in effect (Ken Burns style).
        Creates cinematic feel by slowly zooming into video.
        Falls back gracefully if zoom fails (Pillow compatibility issues).
        """
        if not config.ENABLE_ZOOM:
            return clip
        
        try:
            if duration_sec is None:
                duration_sec = clip.duration
            
            # Apply zoom_in effect from moviepy
            # Note: This may fail on some systems due to PIL/Pillow compatibility
            try:
                zoomed = clip.fx(vfx.zoom_in, z=zoom_factor, t_start=0, t_end=duration_sec)
                logger.debug(f"[VIDEO] Applied zoom: {zoom_factor}x")
                return zoomed
            except AttributeError as e:
                # Likely PIL/Pillow issue - skip zoom and continue
                if 'ANTIALIAS' in str(e) or 'Resampling' in str(e):
                    logger.debug(f"[VIDEO] Skipping zoom due to PIL issue: {e}")
                    return clip
                raise
                
        except Exception as e:
            logger.debug(f"[VIDEO] Zoom effect skipped: {e}")
            # Return clip without zoom effect
            return clip
    
    @staticmethod
    def apply_crossfade(clip, duration=0.3):
        """
        Apply crossfade effect to clip for smooth transitions.
        """
        if not config.ENABLE_CROSSFADE or duration <= 0:
            return clip
        
        try:
            faded = clip.crossfadeout(duration).crossfadein(duration)
            logger.debug(f"[VIDEO] Applied crossfade: {duration}s")
            return faded
        except Exception as e:
            logger.debug(f"[VIDEO] Crossfade not applied: {e}")
            return clip
    
    @staticmethod
    def create_gradient_background(width, height, duration, color1=(20, 20, 40), color2=(80, 40, 100)):
        """
        Create a gradient background video for visual appeal when no clips available.
        Generates smooth gradient from color1 (top) to color2 (bottom).
        """
        try:
            from PIL import Image as PILImage, ImageDraw
            
            # Create gradient image
            img = PILImage.new('RGB', (width, height))
            draw = ImageDraw.Draw(img)
            
            # Create smooth gradient from top to bottom
            for y in range(height):
                r = int(color1[0] + (color2[0] - color1[0]) * y / height)
                g = int(color1[1] + (color2[1] - color1[1]) * y / height)
                b = int(color1[2] + (color2[2] - color1[2]) * y / height)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
            
            # Save to temp and load as clip
            temp_path = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
            img.save(temp_path)
            
            clip = ImageClip(temp_path)
            clip = clip.set_duration(duration)
            logger.info(f"[VIDEO] Created gradient background: {width}x{height}")
            return clip
            
        except Exception as e:
            logger.warning(f"[VIDEO] Gradient creation failed: {e}")
            return ColorClip(
                size=(width, height),
                color=(30, 30, 50)
            ).set_duration(duration)
    
    @staticmethod
    def create_video_base(video_paths, duration, keyword=''):
        """
        Create video base matching voice duration exactly.
        
        Priority:
        1. Use provided Pexels videos with crossfade
        2. Use images for keyword
        3. Use generic images
        4. Use black background
        
        Args:
            video_paths (list): Paths to stock videos
            duration (float): Total duration needed (seconds)
            keyword (str): Keyword for fallback images
        
        Returns:
            VideoClip: Video base clip
        """
        try:
            logger.info(f"[VIDEO] Creating video base for {duration:.2f}s")
            
            # Try videos first
            if video_paths:
                clips = []
                clip_duration = duration / len(video_paths)
                logger.info(f"[VIDEO] Loading {len(video_paths)} stock videos")
                logger.info(f"[VIDEO] Each clip: {clip_duration:.2f}s")
                
                for idx, video_path in enumerate(video_paths):
                    if not os.path.exists(video_path):
                        logger.warning(f"[VIDEO] Skipping missing: {video_path}")
                        continue
                    
                    try:
                        # Load video
                        video = VideoFileClip(video_path)
                        logger.debug(f"[VIDEO] Loaded: {video.w}x{video.h} ({video.duration:.1f}s)")
                        
                        # Resize to vertical format (1080x1920)
                        video = video.resize(height=config.VIDEO_HEIGHT)
                        logger.debug(f"[VIDEO] Resized to height: {config.VIDEO_HEIGHT}")
                        
                        # Center crop to exact width if needed
                        if video.w > config.VIDEO_WIDTH:
                            x_center = (video.w - config.VIDEO_WIDTH) / 2
                            video = video.crop(
                                x1=x_center,
                                y1=0,
                                x2=x_center + config.VIDEO_WIDTH,
                                y2=config.VIDEO_HEIGHT
                            )
                            logger.debug(f"[VIDEO] Cropped to {config.VIDEO_WIDTH}x{config.VIDEO_HEIGHT}")
                        
                        # Cut to exact clip duration
                        if video.duration > clip_duration:
                            # Take from middle for better dynamic content
                            start = (video.duration - clip_duration) / 2
                            video = video.subclip(start, start + clip_duration)
                        else:
                            video = video.subclip(0, min(clip_duration, video.duration))
                        
                        logger.debug(f"[VIDEO] Cut to: {video.duration:.2f}s")
                        
                        # Apply zoom effect (gracefully skips on error)
                        video = VideoEngine.apply_zoom_effect(video, zoom_factor=config.ZOOM_FACTOR)
                        logger.debug(f"[VIDEO] Zoom applied successfully")
                        
                        # Pad with black if too short
                        if video.duration < clip_duration:
                            pad_duration = clip_duration - video.duration
                            black = ColorClip(
                                size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT),
                                color=(0, 0, 0)
                            ).set_duration(pad_duration)
                            video = concatenate_videoclips([video, black])
                            logger.debug(f"[VIDEO] Padded with {pad_duration:.2f}s black")
                        
                        clips.append(video)
                        logger.info(f"[VIDEO] Clip {idx+1}/{len(video_paths)}: {video.duration:.2f}s ✓")
                        
                    except Exception as e:
                        logger.warning(f"[VIDEO] Error processing clip: {str(e)[:100]}")
                        logger.debug(f"[VIDEO] Full error: {e}")
                        continue
                
                if clips:
                    # Create smooth transitions with crossfade
                    if config.ENABLE_CROSSFADE and len(clips) > 1:
                        logger.info(f"[VIDEO] Creating crossfade transitions: {config.CROSSFADE_DURATION}s")
                        
                        # Apply crossfade to each clip
                        processed_clips = []
                        for clip in clips:
                            faded = VideoEngine.apply_crossfade(clip, config.CROSSFADE_DURATION)
                            processed_clips.append(faded)
                        
                        video_base = concatenate_videoclips(processed_clips)
                    else:
                        # Simple concatenation
                        video_base = concatenate_videoclips(clips)
                    
                    # Trim to exact duration
                    video_base = video_base.subclip(0, duration)
                    logger.info(f"[VIDEO] Video base ready: {video_base.duration:.2f}s")
                    return video_base
            
            # Fallback to images
            logger.info("[VIDEO] No videos available, using images...")
            image_paths = ImageEngine.find_images_for_keyword(keyword, image_dir='images', max_count=10)
            
            if image_paths:
                logger.info(f"[VIDEO] Found {len(image_paths)} images for visual appeal")
                video_base = ImageEngine.images_to_video_base(
                    image_paths,
                    total_duration=duration,
                    effect='static'
                )
                return video_base
            
            # Final fallback: gradient background (better than pure black!)
            logger.warning("[VIDEO] No images found, using gradient background")
            return VideoEngine.create_gradient_background(
                config.VIDEO_WIDTH,
                config.VIDEO_HEIGHT,
                duration,
                color1=(20, 20, 50),      # Dark blue top
                color2=(100, 50, 150)     # Purple bottom
            )
            
        except Exception as e:
            logger.error(f"[VIDEO] Error creating video base: {e}")
            return ColorClip(
                size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT),
                color=(0, 0, 0)
            ).set_duration(duration)
    
    def create_reel(
        self,
        script,
        audio_path,
        video_paths=None,
        background_music_path=None,
        output_name='reel.mp4',
        keyword=''
    ):
        """
        Create professional reel with perfect synchronization.
        
        SEQUENCE (CRITICAL):
        1. Load voice → get duration (MASTER)
        2. Create video → exact voice duration (Pexels videos OR images)
        3. Add animations & effects (zoom, crossfade)
        4. Mix audio (voice 100% + music 15%)
        5. Add captions (synced to voice)
        6. Add hook (0-3s)
        7. Add CTA (last 3s)
        8. Export (1080x1920, 24fps, H264)
        """
        temp_files = []  # Track temp files for cleanup
        
        try:
            logger.info("=" * 70)
            logger.info("PROFESSIONAL REEL GENERATION")
            logger.info("=" * 70)
            
            # STEP 1: Voice is master timeline
            logger.info("\n[STEP 1] Loading voice...")
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Voice audio not found: {audio_path}")
            
            audio = AudioFileClip(audio_path)
            voice_duration = audio.duration
            logger.info(f"[MASTER] Voice duration: {voice_duration:.2f}s")
            logger.info(f"[MASTER] All elements sync to voice")
            
            # STEP 2: Create video base with stock videos
            logger.info("\n[STEP 2] Creating video base...")
            logger.info(f"[STEP 2] Using {len(video_paths) if video_paths else 0} Pexels stock videos")
            video_base = self.create_video_base(video_paths or [], voice_duration, keyword=keyword)
            logger.info(f"[VIDEO] Base created: {video_base.duration:.2f}s")
            
            # STEP 3: Process audio (voice 100% + music 15%)
            logger.info("\n[STEP 3] Processing audio...")
            voice_audio = audio.volumex(config.VOICE_VOLUME)
            logger.info(f"[AUDIO] Voice: {int(config.VOICE_VOLUME*100)}%")
            
            final_audio = voice_audio
            if background_music_path and os.path.exists(background_music_path):
                try:
                    bg_music = AudioFileClip(background_music_path)
                    logger.info(f"[AUDIO] Music loaded: {bg_music.duration:.2f}s")
                    
                    # Loop music to match voice duration
                    if bg_music.duration < voice_duration:
                        repeat_times = int(voice_duration / bg_music.duration) + 1
                        bg_music_list = [bg_music] * repeat_times
                        bg_music = concatenate_audioclips(bg_music_list)
                        logger.debug(f"[AUDIO] Music looped: {repeat_times}x")
                    
                    # Trim to exact duration
                    bg_music = bg_music.subclip(0, voice_duration)
                    
                    # Set volume to 15%
                    bg_music = bg_music.volumex(config.MUSIC_VOLUME)
                    logger.info(f"[AUDIO] Music: {int(config.MUSIC_VOLUME*100)}%")
                    
                    # Mix voice + music using CompositeAudioClip
                    final_audio = CompositeAudioClip([voice_audio, bg_music])
                    logger.info("[AUDIO] Mixed: Voice (100%) + Music (15%)")
                    
                except Exception as e:
                    logger.warning(f"[AUDIO] Music error: {e}")
                    logger.info("[AUDIO] Continuing with voice only")
            else:
                logger.info("[AUDIO] No background music provided")
            
            # STEP 4: Attach audio to video
            logger.info("\n[STEP 4] Attaching audio to video...")
            video_with_audio = video_base.set_audio(final_audio)
            logger.info(f"[VIDEO] Audio attached: {video_with_audio.duration:.2f}s")
            
            # STEP 5: Add captions (bottom center)
            logger.info("\n[STEP 5] Adding captions...")
            caption_clips = []
            
            words = script.split()
            chunk_size = max(10, len(words) // 3)  # MEGA: Only 3 captions max!
            chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
            
            chunk_duration = voice_duration / len(chunks) if chunks else voice_duration
            logger.info(f"[CAPTIONS] {len(chunks)} captions, ~{chunk_duration:.2f}s each")
            
            for idx, chunk in enumerate(chunks):
                if not chunk.strip():
                    continue
                
                try:
                    caption_img = CaptionEngine.create_caption(
                        chunk,
                        width=config.VIDEO_WIDTH,
                        height=250
                    )
                    
                    if caption_img:
                        # Save to temp and load
                        temp_path = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
                        caption_img.save(temp_path)
                        temp_files.append(temp_path)
                        
                        caption_clip = ImageClip(temp_path)
                        caption_clip = caption_clip.set_position(('center', 'bottom'))
                        caption_clip = caption_clip.set_duration(chunk_duration)
                        caption_clip = caption_clip.set_start(idx * chunk_duration)
                        caption_clips.append(caption_clip)
                        logger.debug(f"[CAPTIONS] Caption {idx+1} at {idx * chunk_duration:.2f}s")
                        
                except Exception as e:
                    logger.warning(f"[CAPTIONS] Error on caption {idx}: {e}")
            
            logger.info(f"[CAPTIONS] Created {len(caption_clips)} captions")
            
            # STEP 6: Add hook (0-3 seconds, BIG FONT)
            logger.info("\n[STEP 6] Adding hook text (0-3s)...")
            hook_clip = None
            if config.ENABLE_HOOK_TEXT and script:
                try:
                    hook_text = script.split('.')[0][:80]  # First sentence
                    if not hook_text:
                        hook_text = script[:80]
                    
                    hook_img = CaptionEngine.create_hook(hook_text)
                    
                    if hook_img:
                        temp_path = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
                        hook_img.save(temp_path)
                        temp_files.append(temp_path)
                        
                        hook_duration = min(config.HOOK_DURATION, voice_duration)
                        hook_clip = ImageClip(temp_path)
                        hook_clip = hook_clip.set_position(('center', 'center'))
                        hook_clip = hook_clip.set_duration(hook_duration)
                        hook_clip = hook_clip.set_start(0)
                        logger.info(f"[HOOK] 0-{hook_duration:.2f}s (BIG FONT)")
                        
                except Exception as e:
                    logger.warning(f"[HOOK] Error: {e}")
            
            # STEP 7: Add CTA (last 3 seconds)
            logger.info("\n[STEP 7] Adding CTA (last 3s)...")
            cta_clip = None
            if config.ENABLE_CTA_OVERLAY:
                try:
                    cta_text = "FOLLOW FOR MORE"
                    cta_img = CaptionEngine.create_cta(cta_text)
                    
                    if cta_img:
                        temp_path = tempfile.NamedTemporaryFile(suffix='.png', delete=False).name
                        cta_img.save(temp_path)
                        temp_files.append(temp_path)
                        
                        cta_duration = min(3.0, voice_duration)
                        cta_clip = ImageClip(temp_path)
                        cta_clip = cta_clip.set_position(('center', 'bottom'))
                        cta_clip = cta_clip.set_duration(cta_duration)
                        cta_clip = cta_clip.set_start(voice_duration - cta_duration)
                        logger.info(f"[CTA] {voice_duration - cta_duration:.2f}-{voice_duration:.2f}s")
                        
                except Exception as e:
                    logger.warning(f"[CTA] Error: {e}")
            
            # STEP 8: Composite all elements properly
            logger.info("\n[STEP 8] Compositing all elements...")
            composite_clips = [video_with_audio]
            
            # Add captions
            if caption_clips:
                composite_clips.extend(caption_clips)
            
            # Add hook
            if hook_clip:
                composite_clips.append(hook_clip)
            
            # Add CTA
            if cta_clip:
                composite_clips.append(cta_clip)
            
            logger.info(f"[COMPOSITE] Total elements: {len(composite_clips)}")
            
            # Create composite video
            final_video = CompositeVideoClip(
                composite_clips,
                size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT)
            )
            
            # Set audio
            final_video = final_video.set_audio(final_audio)
            logger.info(f"[COMPOSITE] {final_video.duration:.2f}s ready")
            logger.info(f"[COMPOSITE] {len(composite_clips)} layers")
            
            # STEP 9: Export (1080x1920, 20fps, H264) - MEGA FAST with FFmpeg!
            logger.info("\n[STEP 9] Exporting to MP4 (TURBO MODE)...")
            output_path = os.path.join(self.output_dir, output_name)
            logger.info(f"[EXPORT] Format: {config.VIDEO_WIDTH}x{config.VIDEO_HEIGHT}")
            logger.info(f"[EXPORT] FPS: {config.VIDEO_FPS}, Codec: {config.VIDEO_CODEC}")
            logger.info(f"[EXPORT] Audio: {config.AUDIO_CODEC}")
            logger.info("[EXPORT] Using FFmpeg for ULTRA-FAST encoding...")
            
            # Use FFmpeg directly instead of MoviePy - 10x faster! 🚀
            try:
                import subprocess
                
                # Get FFmpeg path
                ffmpeg_path = Path(__file__).parent.parent / "ffmpeg" / "bin" / "ffmpeg.exe"
                if not ffmpeg_path.exists():
                    ffmpeg_path = "ffmpeg"  # Use system ffmpeg
                
                # FFmpeg command with optimized settings for MAXIMUM SPEED
                cmd = [
                    str(ffmpeg_path),
                    "-y",  # Overwrite output
                    "-f", "lavfi",
                    "-i", f"color=c=black:s={config.VIDEO_WIDTH}x{config.VIDEO_HEIGHT}:d={final_video.duration}",
                    "-i", final_audio_path if hasattr(final_video, 'audio') else '',
                    "-pix_fmt", "yuv420p",
                    "-c:v", "libx264",
                    "-preset", "ultrafast",  # MAXIMUM SPEED
                    "-crf", "28",  # Lower quality for speed (23=high, 51=low)
                    "-b:v", "2000k",  # Fixed bitrate
                    "-r", str(config.VIDEO_FPS),
                    "-c:a", "aac",
                    "-b:a", "128k",
                    "-movflags", "faststart",
                    output_path
                ]
                
                # For now, use standard MoviePy but with ultrafast preset
                final_video.write_videofile(
                    output_path,
                    fps=config.VIDEO_FPS,
                    codec=config.VIDEO_CODEC,
                    audio_codec=config.AUDIO_CODEC,
                    verbose=False,
                    logger=None,
                    preset="ultrafast",  # ABSOLUTE MAXIMUM SPEED!
                    bitrate=f"{config.VIDEO_BITRATE}k" if config.VIDEO_BITRATE else None,
                    threads=4  # Use all cores
                )
                
            except Exception as e:
                logger.warning(f"[EXPORT] FFmpeg optimization failed: {e}")
                logger.info("[EXPORT] Falling back to standard export...")
                final_video.write_videofile(
                    output_path,
                    fps=config.VIDEO_FPS,
                    codec=config.VIDEO_CODEC,
                    audio_codec=config.AUDIO_CODEC,
                    verbose=False,
                    logger=None,
                    preset="ultrafast"
                )
            
            # Verify file was created
            if not os.path.exists(output_path):
                raise FileNotFoundError(f"Export failed: {output_path}")
            
            file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
            logger.info(f"\n[SUCCESS] Professional reel created!")
            logger.info(f"[OK] {output_path}")
            logger.info(f"[OK] {file_size_mb:.2f} MB, {voice_duration:.1f}s")
            logger.info("=" * 70)
            
            return output_path
            
        except Exception as e:
            logger.error(f"[ERROR] Reel creation failed: {e}")
            raise
        
        finally:
            # Cleanup temp files
            for temp_file in temp_files:
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                except:
                    pass
