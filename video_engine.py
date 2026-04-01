"""
Professional Video Engine for Instagram Reels
- Subtitle system with clean formatting
- Hook and CTA text overlays
- Cinematic effects (zoom, transitions)
- Professional color grading
- Smart video clip management
"""

import os
import logging
from typing import List, Optional
from pathlib import Path

from moviepy.editor import (
    VideoFileClip, AudioFileClip, ImageClip,
    concatenate_videoclips, concatenate_audioclips,
    CompositeVideoClip, CompositeAudioClip
)
from PIL import Image, ImageDraw, ImageFont

# Fix PIL compatibility with newer Pillow versions (10.0+)
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else 1

logger = logging.getLogger(__name__)


class SubtitleSystem:
    """Generate and manage professional subtitles."""
    
    @staticmethod
    def create_subtitle_image(
        text: str,
        width: int = 1080,
        height: int = 1920,
        duration_sec: float = 2.0,
        position: str = 'bottom'
    ) -> str:
        """
        Create subtitle image with professional styling.
        
        Args:
            text: Subtitle text
            width: Video width
            height: Video height
            duration_sec: Display duration
            position: 'bottom' or 'center'
            
        Returns:
            Path to generated image
        """
        
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        try:
            font_size = 50
            font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 50)
            except:
                font = ImageFont.load_default()
        
        max_width = int(width * 0.8)
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            line_text = ' '.join(current_line)
            
            try:
                bbox = draw.textbbox((0, 0), line_text, font=font)
                line_width = bbox[2] - bbox[0]
            except:
                line_width = len(line_text) * 30
            
            if line_width > max_width and len(current_line) > 1:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        line_height = 80
        total_height = len(lines) * line_height
        
        if position == 'bottom':
            y_start = height - total_height - 100
        else:
            y_start = (height - total_height) // 2
        
        outline_width = 3
        
        for i, line in enumerate(lines):
            y = y_start + i * line_height
            x = width // 2
            
            try:
                bbox = draw.textbbox((x, y), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) // 2
            except:
                x = width // 2
            
            for adj_x in range(-outline_width, outline_width + 1):
                for adj_y in range(-outline_width, outline_width + 1):
                    draw.text((x + adj_x, y + adj_y), line, font=font, fill=(0, 0, 0, 255))
            
            draw.text((x, y), line, font=font, fill=(255, 255, 255, 255))
        
        Path('temp_subtitles').mkdir(exist_ok=True)
        filepath = f"temp_subtitles/subtitle_{hash(text) % 1000000}.png"
        img.save(filepath)
        
        return filepath


