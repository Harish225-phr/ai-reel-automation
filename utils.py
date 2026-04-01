"""
Utility functions for AI Reel Automation System.
Handles file operations, logging, and common helper functions.
"""

import os
import logging
import sys
from datetime import datetime
from pathlib import Path


# ==================== LOGGING SETUP ====================
def setup_logger(name="AIReel", log_file="reel_generator.log"):
    """
    Configure and return a logger instance.
    
    Args:
        name (str): Logger name
        log_file (str): Output log file name
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger


logger = setup_logger()


# ==================== DIRECTORY MANAGEMENT ====================
def ensure_directories():
    """Create required directories if they don't exist."""
    required_dirs = ['audio', 'images', 'music', 'output', 'scripts', 'content']
    
    for directory in required_dirs:
        Path(directory).mkdir(exist_ok=True)
        logger.debug(f"[OK] Directory '{directory}' ready")


def check_files_exist(files_dict):
    """
    Check if required files exist.
    
    Args:
        files_dict (dict): Dictionary with file paths and descriptions
        
    Returns:
        bool: True if all files exist, False otherwise
    """
    missing_files = []
    
    for file_path, description in files_dict.items():
        if not os.path.exists(file_path):
            missing_files.append(f"{description} ({file_path})")
    
    if missing_files:
        for missing in missing_files:
            logger.warning(f"Missing: {missing}")
        return False
    
    return True


# ==================== FILE OPERATIONS ====================
def read_topics(topics_file="topics.txt"):
    """
    Read topics from file.
    
    Args:
        topics_file (str): Path to topics file
        
    Returns:
        list: List of topics (stripped of whitespace)
    """
    try:
        if not os.path.exists(topics_file):
            logger.error(f"Topics file not found: {topics_file}")
            raise FileNotFoundError(f"Cannot find {topics_file}")
        
        with open(topics_file, 'r', encoding='utf-8') as file:
            topics = [line.strip() for line in file.readlines() if line.strip()]
        
        if not topics:
            logger.error("Topics file is empty")
            raise ValueError("No topics found in file")
        
        logger.info(f"[OK] Loaded {len(topics)} topics")
        return topics
    
    except Exception as e:
        logger.error(f"Error reading topics: {e}")
        raise


def get_random_images(images_dir="images", count=5):
    """
    Get random images from directory.
    
    Args:
        images_dir (str): Path to images directory
        count (int): Number of images to select
        
    Returns:
        list: List of image paths
    """
    try:
        if not os.path.exists(images_dir):
            logger.error(f"Images directory not found: {images_dir}")
            raise FileNotFoundError(f"Cannot find {images_dir}")
        
        # Get supported image formats
        supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'}
        images = [
            f for f in os.listdir(images_dir)
            if os.path.splitext(f)[1].lower() in supported_formats
        ]
        
        if not images:
            logger.error(f"No images found in {images_dir}")
            raise FileNotFoundError(f"No images in {images_dir}")
        
        # Select random images
        import random
        selected = random.sample(images, min(count, len(images)))
        image_paths = [os.path.join(images_dir, img) for img in selected]
        
        logger.info(f"[OK] Selected {len(selected)} random images")
        return image_paths
    
    except Exception as e:
        logger.error(f"Error getting images: {e}")
        raise


def get_random_music(music_dir="music"):
    """
    Get a random music file from directory.
    
    Args:
        music_dir (str): Path to music directory
        
    Returns:
        str: Path to random music file (or None if no music available)
    """
    try:
        if not os.path.exists(music_dir):
            logger.warning(f"Music directory not found: {music_dir}")
            return None
        
        # Supported audio formats
        supported_formats = {'.mp3', '.wav', '.aac', '.m4a', '.flac'}
        music_files = [
            f for f in os.listdir(music_dir)
            if os.path.splitext(f)[1].lower() in supported_formats
        ]
        
        if not music_files:
            logger.warning(f"No music files found in {music_dir}")
            return None
        
        import random
        selected_music = random.choice(music_files)
        music_path = os.path.join(music_dir, selected_music)
        
        logger.info(f"[OK] Selected music: {selected_music}")
        return music_path
    
    except Exception as e:
        logger.error(f"Error getting music: {e}")
        return None


# ==================== VALIDATION ====================
def get_image_dimensions(image_path):
    """
    Get image dimensions without loading the full image.
    
    Args:
        image_path (str): Path to image
        
    Returns:
        tuple: (width, height) or None if error
    """
    try:
        from PIL import Image
        with Image.open(image_path) as img:
            return img.size
    except Exception as e:
        logger.error(f"Error getting image dimensions for {image_path}: {e}")
        return None


def is_image_vertical(image_path):
    """
    Check if image has vertical orientation.
    
    Args:
        image_path (str): Path to image
        
    Returns:
        bool: True if height > width
    """
    dims = get_image_dimensions(image_path)
    if dims:
        return dims[1] > dims[0]  # height > width
    return False


# ==================== TIMESTAMP & NAMING ====================
def get_timestamp():
    """Get current timestamp for file naming."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def get_output_filename(extension=".mp4"):
    """
    Generate unique output filename with timestamp.
    
    Args:
        extension (str): File extension
        
    Returns:
        str: Filename with timestamp
    """
    timestamp = get_timestamp()
    return f"reel_{timestamp}{extension}"


def sanitize_filename(filename):
    """
    Sanitize filename by removing invalid characters.
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Sanitized filename
    """
    invalid_chars = r'<>:"/\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


# ==================== PROGRESS TRACKING ====================
def print_progress(current, total, task_name="Processing"):
    """
    Print progress bar.
    
    Args:
        current (int): Current item number
        total (int): Total items
        task_name (str): Task description
    """
    percentage = (current / total) * 100
    filled = int(percentage / 5)
    bar = '#' * filled + '-' * (20 - filled)
    logger.info(f"{task_name}: [{bar}] {percentage:.1f}% ({current}/{total})")


# ==================== DEPENDENCY CHECK ====================
def check_dependencies():
    """Check if all required packages are installed."""
    required_packages = {
        'moviepy': 'moviepy',
        'gtts': 'gTTS',
        'PIL': 'Pillow',
        'selenium': 'selenium'
    }
    
    missing = []
    
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package_name)
    
    if missing:
        logger.error(f"Missing packages: {', '.join(missing)}")
        logger.error(f"Install with: pip install {' '.join(missing)}")
        raise ImportError(f"Missing dependencies: {', '.join(missing)}")
    
    logger.info("[OK] All dependencies installed")


if __name__ == "__main__":
    print("Utilities module loaded successfully")
    check_dependencies()
    ensure_directories()
