import re
import logging
from pathlib import Path
from config import Config

logger = logging.getLogger(__name__)

def sanitize_filename(name):
    """
    Sanitize filename by removing invalid characters and replacing spaces with underscores
    """
    return re.sub(r'[<>:"/\\|?*\n\r\t]', '', name).strip().replace(' ', '_')

def parse_model_url(url):
    """
    Parse CivitAI model URL to extract model_id and version_id
    Returns tuple (model_id, version_id) or (None, None) if invalid
    """
    match = re.search(r'models/(\d+)(?:\?modelVersionId=(\d+))?', url)
    return match.groups() if match else (None, None)

def get_base_model_key(version):
    """
    Extract and normalize the base model from version info
    """
    base_model = version.get("baseModel", "").lower().strip()
    
    if not base_model:
        logger.warning("No baseModel found in version info")
        return "unknown"
    
    # Try exact match first
    if base_model in Config.BASE_MODEL_MAPPINGS:
        return Config.BASE_MODEL_MAPPINGS[base_model]
    
    # Try partial matches for flexibility
    for key, value in Config.BASE_MODEL_MAPPINGS.items():
        if key in base_model or base_model in key:
            logger.info(f"Matched '{base_model}' to '{value}' via partial match")
            return value
    
    logger.warning(f"Unknown base model: '{base_model}', using 'unknown'")
    return "unknown"

def determine_target_dir(model_type, base_model_key, base_name):
    """
    Determine target directory based on model type and base model from API
    """
    model_type_lower = model_type.lower()
    
    # Try to find exact match
    dir_key = (model_type_lower, base_model_key)
    if dir_key in Config.MODEL_TYPE_DIRS:
        subdir = Config.MODEL_TYPE_DIRS[dir_key]
    else:
        # Fallback to unknown base
        fallback_key = (model_type_lower, "unknown")
        subdir = Config.MODEL_TYPE_DIRS.get(fallback_key, "Other/Unknown")
        logger.warning(f"No specific directory mapping for {dir_key}, using fallback: {subdir}")
    
    target_dir = Config.BASE_MODEL_DIR / subdir / base_name
    target_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Target directory: {target_dir}")
    return target_dir

def setup_logging(level=logging.INFO):
    """
    Setup logging configuration
    """
    logging.basicConfig(
        level=level, 
        format="%(asctime)s - %(name)s - %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logging.getLogger(__name__)