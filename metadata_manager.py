import json
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class MetadataManager:
    """
    Manages metadata for downloaded models
    """
    
    def __init__(self):
        self.metadata_filename = "_metadata.json"
        self.info_filename = "_info.html"
    
    def save_metadata(self, model, version, target_dir, base_name, original_url=None, downloaded_files=None):
        """
        Save model metadata to JSON file
        
        Args:
            model (dict): Model data from API
            version (dict): Version data from API
            target_dir (Path): Directory where model is saved
            base_name (str): Base name for files
            original_url (str, optional): Original CivitAI URL
            downloaded_files (dict, optional): Info about downloaded files
            
        Returns:
            Path: Path to saved metadata file
        """
        try:
            metadata = {
                "download_info": {
                    "downloaded_at": datetime.now().isoformat(),
                    "original_url": original_url,
                    "base_name": base_name,
                    "downloaded_files": downloaded_files or {}
                },
                "model": model,
                "version": version
            }
            
            metadata_path = target_dir / f"{base_name}{self.metadata_filename}"
            
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved metadata to: {metadata_path}")
            return metadata_path
            
        except Exception as e:
            logger.error(f"Failed to save metadata: {e}")
            return None
    
    def load_metadata(self, metadata_path):
        """
        Load metadata from JSON file
        
        Args:
            metadata_path (Path): Path to metadata file
            
        Returns:
            dict: Loaded metadata or None if failed
        """
        try:
            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
            
            logger.info(f"Loaded metadata from: {metadata_path}")
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to load metadata from {metadata_path}: {e}")
            return None
    
    def save_html_info(self, html_content, target_dir, base_name):
        """
        Save HTML info page
        
        Args:
            html_content (str): Generated HTML content
            target_dir (Path): Directory to save HTML file
            base_name (str): Base name for the file
            
        Returns:
            Path: Path to saved HTML file
        """
        try:
            html_path = target_dir / f"{base_name}{self.info_filename}"
            
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            logger.info(f"Saved HTML info page to: {html_path}")
            return html_path
            
        except Exception as e:
            logger.error(f"Failed to save HTML info page: {e}")
            return None
    
    def find_existing_downloads(self, base_model_dir):
        """
        Find all existing downloads by scanning for metadata files
        
        Args:
            base_model_dir (Path): Base directory to scan
            
        Returns:
            list: List of metadata file paths
        """
        try:
            metadata_files = list(base_model_dir.rglob(f"*{self.metadata_filename}"))
            logger.info(f"Found {len(metadata_files)} existing downloads")
            return metadata_files
            
        except Exception as e:
            logger.error(f"Failed to scan for existing downloads: {e}")
            return []
    
    def get_download_summary(self, metadata_path):
        """
        Get a summary of a download from its metadata
        
        Args:
            metadata_path (Path): Path to metadata file
            
        Returns:
            dict: Summary information
        """
        metadata = self.load_metadata(metadata_path)
        if not metadata:
            return None
        
        model = metadata.get("model", {})
        version = metadata.get("version", {})
        download_info = metadata.get("download_info", {})
        
        return {
            "model_name": model.get("name", "Unknown"),
            "model_type": model.get("type", "Unknown"),
            "version_name": version.get("name", "Unknown"),
            "base_model": version.get("baseModel", "Unknown"),
            "downloaded_at": download_info.get("downloaded_at", "Unknown"),
            "original_url": download_info.get("original_url"),
            "location": str(metadata_path.parent)
        }