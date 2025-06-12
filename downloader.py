import os
import requests
import logging
from pathlib import Path
from tqdm import tqdm
from config import Config

logger = logging.getLogger(__name__)

class FileDownloader:
    """
    Handles downloading files with progress tracking
    """
    
    def __init__(self):
        self.chunk_size = Config.CHUNK_SIZE
        self.headers = Config.HEADERS
    
    def download_file(self, url, path, headers=None):
        """
        Download a file with progress bar
        
        Args:
            url (str): URL to download from
            path (Path): Local path to save file
            headers (dict, optional): Additional headers for the request
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Merge headers
            request_headers = self.headers.copy()
            if headers:
                request_headers.update(headers)
            
            logger.info(f"Starting download: {path.name}")
            
            with requests.get(url, stream=True, headers=request_headers) as r:
                r.raise_for_status()
                total = int(r.headers.get('content-length', 0))
                
                with open(path, 'wb') as f, tqdm(
                    desc=path.name,
                    total=total,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                ) as bar:
                    for chunk in r.iter_content(chunk_size=self.chunk_size):
                        if chunk:  # filter out keep-alive chunks
                            size = f.write(chunk)
                            bar.update(size)
            
            logger.info(f"Successfully downloaded: {path.name}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error downloading {url}: {e}")
            return False
        except IOError as e:
            logger.error(f"File I/O error saving to {path}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error downloading {url}: {e}")
            return False

class ImageDownloader:
    """
    Specialized downloader for preview images
    """
    
    def __init__(self):
        self.file_downloader = FileDownloader()
    
    def download_images(self, version, target_dir, max_images=None):
        """
        Download up to max_images preview images from the model version
        
        Args:
            version (dict): Version data from API
            target_dir (Path): Directory to save images
            max_images (int, optional): Maximum number of images to download
            
        Returns:
            list: List of downloaded image paths
        """
        if max_images is None:
            max_images = Config.MAX_PREVIEW_IMAGES
        
        images = version.get("images", [])
        if not images:
            logger.info("No images found for this model version")
            return []
        
        downloaded_images = []
        downloaded_count = 0
        
        for i, image in enumerate(images[:max_images]):
            try:
                image_url = image.get("url")
                if not image_url:
                    logger.warning(f"No URL found for image {i+1}")
                    continue
                
                # Determine file extension from URL or default to jpg
                image_ext = ".jpg"
                if image_url.lower().endswith(('.png', '.jpeg', '.jpg', '.webp')):
                    image_ext = os.path.splitext(image_url.lower())[1]
                
                # Create filename
                image_filename = f"preview_{i+1:02d}{image_ext}"
                image_path = target_dir / image_filename
                
                logger.info(f"Downloading image {i+1}/{min(len(images), max_images)}: {image_filename}")
                
                if self.file_downloader.download_file(image_url, image_path):
                    downloaded_count += 1
                    downloaded_images.append(image_path)
                else:
                    logger.warning(f"Failed to download image {i+1}")
                
            except Exception as e:
                logger.error(f"Failed to process image {i+1}: {e}")
        
        logger.info(f"Downloaded {downloaded_count} images out of {min(len(images), max_images)} available")
        return downloaded_images

class ModelDownloader:
    """
    Specialized downloader for model files
    """
    
    def __init__(self):
        self.file_downloader = FileDownloader()
    
    def download_model_file(self, version, target_dir):
        """
        Download the main model file (preferring .safetensors)
        
        Args:
            version (dict): Version data from API
            target_dir (Path): Directory to save the model file
            
        Returns:
            str: Filename of downloaded model or None if failed
        """
        files = version.get("files", [])
        if not files:
            logger.warning("No files found in version data")
            return None
        
        # Look for .safetensors model file first
        safetensors_file = None
        other_model_file = None
        
        for file in files:
            if file.get('type') == 'Model':
                if file['name'].endswith('.safetensors'):
                    safetensors_file = file
                    break
                elif not other_model_file:  # Keep first model file as fallback
                    other_model_file = file
        
        # Choose which file to download
        target_file = safetensors_file or other_model_file
        
        if not target_file:
            logger.warning("No model file found")
            return None
        
        file_url = target_file['downloadUrl']
        filename = target_file['name']
        download_path = target_dir / filename
        
        logger.info(f"Downloading model file: {filename}")
        
        if self.file_downloader.download_file(file_url, download_path):
            return filename
        else:
            logger.error(f"Failed to download model file: {filename}")
            return None