import threading
import queue
import time
from datetime import datetime
from model_processor import ModelProcessor
from utils import parse_model_url

class GUIDownloadManager:
    """
    Manages downloads with GUI feedback and threading
    """
    
    def __init__(self, progress_callback=None, log_callback=None, status_callback=None):
        self.progress_callback = progress_callback
        self.log_callback = log_callback
        self.status_callback = status_callback
        
        self.processor = None
        self.download_thread = None
        self.is_downloading = False
        self.should_stop = False
        
        # Queue for thread-safe communication
        self.message_queue = queue.Queue()
        
        # Download statistics
        self.stats = {
            "total": 0,
            "completed": 0,
            "failed": 0,
            "current_model": "",
            "start_time": None
        }
    
    def start_download(self, urls):
        """
        Start downloading models from URL list
        
        Args:
            urls (list): List of CivitAI URLs to download
        """
        if self.is_downloading:
            self._log("Download already in progress", "WARNING")
            return False
        
        if not urls:
            self._log("No URLs provided for download", "WARNING")
            return False
        
        # Reset state
        self.is_downloading = True
        self.should_stop = False
        self.stats = {
            "total": len(urls),
            "completed": 0,
            "failed": 0,
            "current_model": "",
            "start_time": datetime.now()
        }
        
        # Start download thread
        self.download_thread = threading.Thread(
            target=self._download_worker,
            args=(urls,),
            daemon=True
        )
        self.download_thread.start()
        
        self._log(f"Started downloading {len(urls)} models", "INFO")
        return True
    
    def stop_download(self):
        """Stop the current download process"""
        if not self.is_downloading:
            return
        
        self.should_stop = True
        self._log("Stopping download...", "WARNING")
        
        # Wait for thread to finish
        if self.download_thread and self.download_thread.is_alive():
            self.download_thread.join(timeout=5.0)
        
        self.is_downloading = False
        self._update_status("Download stopped")
        self._log("Download stopped by user", "WARNING")
    
    def _download_worker(self, urls):
        """
        Worker function that runs in a separate thread
        """
        try:
            self.processor = ModelProcessor()
            
            for i, url in enumerate(urls):
                if self.should_stop:
                    break
                
                # Parse URL
                model_id, version_id = parse_model_url(url)
                if not model_id:
                    self._log(f"Invalid URL format: {url}", "ERROR")
                    self.stats["failed"] += 1
                    continue
                
                # Update current model
                self.stats["current_model"] = f"Model {model_id}"
                overall_progress = (i / self.stats["total"]) * 100
                self._update_progress(
                    overall_progress,
                    f"Processing {i+1}/{self.stats['total']}: Model {model_id}"
                )
                
                self._log(f"Starting download: Model {model_id}", "INFO")
                
                # Process model with callbacks
                result = self._process_model_with_feedback(model_id, version_id, url)
                
                if result.get("success", False):
                    self.stats["completed"] += 1
                    self._log(f"✓ Successfully downloaded: {result.get('model_name', 'Unknown')}", "SUCCESS")
                else:
                    self.stats["failed"] += 1
                    error = result.get("error", "Unknown error")
                    self._log(f"✗ Failed to download Model {model_id}: {error}", "ERROR")
                
                # Small delay between downloads
                if not self.should_stop:
                    time.sleep(0.5)
            
            # Finalize
            self._finalize_download()
            
        except Exception as e:
            self._log(f"Unexpected error in download worker: {e}", "ERROR")
        finally:
            if self.processor:
                self.processor.cleanup()
            self.is_downloading = False
    
    def _process_model_with_feedback(self, model_id, version_id, original_url):
        """
        Process a single model with GUI feedback
        """
        try:
            # Fetch model info
            self._update_model_status("Fetching model information...")
            model, version = self.processor.api_client.fetch_model_info(model_id, version_id)
            
            if not model or not version:
                return {"success": False, "error": "Failed to fetch model information"}
            
            model_name = model.get("name", f"Model_{model_id}")
            self.stats["current_model"] = model_name
            
            # Setup directories
            self._update_model_status("Preparing directories...")
            from utils import sanitize_filename, get_base_model_key, determine_target_dir
            
            clean_name = sanitize_filename(model_name)
            base_name = f"{clean_name}_{model_id}_{version['id']}"
            model_type = model.get("type", "Unknown")
            base_model_key = get_base_model_key(version)
            target_dir = determine_target_dir(model_type, base_model_key, base_name)
            
            downloaded_files = {}
            
            # Download model file
            self._update_model_status("Downloading model file...")
            model_filename = self.processor.model_downloader.download_model_file(version, target_dir)
            if model_filename:
                downloaded_files["model_file"] = model_filename
            
            # Download images
            self._update_model_status("Downloading preview images...")
            downloaded_images = self.processor.image_downloader.download_images(version, target_dir)
            if downloaded_images:
                downloaded_files["images"] = [img.name for img in downloaded_images]
            
            # Generate documentation
            self._update_model_status("Generating documentation...")
            html_content = self.processor.html_generator.generate_model_html(
                model, version, target_dir, downloaded_images, original_url
            )
            html_path = self.processor.metadata_manager.save_html_info(html_content, target_dir, base_name)
            if html_path:
                downloaded_files["html_info"] = html_path.name
            
            # Save metadata
            self._update_model_status("Saving metadata...")
            metadata_path = self.processor.metadata_manager.save_metadata(
                model, version, target_dir, base_name, original_url, downloaded_files
            )
            if metadata_path:
                downloaded_files["metadata"] = metadata_path.name
            
            return {
                "success": True,
                "model_name": model_name,
                "model_id": model_id,
                "version_id": version['id'],
                "target_directory": str(target_dir),
                "downloaded_files": downloaded_files
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _finalize_download(self):
        """Finalize the download process and show summary"""
        if self.should_stop:
            self._update_status("Download stopped")
        else:
            self._update_progress(100, "Download complete!")
            
        # Calculate duration
        duration = datetime.now() - self.stats["start_time"]
        duration_str = str(duration).split('.')[0]  # Remove microseconds
        
        # Show summary
        summary = (
            f"Download Summary:\n"
            f"Total: {self.stats['total']}, "
            f"Completed: {self.stats['completed']}, "
            f"Failed: {self.stats['failed']}\n"
            f"Duration: {duration_str}"
        )
        
        self._log(summary, "INFO")
        self._update_status(f"Completed: {self.stats['completed']}/{self.stats['total']} models")
    
    def _update_progress(self, percentage, status=""):
        """Update progress bar"""
        if self.progress_callback:
            self.progress_callback(percentage, status)
    
    def _update_status(self, status):
        """Update status display"""
        if self.status_callback:
            self.status_callback(status)
    
    def _update_model_status(self, status):
        """Update current model status"""
        full_status = f"{self.stats['current_model']}: {status}"
        self._update_status(full_status)
    
    def _log(self, message, level="INFO"):
        """Add log message"""
        if self.log_callback:
            self.log_callback(message, level)
    
    def get_stats(self):
        """Get current download statistics"""
        return self.stats.copy()
    
    def is_busy(self):
        """Check if download is in progress"""
        return self.is_downloading