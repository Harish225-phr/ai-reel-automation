"""
Image Fetcher Module for AI Reel Automation.
Downloads relevant images from free sources (Unsplash, Pexels, Pixabay, DuckDuckGo).
"""

import os
import requests
import random
from pathlib import Path
from utils import logger


class ImageFetcher:
    """Fetch and download images from multiple free sources."""
    
    # API Keys (without keys, public endpoints still work with rate limits)
    UNSPLASH_ACCESS_KEY = "YOUR_UNSPLASH_KEY"  # Get from https://unsplash.com/oauth/applications
    PEXELS_API_KEY = "YOUR_PEXELS_KEY"  # Get from https://www.pexels.com/api/
    PIXABAY_API_KEY = "YOUR_PIXABAY_KEY"  # Get from https://pixabay.com/api/docs/
    
    def __init__(self, output_dir='images'):
        self.output_dir = output_dir
        Path(output_dir).mkdir(exist_ok=True)
    
    @staticmethod
    def download_from_unsplash(keyword, count=5):
        """
        Download images from Unsplash (free source, no key required for basic access).
        Uses search endpoint without authentication.
        """
        try:
            logger.info(f"Fetching from Unsplash: '{keyword}'")
            
            # Use Unsplash search API (public access available)
            url = "https://api.unsplash.com/search/photos"
            params = {
                'query': keyword,
                'per_page': count,
                'order_by': 'relevant',
                'client_id': ImageFetcher.UNSPLASH_ACCESS_KEY or 'demo'
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                logger.warning(f"Unsplash responded with {response.status_code}")
                return []
            
            data = response.json()
            images = []
            for item in data.get('results', []):
                images.append({
                    'url': item['urls']['regular'],
                    'alt': item['description'] or keyword,
                    'source': 'unsplash'
                })
            
            logger.info(f"[OK] Got {len(images)} from Unsplash")
            return images
            
        except Exception as e:
            logger.warning(f"Unsplash fetch failed: {e}")
            return []
    
    @staticmethod
    def download_from_pexels(keyword, count=5):
        """
        Download images from Pexels (free, high quality).
        Requires API key but public search works with rate limiting.
        """
        try:
            logger.info(f"Fetching from Pexels: '{keyword}'")
            
            url = "https://api.pexels.com/v1/search"
            headers = {
                'Authorization': ImageFetcher.PEXELS_API_KEY or 'demo'
            }
            params = {
                'query': keyword,
                'per_page': count,
                'page': 1
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code != 200:
                logger.warning(f"Pexels responded with {response.status_code}")
                return []
            
            data = response.json()
            images = []
            for item in data.get('photos', []):
                images.append({
                    'url': item['src']['large'],
                    'alt': f"{item['photographer']} photo",
                    'source': 'pexels'
                })
            
            logger.info(f"[OK] Got {len(images)} from Pexels")
            return images
            
        except Exception as e:
            logger.warning(f"Pexels fetch failed: {e}")
            return []
    
    @staticmethod
    def download_from_pixabay(keyword, count=5):
        """
        Download images from Pixabay (free, large collection).
        """
        try:
            logger.info(f"Fetching from Pixabay: '{keyword}'")
            
            url = "https://pixabay.com/api/"
            params = {
                'key': ImageFetcher.PIXABAY_API_KEY or 'demo',
                'q': keyword,
                'per_page': count,
                'image_type': 'photo',
                'order': 'popular'
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                logger.warning(f"Pixabay responded with {response.status_code}")
                return []
            
            data = response.json()
            images = []
            for item in data.get('hits', []):
                images.append({
                    'url': item['largeImageURL'],
                    'alt': item['user'],
                    'source': 'pixabay'
                })
            
            logger.info(f"[OK] Got {len(images)} from Pixabay")
            return images
            
        except Exception as e:
            logger.warning(f"Pixabay fetch failed: {e}")
            return []
    
    @staticmethod
    def download_from_duckduckgo(keyword, count=5):
        """
        Download images using DuckDuckGo image search (no API key needed).
        Note: This uses basic web scraping and may be less reliable.
        """
        try:
            logger.info(f"Fetching from DuckDuckGo: '{keyword}'")
            
            # Using DuckDuckGo Lite doesn't require JavaScript
            url = f"https://duckduckgo.com/i.js"
            params = {
                'q': keyword,
                'l': 'en_US',
                'vqd': '',
                'b': '',
                'p': '1'
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code != 200:
                logger.warning(f"DuckDuckGo responded with {response.status_code}")
                return []
            
            data = response.json()
            images = []
            for item in data.get('results', [])[:count]:
                if 'image' in item:
                    images.append({
                        'url': item['image'],
                        'alt': keyword,
                        'source': 'duckduckgo'
                    })
            
            if images:
                logger.info(f"[OK] Got {len(images)} from DuckDuckGo")
            return images
            
        except Exception as e:
            logger.warning(f"DuckDuckGo fetch failed: {e}")
            return []
    
    def download_images(self, keyword, count=5, retry_count=0):
        """
        Download images with fallback sources.
        Tries multiple sources until we have enough images.
        """
        images = []
        max_retries = 3
        
        try:
            logger.info(f"Downloading {count} images for '{keyword}'")
            
            # Try sources in order with fallbacks
            sources = [
                self.download_from_unsplash,
                self.download_from_pexels,
                self.download_from_pixabay,
                self.download_from_duckduckgo
            ]
            
            for source_func in sources:
                if len(images) >= count:
                    break
                
                new_images = source_func(keyword, count - len(images))
                images.extend(new_images)
            
            # If still not enough images, try broader search
            if len(images) < count and retry_count < max_retries:
                logger.warning(f"Got {len(images)}/{count} images, retrying with broader keyword...")
                broader_keyword = keyword.split()[0]  # Try first word only
                retry_images = self.download_images(broader_keyword, count - len(images), retry_count + 1)
                images.extend(retry_images)
            
            # If still not enough, try generic fallback
            if len(images) < count and retry_count < max_retries:
                logger.warning(f"Still need {count - len(images)} images, trying generic search...")
                generic_images = self.download_images('nature', count - len(images), retry_count + 1)
                images.extend(generic_images)
            
            logger.info(f"[OK] Got {len(images)} images total")
            return images[:count]  # Return only what we need
            
        except Exception as e:
            logger.error(f"Error downloading images: {e}")
            return self.get_local_fallback(count)
    
    def save_images(self, images, keyword):
        """
        Save downloaded images to disk.
        
        Args:
            images (list): List of image dicts with 'url' and 'alt'
            keyword (str): Keyword for organizing files
            
        Returns:
            list: Paths to saved images
        """
        saved_paths = []
        
        for idx, img_data in enumerate(images):
            try:
                # Download image
                response = requests.get(img_data['url'], timeout=10)
                if response.status_code != 200:
                    logger.warning(f"Failed to download image {idx+1}")
                    continue
                
                # Save to disk
                filename = f"reel_{keyword.replace(' ', '_')}_{idx+1}.jpg"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                saved_paths.append(filepath)
                logger.debug(f"[OK] Saved: {filename}")
                
            except Exception as e:
                logger.warning(f"Could not save image {idx+1}: {e}")
                continue
        
        logger.info(f"[OK] Saved {len(saved_paths)} images")
        return saved_paths
    
    def get_local_fallback(self, count=5):
        """
        Fallback: Use existing images from images/ folder.
        """
        try:
            local_images = list(Path(self.output_dir).glob('*.jpg')) + \
                          list(Path(self.output_dir).glob('*.png'))
            
            if local_images:
                selected = random.sample(local_images, min(count, len(local_images)))
                logger.info(f"[OK] Using {len(selected)} local fallback images")
                return [str(p) for p in selected]
            
            logger.warning("No local images found as fallback")
            return []
            
        except Exception as e:
            logger.error(f"Error getting local fallback: {e}")
            return []
    
    def fetch_and_save(self, keyword, count=5):
        """
        Complete pipeline: fetch and save images.
        
        Args:
            keyword (str): Search keyword
            count (int): Number of images needed
            
        Returns:
            list: Paths to saved images
        """
        try:
            # Download images
            images = self.download_images(keyword, count)
            
            if not images:
                logger.warning("No images downloaded, using local fallback")
                return self.get_local_fallback(count)
            
            # Save images
            saved_paths = self.save_images(images, keyword)
            
            if not saved_paths:
                logger.warning("Failed to save images, using local fallback")
                return self.get_local_fallback(count)
            
            return saved_paths
            
        except Exception as e:
            logger.error(f"Error in fetch_and_save: {e}")
            return self.get_local_fallback(count)


def fetch_images(keyword, count=5, output_dir='images'):
    """Convenience function to fetch and save images."""
    fetcher = ImageFetcher(output_dir)
    return fetcher.fetch_and_save(keyword, count)
