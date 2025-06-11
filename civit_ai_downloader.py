import requests
import logging
import json
import os
import re
from pathlib import Path
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()


# === CONFIGURATION ===
API_KEY = os.getenv("CIVITAI_API_KEY")
BASE_MODEL_DIR = Path(r"N:/Models")
HEADERS = {"Authorization": f"Bearer {API_KEY}" if API_KEY else ""}

# Enhanced model type directory mapping with specific variants
MODEL_TYPE_DIRS = {
    # FLUX variants
    ("checkpoint", "flux_s"): "FLUX/FLUX.1-S/Checkpoint",
    ("checkpoint merge", "flux_s"): "FLUX/FLUX.1-S/Checkpoint",
    ("lora", "flux_s"): "FLUX/FLUX.1-S/Lora",
    ("textualinversion", "flux_s"): "FLUX/FLUX.1-S/Embeddings",
    ("controlnet", "flux_s"): "FLUX/FLUX.1-S/ControlNet",
    
    ("checkpoint", "flux_d"): "FLUX/FLUX.1-D/Checkpoint",
    ("checkpoint merge", "flux_d"): "FLUX/FLUX.1-D/Checkpoint",
    ("lora", "flux_d"): "FLUX/FLUX.1-D/Lora",
    ("textualinversion", "flux_d"): "FLUX/FLUX.1-D/Embeddings",
    ("controlnet", "flux_d"): "FLUX/FLUX.1-D/ControlNet",
    
    # Generic FLUX (fallback)
    ("checkpoint", "flux"): "FLUX/General/Checkpoint",
    ("checkpoint merge", "flux"): "FLUX/General/Checkpoint",
    ("lora", "flux"): "FLUX/General/Lora",
    ("textualinversion", "flux"): "FLUX/General/Embeddings",
    ("controlnet", "flux"): "FLUX/General/ControlNet",
    
    # Hunyuan variants
    ("checkpoint", "hunyuan"): "Hunyuan/Hunyuan-1/Checkpoint",
    ("checkpoint merge", "hunyuan"): "Hunyuan/Hunyuan-1/Checkpoint",
    ("lora", "hunyuan"): "Hunyuan/Hunyuan-1/Lora",
    ("textualinversion", "hunyuan"): "Hunyuan/Hunyuan-1/Embeddings",
    ("controlnet", "hunyuan"): "Hunyuan/Hunyuan-1/ControlNet",
    
    ("checkpoint", "hunyuan_video"): "Hunyuan/Hunyuan-Video/Checkpoint",
    ("checkpoint merge", "hunyuan_video"): "Hunyuan/Hunyuan-Video/Checkpoint",
    ("lora", "hunyuan_video"): "Hunyuan/Hunyuan-Video/Lora",
    
    # Lumina
    ("checkpoint", "lumina"): "Lumina/Checkpoint",
    ("checkpoint merge", "lumina"): "Lumina/Checkpoint",
    ("lora", "lumina"): "Lumina/Lora",
    ("textualinversion", "lumina"): "Lumina/Embeddings",
    ("controlnet", "lumina"): "Lumina/ControlNet",
    
    # Kolors
    ("checkpoint", "kolors"): "Kolors/Checkpoint",
    ("checkpoint merge", "kolors"): "Kolors/Checkpoint",
    ("lora", "kolors"): "Kolors/Lora",
    ("textualinversion", "kolors"): "Kolors/Embeddings",
    ("controlnet", "kolors"): "Kolors/ControlNet",
    
    # Mochi
    ("checkpoint", "mochi"): "Mochi/Checkpoint",
    ("checkpoint merge", "mochi"): "Mochi/Checkpoint",
    ("lora", "mochi"): "Mochi/Lora",
    
    # LTX-Video
    ("checkpoint", "ltxv"): "LTX-Video/Checkpoint",
    ("checkpoint merge", "ltxv"): "LTX-Video/Checkpoint",
    ("lora", "ltxv"): "LTX-Video/Lora",
    
    # CogVideoX
    ("checkpoint", "cogvideox"): "CogVideoX/Checkpoint",
    ("checkpoint merge", "cogvideox"): "CogVideoX/Checkpoint",
    ("lora", "cogvideox"): "CogVideoX/Lora",
    
    # NoobAI
    ("checkpoint", "noobai"): "NoobAI/Checkpoint",
    ("checkpoint merge", "noobai"): "NoobAI/Checkpoint",
    ("lora", "noobai"): "NoobAI/Lora",
    ("textualinversion", "noobai"): "NoobAI/Embeddings",
    ("controlnet", "noobai"): "NoobAI/ControlNet",
    
    # Wan Video variants
    ("checkpoint", "wan_video_1_3b_t2v"): "Wan-Video/1.3B-T2V/Checkpoint",
    ("checkpoint merge", "wan_video_1_3b_t2v"): "Wan-Video/1.3B-T2V/Checkpoint",
    ("lora", "wan_video_1_3b_t2v"): "Wan-Video/1.3B-T2V/Lora",
    
    ("checkpoint", "wan_video_14b_t2v"): "Wan-Video/14B-T2V/Checkpoint",
    ("checkpoint merge", "wan_video_14b_t2v"): "Wan-Video/14B-T2V/Checkpoint",
    ("lora", "wan_video_14b_t2v"): "Wan-Video/14B-T2V/Lora",
    
    ("checkpoint", "wan_video_14b_i2v_480p"): "Wan-Video/14B-I2V-480p/Checkpoint",
    ("checkpoint merge", "wan_video_14b_i2v_480p"): "Wan-Video/14B-I2V-480p/Checkpoint",
    ("lora", "wan_video_14b_i2v_480p"): "Wan-Video/14B-I2V-480p/Lora",
    
    ("checkpoint", "wan_video_14b_i2v_720p"): "Wan-Video/14B-I2V-720p/Checkpoint",
    ("checkpoint merge", "wan_video_14b_i2v_720p"): "Wan-Video/14B-I2V-720p/Checkpoint",
    ("lora", "wan_video_14b_i2v_720p"): "Wan-Video/14B-I2V-720p/Lora",
    
    # SDXL models
    ("checkpoint", "sdxl"): "SDXL/Checkpoint",
    ("checkpoint merge", "sdxl"): "SDXL/Checkpoint",
    ("lora", "sdxl"): "SDXL/Lora",
    ("textualinversion", "sdxl"): "SDXL/Embeddings",
    ("hypernetwork", "sdxl"): "SDXL/Hypernetworks",
    ("controlnet", "sdxl"): "SDXL/ControlNet",
    
    # SDXL Illustrious (special case)
    ("checkpoint", "illustrious"): "SDXL/Illustrious/Checkpoint",
    ("checkpoint merge", "illustrious"): "SDXL/Illustrious/Checkpoint",
    ("lora", "illustrious"): "SDXL/Illustrious/Lora",
    ("textualinversion", "illustrious"): "SDXL/Illustrious/Embeddings",
    ("controlnet", "illustrious"): "SDXL/Illustrious/ControlNet",
    
    # SD 1.5 models
    ("checkpoint", "sd15"): "SD15/Checkpoint",
    ("checkpoint merge", "sd15"): "SD15/Checkpoint",
    ("lora", "sd15"): "SD15/Lora",
    ("textualinversion", "sd15"): "SD15/Embeddings",
    ("hypernetwork", "sd15"): "SD15/Hypernetworks",
    ("controlnet", "sd15"): "SD15/ControlNet",
    
    # Pony models
    ("checkpoint", "pony"): "SDXL/Pony/Checkpoint",
    ("checkpoint merge", "pony"): "SDXL/Pony/Checkpoint",
    ("lora", "pony"): "SDXL/Pony/Lora",
    
    # Default fallbacks
    ("checkpoint", "unknown"): "Other/Checkpoint",
    ("checkpoint merge", "unknown"): "Other/Checkpoint",
    ("lora", "unknown"): "Other/Lora",
    ("textualinversion", "unknown"): "Other/Embeddings",
    ("hypernetwork", "unknown"): "Other/Hypernetworks",
    ("controlnet", "unknown"): "Other/ControlNet",
}

