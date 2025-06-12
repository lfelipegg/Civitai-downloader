import requests
import logging
from config import Config

logger = logging.getLogger(__name__)

class CivitAIClient:
    """
    Client for interacting with the CivitAI API
    """
    
    def __init__(self):
        self.base_url = Config.BASE_URL
        self.headers = Config.HEADERS
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def fetch_model_info(self, model_id, version_id=None):
        """
        Fetch model and version information from CivitAI API
        
        Args:
            model_id (str): The model ID
            version_id (str, optional): Specific version ID. If None, uses latest version
            
        Returns:
            tuple: (model_data, version_data) or (None, None) on error
        """
        try:
            # Fetch model information
            model_url = f"{self.base_url}/models/{model_id}"
            logger.info(f"Fetching model info from: {model_url}")
            
            model_response = self.session.get(model_url)
            model_response.raise_for_status()
            model = model_response.json()
            
            # If no specific version requested, use the latest (first in list)
            if not version_id:
                model_versions = model.get('modelVersions', [])
                if not model_versions:
                    logger.error(f"No versions found for model {model_id}")
                    return None, None
                version_id = model_versions[0].get('id')
                logger.info(f"Using latest version: {version_id}")
            
            # Fetch version information
            version_url = f"{self.base_url}/model-versions/{version_id}"
            logger.info(f"Fetching version info from: {version_url}")
            
            version_response = self.session.get(version_url)
            version_response.raise_for_status()
            version = version_response.json()
            
            return model, version
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for model {model_id} (version {version_id}): {e}")
            return None, None
        except Exception as e:
            logger.error(f"Unexpected error fetching model {model_id} (version {version_id}): {e}")
            return None, None
    
    def get_download_url(self, file_info):
        """
        Get the download URL for a file
        
        Args:
            file_info (dict): File information from API
            
        Returns:
            str: Download URL or None if not available
        """
        return file_info.get('downloadUrl')
    
    def close(self):
        """
        Close the session
        """
        self.session.close()