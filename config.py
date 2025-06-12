import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the CivitAI downloader"""
    
    # API Configuration
    API_KEY = os.getenv("CIVITAI_API_KEY")
    BASE_URL = "https://civitai.com/api/v1"
    HEADERS = {"Authorization": f"Bearer {API_KEY}" if API_KEY else ""}
    
    # Directory Configuration
    BASE_MODEL_DIR = Path(r"N:/Models")
    
    # Download Configuration
    MAX_PREVIEW_IMAGES = 3
    CHUNK_SIZE = 8192
    
    # Enhanced model type directory mapping based on baseModel field
    MODEL_TYPE_DIRS = {
        # FLUX variants
        ("checkpoint", "flux.1 [dev]"): "FLUX/FLUX.1-Dev/Checkpoint",
        ("checkpoint merge", "flux.1 [dev]"): "FLUX/FLUX.1-Dev/Checkpoint",
        ("lora", "flux.1 [dev]"): "FLUX/FLUX.1-Dev/Lora",
        ("textualinversion", "flux.1 [dev]"): "FLUX/FLUX.1-Dev/Embeddings",
        ("controlnet", "flux.1 [dev]"): "FLUX/FLUX.1-Dev/ControlNet",
        
        ("checkpoint", "flux.1 [schnell]"): "FLUX/FLUX.1-Schnell/Checkpoint",
        ("checkpoint merge", "flux.1 [schnell]"): "FLUX/FLUX.1-Schnell/Checkpoint",
        ("lora", "flux.1 [schnell]"): "FLUX/FLUX.1-Schnell/Lora",
        ("textualinversion", "flux.1 [schnell]"): "FLUX/FLUX.1-Schnell/Embeddings",
        ("controlnet", "flux.1 [schnell]"): "FLUX/FLUX.1-Schnell/ControlNet",
        
        # Generic FLUX (fallback for other flux variants)
        ("checkpoint", "flux"): "FLUX/General/Checkpoint",
        ("checkpoint merge", "flux"): "FLUX/General/Checkpoint",
        ("lora", "flux"): "FLUX/General/Lora",
        ("textualinversion", "flux"): "FLUX/General/Embeddings",
        ("controlnet", "flux"): "FLUX/General/ControlNet",
        
        # Illustrious XL
        ("checkpoint", "illustrious xl v0.1"): "SDXL/Illustrious/Checkpoint",
        ("checkpoint merge", "illustrious xl v0.1"): "SDXL/Illustrious/Checkpoint",
        ("lora", "illustrious xl v0.1"): "SDXL/Illustrious/Lora",
        ("textualinversion", "illustrious xl v0.1"): "SDXL/Illustrious/Embeddings",
        ("controlnet", "illustrious xl v0.1"): "SDXL/Illustrious/ControlNet",
        
        # Pony Diffusion XL
        ("checkpoint", "pony"): "SDXL/Pony/Checkpoint",
        ("checkpoint merge", "pony"): "SDXL/Pony/Checkpoint",
        ("lora", "pony"): "SDXL/Pony/Lora",
        ("textualinversion", "pony"): "SDXL/Pony/Embeddings",
        ("controlnet", "pony"): "SDXL/Pony/ControlNet",
        
        # SDXL 1.0
        ("checkpoint", "sdxl 1.0"): "SDXL/Base/Checkpoint",
        ("checkpoint merge", "sdxl 1.0"): "SDXL/Base/Checkpoint",
        ("lora", "sdxl 1.0"): "SDXL/Base/Lora",
        ("textualinversion", "sdxl 1.0"): "SDXL/Base/Embeddings",
        ("hypernetwork", "sdxl 1.0"): "SDXL/Base/Hypernetworks",
        ("controlnet", "sdxl 1.0"): "SDXL/Base/ControlNet",
        
        # SDXL Turbo
        ("checkpoint", "sdxl turbo"): "SDXL/Turbo/Checkpoint",
        ("checkpoint merge", "sdxl turbo"): "SDXL/Turbo/Checkpoint",
        ("lora", "sdxl turbo"): "SDXL/Turbo/Lora",
        
        # SD 1.5
        ("checkpoint", "sd 1.5"): "SD15/Checkpoint",
        ("checkpoint merge", "sd 1.5"): "SD15/Checkpoint",
        ("lora", "sd 1.5"): "SD15/Lora",
        ("textualinversion", "sd 1.5"): "SD15/Embeddings",
        ("hypernetwork", "sd 1.5"): "SD15/Hypernetworks",
        ("controlnet", "sd 1.5"): "SD15/ControlNet",
        
        # SD 2.1
        ("checkpoint", "sd 2.1"): "SD21/Checkpoint",
        ("checkpoint merge", "sd 2.1"): "SD21/Checkpoint",
        ("lora", "sd 2.1"): "SD21/Lora",
        ("textualinversion", "sd 2.1"): "SD21/Embeddings",
        ("controlnet", "sd 2.1"): "SD21/ControlNet",
        
        # Hunyuan variants
        ("checkpoint", "hunyuan-dit"): "Hunyuan/Hunyuan-DiT/Checkpoint",
        ("checkpoint merge", "hunyuan-dit"): "Hunyuan/Hunyuan-DiT/Checkpoint",
        ("lora", "hunyuan-dit"): "Hunyuan/Hunyuan-DiT/Lora",
        
        ("checkpoint", "hunyuan video"): "Hunyuan/Hunyuan-Video/Checkpoint",
        ("checkpoint merge", "hunyuan video"): "Hunyuan/Hunyuan-Video/Checkpoint",
        ("lora", "hunyuan video"): "Hunyuan/Hunyuan-Video/Lora",
        
        # Kolors
        ("checkpoint", "kolors"): "Kolors/Checkpoint",
        ("checkpoint merge", "kolors"): "Kolors/Checkpoint",
        ("lora", "kolors"): "Kolors/Lora",
        ("textualinversion", "kolors"): "Kolors/Embeddings",
        ("controlnet", "kolors"): "Kolors/ControlNet",
        
        # Lumina
        ("checkpoint", "lumina-t2x"): "Lumina/Checkpoint",
        ("checkpoint merge", "lumina-t2x"): "Lumina/Checkpoint",
        ("lora", "lumina-t2x"): "Lumina/Lora",
        
        # Mochi
        ("checkpoint", "mochi"): "Mochi/Checkpoint",
        ("checkpoint merge", "mochi"): "Mochi/Checkpoint",
        ("lora", "mochi"): "Mochi/Lora",
        
        # LTX-Video
        ("checkpoint", "ltx-video"): "LTX-Video/Checkpoint",
        ("checkpoint merge", "ltx-video"): "LTX-Video/Checkpoint",
        ("lora", "ltx-video"): "LTX-Video/Lora",
        
        # CogVideoX variants
        ("checkpoint", "cogvideox-2b"): "CogVideoX/2B/Checkpoint",
        ("checkpoint merge", "cogvideox-2b"): "CogVideoX/2B/Checkpoint",
        ("lora", "cogvideox-2b"): "CogVideoX/2B/Lora",
        
        ("checkpoint", "cogvideox-5b"): "CogVideoX/5B/Checkpoint",
        ("checkpoint merge", "cogvideox-5b"): "CogVideoX/5B/Checkpoint",
        ("lora", "cogvideox-5b"): "CogVideoX/5B/Lora",
        
        # NoobAI variants
        ("checkpoint", "noobai xl"): "NoobAI/XL/Checkpoint",
        ("checkpoint merge", "noobai xl"): "NoobAI/XL/Checkpoint",
        ("lora", "noobai xl"): "NoobAI/XL/Lora",
        ("textualinversion", "noobai xl"): "NoobAI/XL/Embeddings",
        
        # Default fallbacks for unknown base models
        ("checkpoint", "unknown"): "Other/Checkpoint",
        ("checkpoint merge", "unknown"): "Other/Checkpoint",
        ("lora", "unknown"): "Other/Lora",
        ("textualinversion", "unknown"): "Other/Embeddings",
        ("hypernetwork", "unknown"): "Other/Hypernetworks",
        ("controlnet", "unknown"): "Other/ControlNet",
    }
    
    # Base model name mappings for normalization
    BASE_MODEL_MAPPINGS = {
        # FLUX variants
        "flux.1 [dev]": "flux.1 [dev]",
        "flux.1 [schnell]": "flux.1 [schnell]", 
        "flux1dev": "flux.1 [dev]",
        "flux1schnell": "flux.1 [schnell]",
        "flux dev": "flux.1 [dev]",
        "flux schnell": "flux.1 [schnell]",
        
        # SDXL variants
        "sdxl 1.0": "sdxl 1.0",
        "sdxl": "sdxl 1.0",
        "sdxl turbo": "sdxl turbo",
        "illustrious xl v0.1": "illustrious xl v0.1",
        "illustrious": "illustrious xl v0.1",
        "pony": "pony",
        "pony diffusion xl": "pony",
        
        # SD variants  
        "sd 1.5": "sd 1.5",
        "sd1.5": "sd 1.5",
        "stable diffusion 1.5": "sd 1.5",
        "sd 2.1": "sd 2.1",
        "sd2.1": "sd 2.1",
        
        # Other models
        "hunyuan-dit": "hunyuan-dit",
        "hunyuan video": "hunyuan video",
        "kolors": "kolors",
        "lumina-t2x": "lumina-t2x",
        "mochi": "mochi",
        "ltx-video": "ltx-video",
        "cogvideox-2b": "cogvideox-2b",
        "cogvideox-5b": "cogvideox-5b",
        "noobai xl": "noobai xl",
    }