class HookText:
    """Generate hook text overlays for first 3 seconds."""
    
    @staticmethod
    def create_hook_image(
        keyword: str,
        language: str = 'english',
        width: int = 1080,
        height: int = 1920
    ) -> str:
        """Create hook text image."""
        
        img = Image.new('RGBA', (width, height), (0, 0, 0, 200))
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 80)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
            except:
                font = ImageFont.load_default()
        
        if language == 'hindi':
            title = f"{keyword.upper()}\nके फायदे"
        else:
            title = f"Benefits Of\n{keyword.upper()}"
        
        try:
            bbox = draw.textbbox((0, 0), title, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except:
            text_width = len(title) * 40
            text_height = 200
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        outline_width = 4
        
        for adj_x in range(-outline_width, outline_width + 1):
            for adj_y in range(-outline_width, outline_width + 1):
                draw.text((x + adj_x, y + adj_y), title, font=font, fill=(0, 0, 0, 255))
        
        draw.text((x, y), title, font=font, fill=(255, 215, 0, 255))
        
        Path('temp_hooks').mkdir(exist_ok=True)
        filepath = f"temp_hooks/hook_{hash(keyword) % 1000000}.png"
        img.save(filepath)
        
        return filepath


class CTAText:
    """Generate call-to-action text for last 3 seconds."""
    
    @staticmethod
    def create_cta_image(
        language: str = 'english',
        width: int = 1080,
        height: int = 1920
    ) -> str:
        """Create CTA text image."""
        
        img = Image.new('RGBA', (width, height), (0, 0, 0, 200))
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 60)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
            except:
                font = ImageFont.load_default()
        
        if language == 'hindi':
            cta_text = "और सीखने के लिए Follow करें!\n\nAur Seekhne Ke Liye Follow Karein!"
        else:
            cta_text = "Follow for More Knowledge\n\nDon't Miss Out!"
        
        try:
            bbox = draw.textbbox((0, 0), cta_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except:
            text_width = len(cta_text) * 30
            text_height = 200
        
        x = (width - text_width) // 2
        y = height - text_height - 150
        
        outline_width = 3
        
        for adj_x in range(-outline_width, outline_width + 1):
            for adj_y in range(-outline_width, outline_width + 1):
                draw.text((x + adj_x, y + adj_y), cta_text, font=font, fill=(0, 0, 0, 255))
        
        draw.text((x, y), cta_text, font=font, fill=(255, 255, 255, 255))
        
        Path('temp_ctas').mkdir(exist_ok=True)
        filepath = f"temp_ctas/cta_{language}_{hash(cta_text) % 1000000}.png"
        img.save(filepath)
        
        return filepath


class VideoEngine:
    """Main professional video generation engine."""
    
    REEL_WIDTH = 1080
    REEL_HEIGHT = 1920
    FPS = 30
    
    def __init__(self, output_dir: str = 'output'):
        """Initialize video engine."""
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        logger.info("[VIDEO] Professional video engine initialized")
    
    def create_reel(
        self,
        video_clips: List[str],
        audio_path: str,
        music_path: Optional[str],
        script_sentences: List[str],
        keyword: str,
        language: str = 'english',
        output_filename: str = 'reel.mp4'
    ) -> Optional[str]:
        """
        Create professional Instagram reel.
        
        Args:
            video_clips: List of video file paths
            audio_path: Voice audio file path
            music_path: Background music file path
            script_sentences: List of script sentences for subtitles
            keyword: Topic keyword
            language: 'english' or 'hindi'
            output_filename: Output video filename
            
        Returns:
            Path to output video or None
        """
        
        try:
            logger.info("\n[VIDEO] ========== CREATING PROFESSIONAL REEL ==========")
            
            # Load voice audio
            logger.info(f"[VIDEO] Loading voice audio: {audio_path}")
            voice_audio = AudioFileClip(audio_path)
            voice_duration = voice_audio.duration
            logger.info(f"[VIDEO] Voice duration: {voice_duration:.2f}s")
            
            # Debug print
            logger.info(f"[DEBUG] Script sentences: {len(script_sentences)}")
            for i, sent in enumerate(script_sentences, 1):
                logger.info(f"[DEBUG]   {i}. {sent[:60]}...")
            
            # Calculate timing
            total_duration = voice_duration
            hook_duration = 3.0
            cta_duration = 3.0
            content_duration = total_duration - hook_duration - cta_duration
            
            if content_duration <= 0:
                logger.error("[VIDEO] Total duration too short")
                return None
            
            sentence_duration = content_duration / len(script_sentences)
            
            logger.info(f"[VIDEO] Structure:")
            logger.info(f"  - Hook: {hook_duration:.1f}s")
            logger.info(f"  - Content: {content_duration:.1f}s ({len(script_sentences)} sentences)")
            logger.info(f"  - CTA: {cta_duration:.1f}s")
            logger.info(f"  - Per sentence: {sentence_duration:.2f}s")
            
            # Process video clips
            logger.info(f"[VIDEO] Processing {len(video_clips)} video clips")
            processed_clips = self._prepare_video_clips(
                video_clips,
                sentence_duration,
                len(script_sentences)
            )
            
            if len(processed_clips) < 3:
                logger.error("[VIDEO] Not enough valid video clips")
                return None
            
            logger.info(f"[DEBUG] Clips used: {len(processed_clips)}")
            
            # Create hook
            logger.info("[VIDEO] Creating hook text")
            hook_image_path = HookText.create_hook_image(keyword, language)
            hook_clip = ImageClip(hook_image_path).set_duration(hook_duration)
            
            # Create content clips with subtitles
            logger.info("[VIDEO] Creating content with subtitles")
            content_clips = []
            
            for i, sentence in enumerate(script_sentences):
                if i < len(processed_clips):
                    video_clip = processed_clips[i]
                    video_clip = video_clip.set_duration(sentence_duration)
                else:
                    # Reuse clips if we run out
                    video_clip = processed_clips[i % len(processed_clips)]
                    video_clip = video_clip.set_duration(sentence_duration)
                
                # Create subtitle
                logger.info(f"[VIDEO] Subtitle {i+1}/{len(script_sentences)}: {sentence[:50]}...")
                subtitle_image_path = SubtitleSystem.create_subtitle_image(
                    sentence,
                    duration_sec=sentence_duration,
                    position='bottom'
                )
                
                subtitle_clip = ImageClip(subtitle_image_path).set_duration(sentence_duration)
                
                # Composite
                composite = CompositeVideoClip([
                    video_clip.resize((self.REEL_WIDTH, self.REEL_HEIGHT)),
                    subtitle_clip.set_position(('center', 'bottom'))
                ])
                
                content_clips.append(composite)
            
            # Create CTA
            logger.info("[VIDEO] Creating CTA text")
            cta_image_path = CTAText.create_cta_image(language)
            cta_clip = ImageClip(cta_image_path).set_duration(cta_duration)
            
            # Combine all clips
            logger.info("[VIDEO] Combining all clips")
            all_clips = [hook_clip] + content_clips + [cta_clip]
            
            try:
                final_video = concatenate_videoclips(all_clips, method='chain')
            except Exception as e:
                logger.error(f"[VIDEO] Concatenation error: {e}")
                final_video = concatenate_videoclips(all_clips)
            
            logger.info(f"[VIDEO] ✓ Video assembled: {final_video.duration:.2f}s")
            
            # Mix audio
            logger.info("[VIDEO] Mixing audio tracks")
            
            final_audio = voice_audio
            
            if music_path and os.path.exists(music_path):
                try:
                    logger.info(f"[VIDEO] Loading music: {music_path}")
                    music = AudioFileClip(music_path)
                    
                    if music.duration < voice_duration:
                        repeat_count = int(voice_duration / music.duration) + 1
                        music = concatenate_audioclips([music] * repeat_count)
                    
                    music = music.subclip(0, voice_duration)
                    
                    voice_audio = voice_audio.volumex(1.0)
                    music = music.volumex(0.12)
                    
                    final_audio = CompositeAudioClip([voice_audio, music])
                    logger.info("[VIDEO] ✓ Music mixed (12% volume)")
                    
                except Exception as e:
                    logger.warning(f"[VIDEO] Music mixing failed: {e}")
                    logger.info("[VIDEO] Using voice only")
            else:
                logger.info("[VIDEO] No music available - voice only")
            
            final_video = final_video.set_audio(final_audio)
            
            # Resize
            logger.info("[VIDEO] Resizing to Instagram specs (1080x1920)")
            final_video = final_video.resize((self.REEL_WIDTH, self.REEL_HEIGHT))
            
            # Export
            output_path = os.path.join(self.output_dir, output_filename)
            logger.info(f"[VIDEO] Exporting to: {output_path}")
            logger.info("[VIDEO] Settings: 1080x1920, 30fps, H.264, AAC")
            
            try:
                final_video.write_videofile(
                    output_path,
                    fps=self.FPS,
                    codec='libx264',
                    audio_codec='aac',
                    verbose=False,
                    logger=None
                )
            except Exception as e:
                logger.warning(f"[VIDEO] Export with music failed: {e}")
                logger.info("[VIDEO] Retrying with voice only...")
                
                # Use voice-only version
                final_video_voice_only = final_video.set_audio(voice_audio)
                try:
                    final_video_voice_only.write_videofile(
                        output_path,
                        fps=self.FPS,
                        codec='libx264',
                        audio_codec='aac',
                        verbose=False,
                        logger=None
                    )
                    logger.info(f"[VIDEO] ✓ Successfully exported (voice only): {os.path.basename(output_path)}")
                    return output_path
                except Exception as e2:
                    logger.error(f"[VIDEO] Export failed even with voice only: {e2}")
                    return None
            
            logger.info(f"[VIDEO] ✓✓✓ REEL COMPLETE: {output_path}")
            logger.info(f"[VIDEO] Duration: {final_video.duration:.2f}s")
            
            final_video.close()
            voice_audio.close()
            
            return output_path
            
        except Exception as e:
            logger.error(f"[VIDEO] Reel creation failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    def _prepare_video_clips(
        self,
        video_paths: List[str],
        clip_duration: float,
        num_clips_needed: int
    ) -> List[VideoFileClip]:
        """Prepare and validate video clips."""
        
        prepared_clips = []
        max_retries = 2
        
        for i, video_path in enumerate(video_paths):
            if len(prepared_clips) >= num_clips_needed:
                break
            
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    if not os.path.exists(video_path):
                        logger.warning(f"[VIDEO] Video not found: {video_path}")
                        break
                    
                    clip = VideoFileClip(video_path)
                    
                    if clip.duration < clip_duration:
                        logger.warning(f"[VIDEO] Clip too short ({clip.duration:.1f}s)")
                        clip = clip.speedx(0.9)
                    
                    trimmed = clip.subclip(0, min(clip_duration, clip.duration))
                    prepared_clips.append(trimmed)
                    
                    logger.info(f"[VIDEO] Loaded clip {i+1}: {clip_duration:.2f}s")
                    break
                    
                except Exception as e:
                    retry_count += 1
                    logger.warning(f"[VIDEO] Clip load error (attempt {retry_count}): {e}")
        
        if len(prepared_clips) < 3:
            logger.error(f"[VIDEO] Only {len(prepared_clips)} valid clips (need 3+)")
        
        return prepared_clips
