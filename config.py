"""
Professional AI Reel Automation - Configuration
Global settings for video engine, quality, and features.
"""

# ============================================================
# VIDEO FORMAT (Instagram Reels Standard)
# ============================================================
VIDEO_WIDTH = 1080          # Vertical reel width
VIDEO_HEIGHT = 1920         # Vertical reel height
VIDEO_FPS = 20              # OPTIMIZED: 20fps (saves 30% encoding vs 24fps, still smooth for social)
VIDEO_CODEC = 'libx264'     # H.264 codec
AUDIO_CODEC = 'aac'         # AAC audio codec

# ============================================================
# TIMELINE CONFIGURATION
# ============================================================
HOOK_DURATION = 0.0         # Disabled for speed
CAPTION_DISPLAY_TIME = 3.0  # Longer display = fewer captions needed
MIN_REEL_DURATION = 15.0    # Minimum reel length
MAX_REEL_DURATION = 120.0   # Maximum reel length

# ============================================================
# AUDIO MIXING
# ============================================================
VOICE_VOLUME = 1.0          # Voice narration (100%)
MUSIC_VOLUME = 0.15         # Background music (15%)
FADE_DURATION = 0.5         # Audio fade in/out

# ============================================================
# VIDEO EFFECTS
# ============================================================
ENABLE_ZOOM = False         # Disable for speed (saves 30-40% encoding time)
ZOOM_FACTOR = 1.05          # Reduced zoom (1.0 = no zoom)
ENABLE_CROSSFADE = False    # OPTIMIZED: Skip crossfade for speed (saves 10% time)
CROSSFADE_DURATION = 0.2    # Reduced transition length (faster)

# ============================================================
# TEXT OVERLAYS
# ============================================================
ENABLE_HOOK_TEXT = False    # OPTIMIZED: Skip hook for maximum speed
ENABLE_CTA_OVERLAY = False  # OPTIMIZED: Skip CTA for maximum speed
HOOK_FONT_SIZE = 120        # Hook text size
CAPTION_FONT_SIZE = 60      # Subtitle text size
CTA_FONT_SIZE = 80          # Call-to-action size
TEXT_COLOR = (255, 255, 255)  # White
TEXT_BG_OPACITY = 180       # Semi-transparent background

# ============================================================
# PATHS
# ============================================================
OUTPUT_DIR = 'output'
AUDIO_DIR = 'audio'
VIDEO_DIR = 'videos'
IMAGES_DIR = 'images'
MUSIC_DIR = 'assets/music'
FONTS_DIR = 'assets/fonts'

# ============================================================
# VOICE SETTINGS (Edge TTS)
# ============================================================
DEFAULT_VOICE = 'en-US-AriaNeural'  # Female voice
MALE_VOICES = [
    'en-US-GuyNeural',
    'en-GB-RyanNeural',
    'en-AU-WilliamNeural',
]
FEMALE_VOICES = [
    'en-US-AriaNeural',
    'en-US-AvaNeural',
    'en-GB-SoniaNeural',
    'en-AU-NatashaNeural',
]

# ============================================================
# SCRIPT GENERATION
# ============================================================
MIN_SCRIPT_LENGTH = 200     # Minimum characters
MAX_SCRIPT_LENGTH = 600     # OPTIMIZED: Shorter scripts = shorter videos = faster rendering
TARGET_VIDEO_DURATION = 20.0  # OPTIMIZED: Target 20s (not 25s) = less processing

# ============================================================
# QUALITY SETTINGS (TURBO MODE)
# ============================================================
ENCODING_PRESET = 'superfast'  # OPTIMIZED: superfast for speed (from ultrafast)
VIDEO_BITRATE = 2000        # OPTIMIZED: Limit bitrate to 2Mbps (faster encoding, still good quality)

# ============================================================
# STOCK VIDEO SOURCES
# ============================================================
PEXELS_VIDEO_COUNT = 4      # OPTIMIZED: Fetch only 4 videos (not 10) - 60% faster download
PEXELS_VIDEO_QUALITY = 'sd'  # OPTIMIZED: Use SD (not HD) - smaller files, faster processing
PIXABAY_VIDEO_QUALITY = 'small'  # small/medium

# ============================================================
# API KEYS - PEXELS & FREESOUND
# ============================================================
PEXELS_API_KEY = "WpFsET9nVh30a0g2qOErgaePd7GuA7D8HKfOUFcaeLTJr6C6xHGT7nFv"
PIXABAY_API_KEY = "41652470-89fa37c975e9cffbf88627b9a"
FREESOUND_API_KEY = "ul0LhS7Nji1TiF5EAxSwIrNkSMpjfTjFsVKSDeSI"

# ============================================================
# CONTENT DIRECTORIES
# ============================================================
CONTENT_VIDEOS_DIR = 'content/videos'  # Pexels/stock videos
CONTENT_IMAGES_DIR = 'content/images'  # Search placeholder images

# ============================================================
# FEATURE FLAGS
# ============================================================
ENABLE_CAPTIONS = True
ENABLE_HOOK_TEXT = True
ENABLE_CTA_OVERLAY = True
ENABLE_BACKGROUND_MUSIC = True
ENABLE_ZOOM_EFFECTS = True
ENABLE_TRANSITIONS = True
ENABLE_PEXELS_API = True   # Use Pexels for stock videos
ENABLE_FREESOUND_API = True  # Use Freesound for music

# ============================================================
# LOGGING
# ============================================================
LOG_LEVEL = 'INFO'
VERBOSE_MODE = False
