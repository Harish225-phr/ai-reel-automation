"""
Upload Module for AI Reel Automation.
Handles uploading generated reels to various platforms (YouTube, TikTok, etc.)
Uses Selenium for automation.
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from utils import logger


# ==================== YOUTUBE UPLOAD ====================
class YouTubeUploader:
    """Handle YouTube video uploads using Selenium."""
    
    def __init__(self, email, password, headless=False):
        """
        Initialize YouTube uploader.
        
        Args:
            email (str): YouTube account email
            password (str): YouTube account password
            headless (bool): Run browser in headless mode
        """
        self.email = email
        self.password = password
        self.driver = None
        self.headless = headless
        self.wait = None
        
        logger.info("YouTube Uploader initialized")
    
    def setup_driver(self):
        """Setup Chrome WebDriver with options."""
        try:
            logger.info("Setting up Chrome WebDriver...")
            
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless")
            
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 20)
            
            logger.info("✓ WebDriver setup complete")
            
        except Exception as e:
            logger.error(f"Error setting up WebDriver: {e}")
            raise
    
    def login(self):
        """Login to YouTube account."""
        try:
            logger.info("Logging into YouTube...")
            
            self.driver.get("https://youtube.com")
            time.sleep(2)
            
            # Click sign in
            sign_in_button = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Sign in"))
            )
            sign_in_button.click()
            
            time.sleep(2)
            
            # Enter email
            email_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "identifierId"))
            )
            email_input.send_keys(self.email)
            
            next_button = self.driver.find_element(By.ID, "identifierNext")
            next_button.click()
            
            time.sleep(2)
            
            # Enter password
            password_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_input.send_keys(self.password)
            
            next_button = self.driver.find_element(By.ID, "passwordNext")
            next_button.click()
            
            time.sleep(3)
            
            logger.info("✓ Login successful")
            
        except Exception as e:
            logger.error(f"Login failed: {e}")
            raise
    
    def upload_video(self, video_path, title, description, tags, is_private=False):
        """
        Upload video to YouTube.
        
        Args:
            video_path (str): Path to video file
            title (str): Video title
            description (str): Video description
            tags (list): List of tags/hashtags
            is_private (bool): Upload as private video
            
        Returns:
            bool: True if upload successful
        """
        try:
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video not found: {video_path}")
            
            logger.info(f"Uploading video: {title}")
            
            # Navigate to upload page
            self.driver.get("https://www.youtube.com/upload")
            time.sleep(2)
            
            # Click on file input
            file_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
            
            # Get absolute path
            absolute_path = os.path.abspath(video_path)
            file_input.send_keys(absolute_path)
            
            logger.info("File uploaded, waiting for processing...")
            time.sleep(5)
            
            # Fill title
            logger.info("Filling video details...")
            title_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "title"))
            )
            title_input.clear()
            title_input.send_keys(title)
            
            time.sleep(1)
            
            # Fill description
            description_input = self.driver.find_element(By.ID, "description")
            description_input.clear()
            description_input.send_keys(description)
            
            time.sleep(1)
            
            # Add tags
            tags_input = self.driver.find_element(By.ID, "keywords")
            tags_text = ", ".join(tags)
            tags_input.send_keys(tags_text)
            
            time.sleep(1)
            
            # Set visibility
            if is_private:
                private_radio = self.driver.find_element(
                    By.XPATH, "//input[@value='PRIVATE']"
                )
                private_radio.click()
                logger.info("Set to private")
            
            time.sleep(1)
            
            # Publish
            logger.info("Publishing video...")
            publish_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "submit-button"))
            )
            publish_button.click()
            
            # Wait for upload to complete
            logger.info("Waiting for upload to complete...")
            time.sleep(30)
            
            logger.info("✓ Video uploaded successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Upload failed: {e}")
            return False
    
    def close(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed")


# ==================== BATCH UPLOAD ====================
def batch_upload_to_youtube(
    video_list,
    email,
    password,
    headless=False
):
    """
    Upload multiple videos to YouTube.
    
    Args:
        video_list (list): List of dicts with video info
        email (str): YouTube email
        password (str): YouTube password
        headless (bool): Run browser headless
        
    Returns:
        list: Upload results
    """
    try:
        logger.info(f"Starting batch upload of {len(video_list)} videos...")
        
        uploader = YouTubeUploader(email, password, headless=headless)
        uploader.setup_driver()
        uploader.login()
        
        results = []
        
        for idx, video_info in enumerate(video_list):
            logger.info(f"\nUploading video {idx+1}/{len(video_list)}")
            
            try:
                success = uploader.upload_video(
                    video_path=video_info['video_path'],
                    title=video_info.get('title', video_info.get('topic')),
                    description=video_info.get('description', video_info.get('script')),
                    tags=video_info.get('hashtags', []),
                    is_private=video_info.get('is_private', False)
                )
                
                results.append({
                    'video': video_info['video_path'],
                    'success': success
                })
                
            except Exception as e:
                logger.error(f"Failed to upload video {idx+1}: {e}")
                results.append({
                    'video': video_info['video_path'],
                    'success': False,
                    'error': str(e)
                })
        
        uploader.close()
        
        successful = sum(1 for r in results if r['success'])
        logger.info(f"\n✓ Batch upload complete: {successful}/{len(video_list)} successful")
        
        return results
    
    except Exception as e:
        logger.error(f"Batch upload error: {e}")
        raise


# ==================== HELPER FUNCTIONS ====================
def prepare_upload_data(reel_data):
    """
    Prepare reel data for upload.
    
    Args:
        reel_data (dict): Reel information
        
    Returns:
        dict: Formatted upload data
    """
    try:
        upload_data = {
            'video_path': reel_data['video_path'],
            'title': reel_data['topic'],
            'description': reel_data['captions'][0],
            'hashtags': reel_data['hashtags'],
            'is_private': False
        }
        
        return upload_data
    
    except Exception as e:
        logger.error(f"Error preparing upload data: {e}")
        raise


# ==================== MANUAL UPLOAD GUIDE ====================
def print_upload_guide():
    """Print manual upload instructions."""
    
    guide = """
    
