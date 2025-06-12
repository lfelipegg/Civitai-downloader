# CivitAI Model Downloader

A modular Python tool for downloading AI models from CivitAI with automatic organization and documentation generation.

## Features

- **Automatic Organization**: Models are sorted into directories based on type and base model
- **Preview Images**: Downloads model preview images automatically
- **HTML Documentation**: Generates beautiful HTML pages for each model with metadata
- **Progress Tracking**: Visual progress bars for downloads
- **Metadata Management**: Saves complete model information in JSON format
- **Flexible Input**: Accepts CivitAI URLs or model IDs
- **Error Handling**: Robust error handling with detailed logging

## Project Structure

```
civitai_downloader/
├── main.py              # Main entry point
├── config.py            # Configuration settings
├── utils.py             # Utility functions
├── api_client.py        # CivitAI API client
├── downloader.py        # File download managers
├── html_generator.py    # HTML documentation generator
├── metadata_manager.py  # Metadata handling
├── model_processor.py   # Main processing logic
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

## Installation

1. **Clone or download the files** to a directory on your computer

2. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional but recommended):

   ```bash
   cp .env.example .env
   # Edit .env file and add your CivitAI API key
   ```

4. **Configure settings** in `config.py`:
   - Update `BASE_MODEL_DIR` to your preferred model storage location
   - Adjust `MAX_PREVIEW_IMAGES` and other settings as needed

## Usage

### Command Line Mode

Download specific models by providing CivitAI URLs:

```bash
# Download a single model (latest version)
python main.py "https://civitai.com/models/123456"

# Download a specific version
python main.py "https://civitai.com/models/123456?modelVersionId=789012"

# Download multiple models
python main.py "https://civitai.com/models/123456" "https://civitai.com/models/789012"
```

### Interactive Mode

Run without arguments for interactive mode:

```bash
python main.py
```

This provides a menu-driven interface to:

- Download models by entering URLs
- View existing downloads
- Browse downloaded model information

## File Organization

Models are automatically organized into a hierarchical directory structure:

```
Models/
├── FLUX/
│   ├── FLUX.1-Dev/
│   │   ├── Checkpoint/
│   │   ├── Lora/
│   │   └── Embeddings/
│   └── FLUX.1-Schnell/
├── SDXL/
│   ├── Base/
│   ├── Pony/
│   └── Illustrious/
├── SD15/
└── Other/
```

Each downloaded model gets its own directory containing:

- **Model file** (`.safetensors` preferred)
- **Preview images** (up to 3 images)
- **HTML documentation** (`_info.html`)
- **Metadata** (`_metadata.json`)

## Configuration

### Environment Variables

Create a `.env` file with your settings:

```bash
CIVITAI_API_KEY=your_api_key_here
```

### Config File

Modify `config.py` to customize:

- **Base directory**: Where models are downloaded
- **Directory structure**: How models are organized
- **Download settings**: Number of preview images, chunk size, etc.
- **Model mappings**: Add support for new model types

## API Key

While not required, having a CivitAI API key provides benefits:

- Access to private models
- Higher rate limits
- Better error handling

Get your API key from: https://civitai.com/user/account

## Module Overview

### Core Modules

- **`config.py`**: Central configuration and settings
- **`main.py`**: Command-line interface and entry point
- **`model_processor.py`**: Orchestrates the entire download process

### Specialized Modules

- **`api_client.py`**: Handles all CivitAI API interactions
- **`downloader.py`**: Manages file downloads with progress tracking
- **`html_generator.py`**: Creates beautiful HTML documentation
- **`metadata_manager.py`**: Handles metadata saving and loading
- **`utils.py`**: Common utility functions

## Examples

### Basic Download

```bash
python main.py "https://civitai.com/models/4384"
```

### Batch Download

Create a file `models.txt` with URLs (one per line) and use:

```bash
# Read URLs from file and download
cat models.txt | xargs python main.py
```

### Programmatic Usage

```python
from model_processor import ModelProcessor

processor = ModelProcessor()
result = processor.process_model("4384")  # Model ID
print(f"Downloaded to: {result['target_directory']}")
processor.cleanup()
```

## Error Handling

The tool includes comprehensive error handling:

- Network timeouts and retries
- Invalid URLs or model IDs
- Missing files or permissions
- API rate limiting
- Corrupted downloads

All errors are logged with detailed information for troubleshooting.

## Logging

Logs include:

- Download progress and status
- File organization decisions
- Error details and debugging information
- Processing summaries

## Contributing

To extend the tool:

1. **Add new model types**: Update `MODEL_TYPE_DIRS` in `config.py`
2. **Modify organization**: Change directory mapping logic in `utils.py`
3. **Enhance HTML**: Update templates in `html_generator.py`
4. **Add features**: Create new modules following the existing pattern

## Requirements

- Python 3.7+
- Internet connection
- Storage space for models (models can be several GB each)

## License

This tool is for personal use. Respect CivitAI's terms of service and model licenses.

## Troubleshooting

### Common Issues

1. **"No API key" warning**: Set `CIVITAI_API_KEY` environment variable
2. **Permission errors**: Check write permissions to download directory
3. **Network timeouts**: Check internet connection and try again
4. **Invalid URL format**: Ensure URLs are from civitai.com/models/

### Getting Help

- Check the logs for detailed error messages
- Verify your CivitAI URLs are valid
- Ensure you have enough disk space
- Try downloading one model at a time to isolate issues

---

**Note**: Always respect the licensing terms of downloaded models and CivitAI's terms of service.
