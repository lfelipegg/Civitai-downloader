import logging
from pathlib import Path
from api_client import CivitAIClient
from downloader import ModelDownloader, ImageDownloader
from html_generator import HTMLGenerator
from metadata_manager import MetadataManager
from utils import sanitize_filename, get_base_model_key, determine_target_dir

logger = logging.getLogger(__name__)

class ModelProcessor:
    """
    Main class that orchestrates the model download process
    """
    
    def __init__(self):
        self.api_client = CivitAIClient()
        self.model_downloader = ModelDownloader()
        self.image_downloader = ImageDownloader()
        self.html_generator = HTMLGenerator()
        self.metadata_manager = MetadataManager()
    
    def process_model(self, model_id, version_id=None, original_url=None):
        """
        Process a single model: download files, images, and generate documentation
        
        Args:
            model_id (str): Model ID from CivitAI
            version_id (str, optional): Specific version ID
            original_url (str, optional): Original URL for reference
            
        Returns:
            dict: Processing result with success status and details
        """
        logger.info(f"Starting to process model {model_id} (version: {version_id})")
        
        try:
            # Fetch model and version information
            model, version = self.api_client.fetch_model_info(model_id, version_id)
            if not model or not version:
                return {
                    "success": False,
                    "error": "Failed to fetch model information from API",
                    "model_id": model_id,
                    "version_id": version_id
                }
            
            # Prepare file paths and directories
            raw_name = model.get("name", f"Model_{model_id}")
            clean_name = sanitize_filename(raw_name)
            base_name = f"{clean_name}_{model_id}_{version['id']}"
            
            model_type = model.get("type", "Unknown")
            base_model_key = get_base_model_key(version)
            target_dir = determine_target_dir(model_type, base_model_key, base_name)
            
            logger.info(f"Processing: {raw_name}")
            logger.info(f"Model type: {model_type}, Base model: {base_model_key}")
            logger.info(f"Target directory: {target_dir}")
            
            downloaded_files = {}
            
            # Download main model file
            logger.info("Downloading model file...")
            model_filename = self.model_downloader.download_model_file(version, target_dir)
            if model_filename:
                downloaded_files["model_file"] = model_filename
                logger.info(f"Successfully downloaded model file: {model_filename}")
            else:
                logger.warning("Failed to download model file")
            
            # Download preview images
            logger.info("Downloading preview images...")
            downloaded_images = self.image_downloader.download_images(version, target_dir)
            if downloaded_images:
                downloaded_files["images"] = [img.name for img in downloaded_images]
                logger.info(f"Successfully downloaded {len(downloaded_images)} images")
            else:
                logger.info("No images downloaded")
            
            # Generate HTML documentation
            logger.info("Generating HTML documentation...")
            html_content = self.html_generator.generate_model_html(
                model, version, target_dir, downloaded_images, original_url
            )
            html_path = self.metadata_manager.save_html_info(html_content, target_dir, base_name)
            if html_path:
                downloaded_files["html_info"] = html_path.name
            
            # Save metadata
            logger.info("Saving metadata...")
            metadata_path = self.metadata_manager.save_metadata(
                model, version, target_dir, base_name, original_url, downloaded_files
            )
            if metadata_path:
                downloaded_files["metadata"] = metadata_path.name
            
            logger.info(f"Successfully processed model: {raw_name}")
            
            return {
                "success": True,
                "model_name": raw_name,
                "model_id": model_id,
                "version_id": version['id'],
                "target_directory": str(target_dir),
                "downloaded_files": downloaded_files,
                "base_name": base_name
            }
            
        except Exception as e:
            logger.error(f"Unexpected error processing model {model_id}: {e}")
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "model_id": model_id,
                "version_id": version_id
            }
    
    def process_multiple_models(self, model_list):
        """
        Process multiple models from a list of URLs or (model_id, version_id) tuples
        
        Args:
            model_list (list): List of URLs or (model_id, version_id) tuples
            
        Returns:
            list: List of processing results
        """
        results = []
        
        for item in model_list:
            if isinstance(item, str):
                # It's a URL, parse it
                from utils import parse_model_url
                model_id, version_id = parse_model_url(item)
                original_url = item
            elif isinstance(item, (tuple, list)) and len(item) >= 2:
                # It's a (model_id, version_id) tuple
                model_id, version_id = item[0], item[1]
                original_url = None
            else:
                logger.warning(f"Invalid item format: {item}")
                results.append({
                    "success": False,
                    "error": "Invalid item format",
                    "item": str(item)
                })
                continue
            
            if not model_id:
                logger.warning(f"Could not extract model ID from: {item}")
                results.append({
                    "success": False,
                    "error": "Could not extract model ID",
                    "item": str(item)
                })
                continue
            
            result = self.process_model(model_id, version_id, original_url)
            results.append(result)
        
        return results
    
    def get_processing_summary(self, results):
        """
        Generate a summary of processing results
        
        Args:
            results (list): List of processing results
            
        Returns:
            dict: Summary statistics
        """
        successful = [r for r in results if r.get("success", False)]
        failed = [r for r in results if not r.get("success", False)]
        
        summary = {
            "total_processed": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "success_rate": len(successful) / len(results) * 100 if results else 0,
            "successful_models": [r.get("model_name", "Unknown") for r in successful],
            "failed_items": [{"item": r.get("model_id", "Unknown"), "error": r.get("error", "Unknown")} for r in failed]
        }
        
        return summary
    
    def cleanup(self):
        """
        Cleanup resources
        """
        self.api_client.close()
        logger.info("Cleaned up resources")