╔════════════════════════════════════════════════════════════════╗
║              MANUAL VIDEO UPLOAD GUIDE                         ║
╚════════════════════════════════════════════════════════════════╝

📥 UPLOADING YOUR REEL

1️⃣  LOCAL PLATFORMS (Recommended for beginners)
   
   YouTube:
   - Go to https://www.youtube.com/upload
   - Upload your video from output/ folder
   - Copy caption and hashtags from the console output
   - Set visibility to Public or Unlisted
   - Publish!
   
   Instagram Reels:
   - Open Instagram and go to Create
   - Select "Reels"
   - Upload video from output/ folder
   - Add caption and hashtags
   - Share!
   
   TikTok:
   - Open TikTok and tap +
   - Select "Upload a video"
   - Choose video from output/ folder
   - Add caption, hashtags, and sounds
   - Publish!

2️⃣  AUTOMATED UPLOAD (Advanced)
   
   To use automated YouTube upload:
   
   from upload import YouTubeUploader
   
   uploader = YouTubeUploader('your@email.com', 'your_password')
   uploader.setup_driver()
   uploader.login()
   uploader.upload_video(
       'output/reel_20240101_120000.mp4',
       'Your Title',
       'Your Description',
       ['tag1', 'tag2']
   )
   uploader.close()

3️⃣  CAPTIONS & HASHTAGS
   
   The system automatically generates:
   - Video captions (shown in console)
   - Relevant hashtags
   - Full description with hashtags
   
   Copy these directly to your platform!

4️⃣  VIDEO SPECS
   
   Resolution: 1080x1920 (9:16 aspect ratio)
   Duration: Variable (usually 15-60 seconds)
   Format: MP4
   Codec: H.264
   
   These specs work perfectly for:
   - YouTube Shorts
   - Instagram Reels
   - TikTok Videos
   - Facebook Reels

════════════════════════════════════════════════════════════════

Need help? Check reel_generator.log for detailed information.

════════════════════════════════════════════════════════════════
    """
    
    print(guide)
    logger.info(guide)


if __name__ == "__main__":
    print_upload_guide()