# List of URLs to process
URLS = ["https://civitai.com/models/1668954/minimal-mix-or-illustrious-or-mexes?modelVersionId=1889067","https://civitai.com/models/1668786/impellitterispell?modelVersionId=1888875","https://civitai.com/models/1611971/mklan-pony?modelVersionId=1888440"]

# === LOGGING SETUP ===
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# === UTILITIES ===
def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*\n\r\t]', '', name).strip().replace(' ', '_')

def download_file(url, path, headers=None):
    try:
        with requests.get(url, stream=True, headers=headers) as r:
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))
            with open(path, 'wb') as f, tqdm(
                desc=path.name,
                total=total,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    bar.update(len(chunk))
        return True
    except Exception as e:
        logger.error(f"Failed to download file from {url}: {e}")
        return False

def fetch_model_info(model_id, version_id=None):
    try:
        model_url = f"https://civitai.com/api/v1/models/{model_id}"
        model = requests.get(model_url, headers=HEADERS).json()

        if not version_id:
            version_id = model.get('modelVersions', [{}])[0].get('id')
        version_url = f"https://civitai.com/api/v1/model-versions/{version_id}"
        version = requests.get(version_url, headers=HEADERS).json()

        return model, version
    except Exception as e:
        logger.error(f"Error fetching model {model_id} (version {version_id}): {e}")
        return None, None

def detect_model_base(model, version):
    """
    Detect the base model type with specific variants from model information
    """
    # Check model name and tags for keywords
    model_name = model.get("name", "").lower()
    
    # Handle tags that can be either strings or objects
    model_tags = []
    for tag in model.get("tags", []):
        if isinstance(tag, str):
            model_tags.append(tag.lower())
        elif isinstance(tag, dict):
            model_tags.append(tag.get("name", "").lower())
    
    version_name = version.get("name", "").lower()
    description = model.get("description", "").lower()
    
    # Combine all text sources for analysis
    all_text = f"{model_name} {version_name} {description} {' '.join(model_tags)}"
    
    # Check for FLUX variants (more specific first)
    if any(keyword in all_text for keyword in ["flux.1-s", "flux 1 s", "flux1s", "flux.1 s"]):
        return "flux_s"
    elif any(keyword in all_text for keyword in ["flux.1-dev", "flux.1-d", "flux 1 dev", "flux 1 d", "flux1d", "flux.1 dev", "flux.1 d"]):
        return "flux_d"
    elif any(keyword in all_text for keyword in ["flux", "flux.1", "flux1"]):
        return "flux"
    
    # Check for Hunyuan variants
    if any(keyword in all_text for keyword in ["hunyuan video", "hunyuan-video", "hunyuanvideo"]):
        return "hunyuan_video"
    elif any(keyword in all_text for keyword in ["hunyuan", "hunyuan-1", "hunyuan 1"]):
        return "hunyuan"
    
    # Check for Wan Video variants (most specific first)
    if any(keyword in all_text for keyword in ["wan video 14b i2v 720p", "wan-video-14b-i2v-720p", "wanvideo14bi2v720p"]):
        return "wan_video_14b_i2v_720p"
    elif any(keyword in all_text for keyword in ["wan video 14b i2v 480p", "wan-video-14b-i2v-480p", "wanvideo14bi2v480p"]):
        return "wan_video_14b_i2v_480p"
    elif any(keyword in all_text for keyword in ["wan video 14b t2v", "wan-video-14b-t2v", "wanvideo14bt2v"]):
        return "wan_video_14b_t2v"
    elif any(keyword in all_text for keyword in ["wan video 1.3b t2v", "wan-video-1.3b-t2v", "wanvideo1.3bt2v", "wan video 1_3b t2v"]):
        return "wan_video_1_3b_t2v"
    
    # Check for other new models
    if any(keyword in all_text for keyword in ["lumina", "lumina-t2x"]):
        return "lumina"
    
    if any(keyword in all_text for keyword in ["kolors", "kwai-kolors"]):
        return "kolors"
    
    if any(keyword in all_text for keyword in ["mochi", "mochi-1"]):
        return "mochi"
    
    if any(keyword in all_text for keyword in ["ltx-video", "ltxv", "ltx video", "lightricks"]):
        return "ltxv"
    
    if any(keyword in all_text for keyword in ["cogvideox", "cog-videox", "cog videox"]):
        return "cogvideox"
    
    if any(keyword in all_text for keyword in ["noobai", "noob-ai", "noob ai"]):
        return "noobai"
    
    # Check for Illustrious (specific SDXL variant)
    if any(keyword in all_text for keyword in ["illustrious", "illust"]):
        return "illustrious"
    
    # Check for Pony (specific SDXL variant)
    if any(keyword in all_text for keyword in ["pony", "ponyxl", "pony diffusion"]):
        return "pony"
    
    # Check for SDXL
    if any(keyword in all_text for keyword in ["sdxl", "xl", "stable diffusion xl"]):
        return "sdxl"
    
    # Check for SD 1.5
    if any(keyword in all_text for keyword in ["sd15", "sd 1.5", "stable diffusion 1.5", "v1-5"]):
        return "sd15"
    
    # Check base model from version info if available
    base_model = version.get("baseModel", "").lower()
    if base_model:
        # Check for specific variants first
        if "flux" in base_model:
            if "dev" in base_model or "1-d" in base_model:
                return "flux_d"
            elif "schnell" in base_model or "1-s" in base_model:
                return "flux_s"
            else:
                return "flux"
        elif "hunyuan" in base_model:
            if "video" in base_model:
                return "hunyuan_video"
            else:
                return "hunyuan"
        elif "sdxl" in base_model or "xl" in base_model:
            if "illustrious" in all_text:
                return "illustrious"
            elif "pony" in all_text:
                return "pony"
            else:
                return "sdxl"
        elif "sd 1.5" in base_model or "v1-5" in base_model:
            return "sd15"
        elif "lumina" in base_model:
            return "lumina"
        elif "kolors" in base_model:
            return "kolors"
        elif "mochi" in base_model:
            return "mochi"
        elif "ltx" in base_model:
            return "ltxv"
        elif "cog" in base_model and "video" in base_model:
            return "cogvideox"
        elif "noob" in base_model:
            return "noobai"
    
    logger.warning(f"Could not detect base model for {model_name}, using 'unknown'")
    return "unknown"

def determine_target_dir(model_type, model_base, base_name):
    """
    Determine target directory based on model type and detected base model
    """
    model_type_lower = model_type.lower()
    
    # Try to find exact match
    dir_key = (model_type_lower, model_base)
    if dir_key in MODEL_TYPE_DIRS:
        subdir = MODEL_TYPE_DIRS[dir_key]
    else:
        # Fallback to unknown base
        fallback_key = (model_type_lower, "unknown")
        subdir = MODEL_TYPE_DIRS.get(fallback_key, "Other/Unknown")
    
    target_dir = BASE_MODEL_DIR / subdir / base_name
    target_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Target directory: {target_dir}")
    return target_dir

def download_images(version, target_dir, max_images=3):
    """
    Download up to max_images preview images from the model version
    Returns list of downloaded image paths
    """
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
                continue
            
            # Determine file extension from URL or default to jpg
            image_ext = ".jpg"
            if image_url.lower().endswith(('.png', '.jpeg', '.jpg', '.webp')):
                image_ext = os.path.splitext(image_url.lower())[1]
            
            # Create filename
            image_filename = f"preview_{i+1:02d}{image_ext}"
            image_path = target_dir / image_filename
            
            logger.info(f"Downloading image {i+1}: {image_filename}")
            if download_file(image_url, image_path):
                downloaded_count += 1
                downloaded_images.append(image_path)
            
        except Exception as e:
            logger.error(f"Failed to download image {i+1}: {e}")
    
    logger.info(f"Downloaded {downloaded_count} images")
    return downloaded_images

def generate_model_html(model, version, target_dir, downloaded_images):
    """
    Generate a complete HTML page for the downloaded model
    """
    model_name = model.get('name', 'Unnamed Model')
    model_description = model.get('description', 'No description available')
    model_type = model.get('type', 'Unknown')
    
    # Handle tags that can be either strings or objects
    model_tags = []
    for tag in model.get('tags', []):
        if isinstance(tag, str):
            model_tags.append(tag)
        elif isinstance(tag, dict):
            model_tags.append(tag.get('name', ''))
    
    # Version info
    version_name = version.get('name', 'Unknown Version')
    version_description = version.get('description', '')
    base_model = version.get('baseModel', 'Unknown')
    trained_words = version.get('trainedWords', [])
    
    # Create image gallery HTML
    image_gallery = ""
    if downloaded_images:
        image_gallery = "<div class='image-gallery'>\n"
        for img_path in downloaded_images:
            image_gallery += f"        <img src='{img_path.name}' alt='Preview Image' onclick='openModal(this.src)'>\n"
        image_gallery += "    </div>\n"
    
    # Create tags HTML
    tags_html = ""
    if model_tags:
        tags_html = "<div class='tags'>\n"
        for tag in model_tags:
            tags_html += f"        <span class='tag'>{tag}</span>\n"
        tags_html += "    </div>\n"
    
    # Create trained words HTML
    trained_words_html = ""
    if trained_words:
        trained_words_html = "<div class='trained-words'>\n"
        trained_words_html += "        <h3>Trained Words/Triggers:</h3>\n"
        trained_words_html += "        <div class='word-list'>\n"
        for word in trained_words:
            trained_words_html += f"            <code>{word}</code>\n"
        trained_words_html += "        </div>\n"
        trained_words_html += "    </div>\n"
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{model_name}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        
        .model-info {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        
        .info-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .info-card h3 {{
            margin-top: 0;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .description {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #3498db;
        }}
        
        .image-gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .image-gallery img {{
            width: 100%;
            height: 300px;
            object-fit: cover;
            border-radius: 10px;
            cursor: pointer;
            transition: transform 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        
        .image-gallery img:hover {{
            transform: scale(1.05);
        }}
        
        .tags {{
            margin: 20px 0;
        }}
        
        .tag {{
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 5px 12px;
            margin: 3px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        
        .trained-words {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }}
        
        .word-list code {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 4px 8px;
            border-radius: 4px;
            margin: 2px;
            display: inline-block;
            font-family: 'Courier New', monospace;
        }}
        
        .modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.9);
        }}
        
        .modal-content {{
            margin: auto;
            display: block;
            width: 90%;
            max-width: 1000px;
            max-height: 90%;
            object-fit: contain;
        }}
        
        .close {{
            position: absolute;
            top: 15px;
            right: 35px;
            color: #f1f1f1;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
        }}
        
        .close:hover {{
            color: #bbb;
        }}
        
        @media (max-width: 768px) {{
            .model-info {{
                grid-template-columns: 1fr;
            }}
            
            .image-gallery {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{model_name}</h1>
            <p>Version: {version_name}</p>
        </div>
        
        <div class="model-info">
            <div class="info-card">
                <h3>Model Information</h3>
                <p><strong>Type:</strong> {model_type}</p>
                <p><strong>Base Model:</strong> {base_model}</p>
            </div>
            
            <div class="info-card">
                <h3>Version Details</h3>
                <p><strong>Version Name:</strong> {version_name}</p>
                {f'<p><strong>Version Description:</strong> {version_description}</p>' if version_description else ''}
            </div>
        </div>
        
        <div class="content">
            {f'<div class="description"><h3>Description</h3><p>{model_description}</p></div>' if model_description != 'No description available' else ''}
            
            {trained_words_html}
            
            {f'<h3>Tags</h3>{tags_html}' if tags_html else ''}
            
            {f'<h3>Preview Images</h3>{image_gallery}' if image_gallery else '<p>No preview images available</p>'}
        </div>
    </div>
    
    <!-- Modal for image viewing -->
    <div id="imageModal" class="modal">
        <span class="close">&times;</span>
        <img class="modal-content" id="modalImage">
    </div>
    
    <script>
        function openModal(src) {{
            document.getElementById('imageModal').style.display = 'block';
            document.getElementById('modalImage').src = src;
        }}
        
        document.querySelector('.close').onclick = function() {{
            document.getElementById('imageModal').style.display = 'none';
        }}
        
        window.onclick = function(event) {{
            if (event.target == document.getElementById('imageModal')) {{
                document.getElementById('imageModal').style.display = 'none';
            }}
        }}
    </script>
</body>
</html>"""
    
    return html_content

def download_model(model_id, model, version):
    raw_name = model.get("name", f"Model_{model_id}")
    clean_name = sanitize_filename(raw_name)
    base_name = f"{clean_name}_{model_id}_{version['id']}"

    model_type = model.get("type", "Unknown")
    model_base = detect_model_base(model, version)
    target_dir = determine_target_dir(model_type, model_base, base_name)

    logger.info(f"Processing: {raw_name}")
    logger.info(f"Detected model type: {model_type}, base: {model_base}")

    # Download model file
    safetensors_file = ""
    for file in version.get("files", []):
        if file['type'] == 'Model' and file['name'].endswith('.safetensors'):
            file_url = file['downloadUrl']
            safetensors_file = file['name']
            download_path = target_dir / safetensors_file
            logger.info(f"Downloading model: {safetensors_file}")
            download_file(file_url, download_path, headers=HEADERS)
            break
    else:
        logger.warning(f"No .safetensors model file found for {base_name}")

    # Download preview images and get paths
    downloaded_images = download_images(version, target_dir, max_images=3)

    # Save metadata
    metadata_path = target_dir / f"{base_name}_metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump({"model": model, "version": version}, f, ensure_ascii=False, indent=2)

    # Generate and save HTML page for this model
    html_content = generate_model_html(model, version, target_dir, downloaded_images)
    html_path = target_dir / f"{base_name}_info.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    logger.info(f"Generated HTML page: {html_path}")

def parse_model_url(url):
    match = re.search(r'models/(\d+)(?:\?modelVersionId=(\d+))?', url)
    return match.groups() if match else (None, None)

def main():
    for url in URLS:
        model_id, version_id = parse_model_url(url)
        if model_id:
            model, version = fetch_model_info(model_id, version_id)
            if model and version:
                download_model(model_id, model, version)
        else:
            logger.warning(f"Invalid URL format: {url}")

    logger.info("All models processed successfully!")

if __name__ == "__main__":
    main()