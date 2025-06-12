import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class HTMLGenerator:
    """
    Generates HTML documentation for downloaded models
    """
    
    def __init__(self):
        pass
    
    def generate_model_html(self, model, version, target_dir, downloaded_images, original_url=None):
        """
        Generate a complete HTML page for the downloaded model
        
        Args:
            model (dict): Model data from API
            version (dict): Version data from API
            target_dir (Path): Directory where model is saved
            downloaded_images (list): List of downloaded image paths
            original_url (str, optional): Original CivitAI URL
            
        Returns:
            str: Generated HTML content
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
        image_gallery = self._create_image_gallery(downloaded_images)
        
        # Create tags HTML
        tags_html = self._create_tags_html(model_tags)
        
        # Create trained words HTML
        trained_words_html = self._create_trained_words_html(trained_words)
        
        # Create original URL section
        original_url_html = self._create_original_url_html(original_url)
        
        # Generate complete HTML
        html_content = self._generate_html_template(
            model_name=model_name,
            model_description=model_description,
            model_type=model_type,
            version_name=version_name,
            version_description=version_description,
            base_model=base_model,
            tags_html=tags_html,
            trained_words_html=trained_words_html,
            image_gallery=image_gallery,
            original_url_html=original_url_html
        )
        
        return html_content
    
    def _create_image_gallery(self, downloaded_images):
        """Create HTML for image gallery"""
        if not downloaded_images:
            return ""
        
        image_gallery = "<div class='image-gallery'>\n"
        for img_path in downloaded_images:
            image_gallery += f"        <img src='{img_path.name}' alt='Preview Image' onclick='openModal(this.src)'>\n"
        image_gallery += "    </div>\n"
        return image_gallery
    
    def _create_tags_html(self, model_tags):
        """Create HTML for tags"""
        if not model_tags:
            return ""
        
        tags_html = "<div class='tags'>\n"
        for tag in model_tags:
            tags_html += f"        <span class='tag'>{tag}</span>\n"
        tags_html += "    </div>\n"
        return tags_html
    
    def _create_trained_words_html(self, trained_words):
        """Create HTML for trained words"""
        if not trained_words:
            return ""
        
        trained_words_html = "<div class='trained-words'>\n"
        trained_words_html += "        <h3>Trained Words/Triggers:</h3>\n"
        trained_words_html += "        <div class='word-list'>\n"
        for word in trained_words:
            trained_words_html += f"            <code>{word}</code>\n"
        trained_words_html += "        </div>\n"
        trained_words_html += "    </div>\n"
        return trained_words_html
    
    def _create_original_url_html(self, original_url):
        """Create HTML for original URL"""
        if not original_url:
            return ""
        
        return f"""
            <div class="info-card">
                <h3>Original Source</h3>
                <p><strong>CivitAI URL:</strong></p>
                <a href="{original_url}" target="_blank" class="civitai-link">{original_url}</a>
            </div>
        """
    
    def _generate_html_template(self, **kwargs):
        """Generate the complete HTML template"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{kwargs['model_name']}</title>
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
        
        .civitai-link {{
            color: #3498db;
            text-decoration: none;
            word-break: break-all;
            font-size: 0.9em;
            padding: 8px 12px;
            background: #f8f9fa;
            border-radius: 5px;
            border: 1px solid #dee2e6;
            display: inline-block;
            margin-top: 5px;
            transition: background-color 0.3s ease;
        }}
        
        .civitai-link:hover {{
            background: #e9ecef;
            text-decoration: underline;
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
            <h1>{kwargs['model_name']}</h1>
            <p>Version: {kwargs['version_name']}</p>
        </div>
        
        <div class="model-info">
            <div class="info-card">
                <h3>Model Information</h3>
                <p><strong>Type:</strong> {kwargs['model_type']}</p>
                <p><strong>Base Model:</strong> {kwargs['base_model']}</p>
            </div>
            
            <div class="info-card">
                <h3>Version Details</h3>
                <p><strong>Version Name:</strong> {kwargs['version_name']}</p>
                {f'<p><strong>Version Description:</strong> {kwargs["version_description"]}</p>' if kwargs['version_description'] else ''}
            </div>
            
            {kwargs['original_url_html']}
        </div>
        
        <div class="content">
            {f'<div class="description"><h3>Description</h3><p>{kwargs["model_description"]}</p></div>' if kwargs['model_description'] != 'No description available' else ''}
            
            {kwargs['trained_words_html']}
            
            {f'<h3>Tags</h3>{kwargs["tags_html"]}' if kwargs['tags_html'] else ''}
            
            {f'<h3>Preview Images</h3>{kwargs["image_gallery"]}' if kwargs['image_gallery'] else '<p>No preview images available</p>'}
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