"""
STABLE VIDEO ENGINE - Reliability First
Enforces: Minimum 3 clips, Default music fallback, Edge TTS only, Comprehensive debug
"""

import os
from pathlib import Path
from PIL import Image

# Pillow 11 compatibility
try:
    Image.ANTIALIAS = Image.Resampling.LANCZOS
except AttributeError:
    pass

from moviepy.editor import (
    VideoFileClip, ImageClip, AudioFileClip, 
    concatenate_videoclips, CompositeVideoClip, 
    ColorClip, TextClip, CompositeAudioClip, concatenate_audioclips
)
import config


class StableVideoEngine:
    """
    Reliable video engine focused on stability and guaranteed output.
    
    Rules:
    1. Minimum 3 video clips required - STOP if less
    2. Never fallback to black screen
    3. Always use default music if API fails
    4. Use only Edge TTS for voice
    5. Print debug info for every step
    """
    
    REQUIRED_CLIP_COUNT = 3
    DEFAULT_MUSIC_PATH = Path(__file__).parent / "assets" / "music" / "music_motivational_270686.wav"
    FALLBACK_MUSIC_PATHS = [
        Path(__file__).parent / "assets" / "music" / "music_motivational_270686.wav",
        Path(__file__).parent / "assets" / "music" / "music_calm_482679.wav",
    ]
    
    def __init__(self, output_dir='output'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True, parents=True)
        print(f"\n[VIDEO_ENGINE] ✓ Initialized: {self.output_dir}")
    
    def validate_clips(self, video_paths: list) -> bool:
        """
        RULE 1: Validate minimum 3 clips exist and are valid.
        Stop generation if less than 3 clips.
        """
        print(f"\n[DEBUG] Validating clips...")
        print(f"[DEBUG] Received {len(video_paths)} clip paths")
        
        if not video_paths:
            print(f"[ERROR] ✗ NO CLIPS PROVIDED!")
            print(f"[ERROR] Minimum required: {self.REQUIRED_CLIP_COUNT}")
            print(f"[ERROR] STOPPING GENERATION - Cannot create black screen fallback")
            raise ValueError(f"No video clips provided. Minimum {self.REQUIRED_CLIP_COUNT} required.")
        
        valid_clips = []
        for clip_path in video_paths:
            if clip_path and Path(clip_path).exists():
                valid_clips.append(clip_path)
                print(f"[DEBUG]   ✓ Clip {len(valid_clips)}: {Path(clip_path).name}")
            else:
                print(f"[DEBUG]   ✗ Invalid clip path: {clip_path}")
        
        print(f"\n[DEBUG] Valid clips: {len(valid_clips)}/{len(video_paths)}")
        
        if len(valid_clips) < self.REQUIRED_CLIP_COUNT:
            print(f"\n[ERROR] ✗ INSUFFICIENT CLIPS!")
            print(f"[ERROR] Found: {len(valid_clips)}")
            print(f"[ERROR] Required: {self.REQUIRED_CLIP_COUNT}")
            print(f"[ERROR] STOPPING GENERATION - Never use black screen fallback")
            raise ValueError(
                f"Only {len(valid_clips)} valid clips found. "
                f"Minimum {self.REQUIRED_CLIP_COUNT} required. Generation stopped."
            )
        
        print(f"[VIDEO_ENGINE] ✓ Clip validation PASSED")
        return True
    
    def get_music_file(self, fallback_music_path: str = None) -> str:
        """
        RULE 3: Get music file with default fallback.
        If provided music doesn't exist, use default.
        """
        print(f"\n[DEBUG] Resolving music file...")
        
        if fallback_music_path and Path(fallback_music_path).exists():
            print(f"[DEBUG]   ✓ Using provided music: {Path(fallback_music_path).name}")
            return fallback_music_path
        
        if fallback_music_path:
            print(f"[DEBUG]   ✗ Provided music not found: {fallback_music_path}")
        
        # Try default music
        if self.DEFAULT_MUSIC_PATH.exists():
            print(f"[DEBUG]   ✓ Using default music: {self.DEFAULT_MUSIC_PATH.name}")
            return str(self.DEFAULT_MUSIC_PATH)
        
        # Try fallback paths
        for fallback_path in self.FALLBACK_MUSIC_PATHS:
            if fallback_path.exists():
                print(f"[DEBUG]   ✓ Using fallback music: {fallback_path.name}")
                return str(fallback_path)
        
        print(f"[WARNING] ⚠ No music files found!")
        print(f"[WARNING] Music will be skipped if not available")
        return None
    
    def load_video_clip(self, video_path: str, duration: float = None) -> VideoFileClip:
        """
        Load a video clip and set duration.
        """
        try:
            clip = VideoFileClip(video_path)
            if duration and clip.duration > duration:
                # Trim to duration using subclip
                clip = clip.subclip(0, duration)
            print(f"[DEBUG]     Loaded: {Path(video_path).name} ({clip.duration:.1f}s)")
            return clip
        except Exception as e:
            raise ValueError(f"Failed to load video {video_path}: {e}")
    
    def compose_clips(self, video_paths: list, total_duration: float) -> VideoFileClip:
        """
        Compose video clips to fill total_duration.
        Repeat clips if necessary to reach duration.
        """
        print(f"\n[DEBUG] Composing {len(video_paths)} clips for {total_duration:.1f}s duration...")
        
        clips = []
        current_duration = 0
        clip_idx = 0
        
        while current_duration < total_duration:
            # Get next clip (rotate through all provided)
            video_path = video_paths[clip_idx % len(video_paths)]
            
            # Calculate how much time we need
            time_remaining = total_duration - current_duration
            
            # Load clip with duration
            clip = self.load_video_clip(video_path, duration=time_remaining)
            clips.append(clip)
            
            current_duration += clip.duration
            clip_idx += 1
        
        # Concatenate all clips
        final_clip = concatenate_videoclips(clips)
        final_clip = final_clip.subclip(0, total_duration)  # Trim to exact duration
        
        print(f"[DEBUG]   ✓ Composed {len(clips)} clip segments")
        print(f"[DEBUG]   ✓ Final composition duration: {final_clip.duration:.2f}s")
        return final_clip
    
    def create_reel(self, 
                   script: str,
                   audio_path: str,
                   video_paths: list,
                   background_music_path: str = None,
                   output_name: str = 'reel_output.mp4',
                   keyword: str = 'content') -> str:
        """
        Create final reel compositing all elements.
        
        Output:
            str: Path to output MP4 file
        """
        print(f"\n{'='*70}")
        print(f"[VIDEO_ENGINE] CREATING REEL")
        print(f"{'='*70}")
        
        try:
            # ===== VALIDATION: CLIPS =====
            print(f"\n[STEP 1/6] Validating clips...")
            self.validate_clips(video_paths)
            print(f"[VIDEO_ENGINE] ✓ {len(video_paths)} clips validated")
            
            # ===== LOAD VOICE AUDIO =====
            print(f"\n[STEP 2/6] Loading voice audio...")
            if not audio_path or not Path(audio_path).exists():
                raise FileNotFoundError(f"Voice audio not found: {audio_path}")
            
            voice_clip = AudioFileClip(audio_path)
            voice_duration = voice_clip.duration
            print(f"[DEBUG]   ✓ Voice loaded: {Path(audio_path).name} ({voice_duration:.2f}s)")
            
            # ===== COMPOSE VIDEO =====
            print(f"\n[STEP 3/6] Composing video clips...")
            video_clip = self.compose_clips(video_paths, voice_duration)
            print(f"[DEBUG]   ✓ Video composition complete: {video_clip.duration:.2f}s")
            
            # ===== PREPARE AUDIO =====
            print(f"\n[STEP 4/6] Preparing audio mix...")
            
            # Get music file
            music_path = self.get_music_file(background_music_path)
            
            # Build audio mix
            audio_clips = [voice_clip]
            if music_path and Path(music_path).exists():
                try:
                    music_clip = AudioFileClip(music_path)
                    
                    # Trim/loop music to match duration
                    if music_clip.duration < voice_duration:
                        # Loop music
                        loops_needed = int(voice_duration / music_clip.duration) + 1
                        music_parts = [music_clip for _ in range(loops_needed)]
                        music_clip = concatenate_audioclips(music_parts)
                    
                    music_clip = music_clip.subclip(0, voice_duration)
                    
                    # Volume: Voice 100%, Music 15%
                    voice_clip = voice_clip.volumex(config.VOICE_VOLUME)
                    music_clip = music_clip.volumex(config.MUSIC_VOLUME)
                    
                    audio_clips = [voice_clip, music_clip]
                    print(f"[DEBUG]   ✓ Music added: {music_clip.duration:.2f}s @ {config.MUSIC_VOLUME*100:.0f}% volume")
                except Exception as e:
                    print(f"[WARNING] ⚠ Music mixing failed: {e}")
                    print(f"[WARNING] Continuing with voice only")
            else:
                print(f"[DEBUG]   ⚠ No music file available - voice only")
            
            # Mix audio
            final_audio = CompositeAudioClip(audio_clips)
            print(f"[DEBUG]   ✓ Audio mix complete: {final_audio.duration:.2f}s")
            
            # ===== COMPOSE FINAL VIDEO =====
            print(f"\n[STEP 5/6] Compositing final video...")
            
            final_video = video_clip.set_audio(final_audio)
            print(f"[DEBUG]   ✓ Audio attached to video")
            print(f"[DEBUG]   ✓ Final video duration: {final_video.duration:.2f}s")
            
            # ===== EXPORT =====
            print(f"\n[STEP 6/6] Exporting MP4...")
            
            output_path = self.output_dir / output_name
            print(f"[DEBUG]   Output file: {output_path}")
            
            # Export with optimized settings
            final_video.write_videofile(
                str(output_path),
                fps=config.VIDEO_FPS,
                preset=config.ENCODING_PRESET,
                codec=config.VIDEO_CODEC,
                audio_codec=config.AUDIO_CODEC,
                bitrate=f"{config.VIDEO_BITRATE}k",
                verbose=False,
                logger=None,
            )
            
            # Verify output
            if not output_path.exists():
                raise FileNotFoundError(f"Export failed - output file not created: {output_path}")
            
            file_size_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"[DEBUG]   ✓ Export complete: {file_size_mb:.2f} MB")
            
            # ===== DEBUG SUMMARY =====
            print(f"\n{'='*70}")
            print(f"[VIDEO_ENGINE] ✓ REEL GENERATION SUCCESSFUL")
            print(f"{'='*70}")
            print(f"[DEBUG] Output path: {output_path}")
            print(f"[DEBUG] File size: {file_size_mb:.2f} MB")
            print(f"[DEBUG] Duration: {final_video.duration:.2f} seconds")
            print(f"[DEBUG] Clips used: {len(video_paths)}")
            print(f"[DEBUG] Music added: {'YES' if music_path else 'NO'}")
            print(f"[DEBUG] Voice file: {Path(audio_path).name if audio_path else 'MISSING'}")
            
            return str(output_path)
        
        except Exception as e:
            print(f"\n{'='*70}")
            print(f"[VIDEO_ENGINE] ✗ REEL GENERATION FAILED")
            print(f"{'='*70}")
            print(f"[ERROR] {type(e).__name__}: {e}")
            raise


# Quick test
if __name__ == '__main__':
    print("Stable Video Engine loaded successfully")
