# CivitAI Model Downloader - GUI Version

A modern, user-friendly graphical interface for downloading AI models from CivitAI with automatic organization and documentation.

## GUI Features

### 🎨 Modern Interface

- Clean, professional design with hover effects
- Tabbed interface for organized functionality
- Real-time progress tracking with visual feedback
- Comprehensive logging with color-coded messages

### 📥 Download Management

- **URL Queue System**: Add multiple URLs and manage download queue
- **Progress Tracking**: Real-time progress bars and status updates
- **Batch Downloads**: Download multiple models sequentially
- **Error Handling**: Graceful error handling with detailed feedback

### 📚 Library Management

- **Downloaded Models View**: Browse all downloaded models
- **Model Cards**: Rich display with model information and actions
- **Quick Actions**: Open model folders and view online sources
- **Search Functionality**: Filter models by name or type

### ⚙️ Settings Panel

- **API Key Management**: Secure API key storage with show/hide toggle
- **Download Directory**: Easy folder selection with browse dialog
- **Download Options**: Configurable preview image count
- **Settings Persistence**: Save and restore user preferences

## GUI Components

### Main Interface

```
┌─────────────────────────────────────────────────────┐
│ [Download] [Library] [Settings]                     │
├─────────────────────────────────────────────────────┤
│ CivitAI Model URLs:                          [Help] │
│ ┌─────────────────────────────────────────┐ [Add]   │
│ │ https://civitai.com/models/12345        │         │
│ └─────────────────────────────────────────┘         │
│                                                     │
│ Queue:                                              │
│ ┌─────────────────────────────────────────────────┐ │
│ │ • https://civitai.com/models/12345              │ │
│ │ • https://civitai.com/models/67890              │ │
│ └─────────────────────────────────────────────────┘ │
│ [Remove Selected] [Clear All]                       │
│                                                     │
│ [Start Download] [Stop] [Open Download Folder]      │
│                                                     │
│ Download Progress:                                  │
│ ████████████████████░░░░░░░░ 75%                   │
│ Downloading Model 12345: Generating documentation   │
│                                                     │
│ Log Output:                               [Clear]   │
│ ┌─────────────────────────────────────────────────┐ │
│ │ [12:34:56] INFO: Starting download...           │ │
│ │ [12:35:02] SUCCESS: ✓ Downloaded Model X       │ │
│ │ [12:35:15] WARNING: API rate limit reached     │ │
│ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

## Installation & Usage

### Quick Start

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Launch GUI**:
   ```bash
   python launch_gui.py
   ```
   Or directly:
   ```bash
   python gui.py
   ```

### First Time Setup

1. **Configure API Key** (recommended):

   - Go to Settings tab
   - Enter your CivitAI API key from https://civitai.com/user/account
   - Click "Save Settings"

2. **Set Download Directory**:

   - In Settings tab, browse for your preferred download location
   - Default is `N:/Models` (configurable in config.py)

3. **Adjust Download Options**:
   - Set maximum preview images to download (0-10)
   - Configure other preferences as needed

## Using the GUI

### Downloading Models

1. **Add URLs**:

   - Paste CivitAI model URL in the input field
   - Press Enter or click "Add URL"
   - Repeat for multiple models

2. **Manage Queue**:

   - View queued URLs in the list
   - Remove selected URLs or clear all
   - URLs are validated when added

3. **Start Download**:
   - Click "Start Download" to begin
   - Monitor progress in real-time
   - View detailed logs in the log panel
   - Stop downloads if needed

### Library Management

1. **View Downloaded Models**:

   - Switch to Library tab
   - Browse model cards with details
   - Search/filter models (coming soon)

2. **Model Actions**:
   - **Open Folder**: Open model directory in file explorer
   - **View Online**: Open original CivitAI page
   - **Model Info**: View detailed information

### Settings Configuration

1. **API Configuration**:

   - Enter your CivitAI API key for authenticated access
   - Use show/hide toggle for security
   - Required for private models and higher rate limits

2. **Directory Settings**:

   - Choose where models are downloaded
   - Directory structure is created automatically
   - Browse button for easy selection

3. **Download Options**:
   - Set maximum preview images (default: 3)
   - More options can be added in config.py

## GUI Architecture

### Component Structure

```
gui.py (Main Application)
├── gui_components.py (Custom Widgets)
│   ├── ModernButton (Styled buttons)
│   ├── ProgressFrame (Progress display)
│   ├── LogFrame (Logging widget)
│   ├── ModelCard (Model display)
│   └── UrlInputFrame (URL management)
├── download_manager_gui.py (GUI Download Manager)
└── Core modules (model_processor, api_client, etc.)
```

### Threading Model

- **Main Thread**: GUI updates and user interaction
- **Download Thread**: Model processing and file downloads
- **Thread-Safe Communication**: Queue-based messaging for updates

### Event System

- **Progress Callbacks**: Real-time progress updates
- **Log Callbacks**: Structured logging with levels
- **Status Callbacks**: Status bar updates
- **Completion Callbacks**: Download finish handling

## Customization

### Styling

Modify GUI appearance in `gui_components.py`:

```python
# Button color schemes
styles = {
    "primary": {"bg": "#3498db", "hover_bg": "#2980b9"},
    "success": {"bg": "#27ae60", "hover_bg": "#219a52"},
    # Add custom styles...
}
```

### Layout

Adjust layout in `gui.py`:

- Tab organization
- Widget placement
- Window sizing and constraints

### Functionality

Extend features by:

- Adding new tabs
- Creating custom widgets
- Implementing additional download options
- Adding model management features

## Troubleshooting

### Common Issues

1. **GUI Won't Start**:

   ```bash
   # Check dependencies
   python launch_gui.py
   # Install missing packages
   pip install tkinter requests tqdm python-dotenv
   ```

2. **Download Errors**:

   - Check internet connection
   - Verify CivitAI URLs are valid
   - Ensure API key is correct (if used)
   - Check download directory permissions

3. **Performance Issues**:

   - Limit concurrent downloads (built-in)
   - Close unused applications
   - Monitor disk space

4. **Display Issues**:
   - Update display drivers
   - Try different scaling settings
   - Restart the application

### Debug Mode

Enable detailed logging by modifying `utils.py`:

```python
setup_logging(level=logging.DEBUG)
```

### Getting Help

- Use the Help button in the GUI for quick reference
- Check the main README.md for detailed information
- Review log output for error details

## Advanced Features

### Keyboard Shortcuts

- **Enter**: Add URL to queue (when in URL field)
- **Escape**: Close help dialog
- **Ctrl+A**: Select all in text fields

### Batch Operations

- **Multiple URL Import**: Paste multiple URLs (one per line)
- **Queue Management**: Bulk remove/clear operations
- **Selective Downloads**: Remove specific URLs before starting

### Progress Monitoring

- **Real-time Updates**: Live progress and status
- **Detailed Logging**: Color-coded log levels
- **Error Recovery**: Graceful handling of failed downloads
- **Statistics**: Success/failure counts and timing

## Future Enhancements

Planned features for future versions:

- **Advanced Search**: Filter library by multiple criteria
- **Download Scheduling**: Queue downloads for later
- **Model Preview**: Image preview in library
- **Export Options**: Export model lists and metadata
- **Themes**: Light/dark theme support
- **Plugins**: Extensible architecture for custom features

---

**Note**: The GUI version provides the same core functionality as the command-line version but with enhanced usability and visual feedback. Both versions share the same underlying modular architecture.
