"""
GUI Components Package - Modular GUI components for CivitAI downloader

This package contains all the GUI components organized into logical modules:
- core_components: Basic reusable widgets (buttons, progress, logs)
- filter_components: Search and filtering widgets
- url_components: URL input and management
- model_components: Model cards and display widgets
"""

# Import all components for easy access
from .core_components import ModernButton, ProgressFrame, LogFrame
from .filter_components import FilterFrame
from .url_components import UrlInputFrame
from .model_components import ModelCard

# Version info
__version__ = "1.0.0"
__author__ = "CivitAI Downloader Team"

# Export all components
__all__ = [
    'ModernButton',
    'ProgressFrame', 
    'LogFrame',
    'FilterFrame',
    'UrlInputFrame',
    'ModelCard'
]