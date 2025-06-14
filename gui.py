#!/usr/bin/env python3
"""
CivitAI Model Downloader - GUI Version
A modern graphical interface for downloading AI models from CivitAI
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import sys
import webbrowser
from pathlib import Path

# Import from modular GUI components
from gui import (
    ModernButton, ProgressFrame, LogFrame, 
    ModelCard, UrlInputFrame, FilterFrame
)

from download_manager_gui import GUIDownloadManager
from metadata_manager import MetadataManager
from config import Config
from utils import setup_logging

class CivitAIDownloaderGUI:
    """Main GUI application for CivitAI Model Downloader"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_variables()
        self.setup_gui()
        self.setup_download_manager()
        
        # Setup logging
        setup_logging()
        
        # Initial status
        self.log_frame.add_log("CivitAI Model Downloader started", "INFO")
        self.check_configuration()
    
    def setup_window(self):
        """Configure the main window"""
        self.root.title("CivitAI Model Downloader")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Icon (if available)
        try:
            # You can add an icon file here
            pass
        except:
            pass
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.root.configure(bg="#ecf0f1")
    
    def setup_variables(self):
        """Setup tkinter variables"""
        self.status_var = tk.StringVar(value="Ready")
        self.api_key_var = tk.StringVar(value=Config.API_KEY or "")
        self.download_dir_var = tk.StringVar(value=str(Config.BASE_MODEL_DIR))
    
    def setup_gui(self):
        """Setup the GUI layout"""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill="both", expand=True)
        
        # Create tabs
        self.create_download_tab()
        self.create_library_tab()
        self.create_settings_tab()
        
        # Status bar
        self.create_status_bar(main_container)
    
    def create_download_tab(self):
        """Create the main download tab"""
        download_frame = ttk.Frame(self.notebook)
        self.notebook.add(download_frame, text="Download")
        
        # Header
        header_frame = ttk.Frame(download_frame)
        header_frame.pack(fill="x", pady=(0, 10))
        
        title_label = ttk.Label(
            header_frame,
            text="CivitAI Model Downloader",
            font=("Segoe UI", 16, "bold"),
            foreground="#2c3e50"
        )
        title_label.pack(side="left")
        
        # Help button
        ModernButton(
            header_frame,
            text="Help",
            command=self.show_help,
            style="secondary"
        ).pack(side="right")
        
        # URL input section
        self.url_input_frame = UrlInputFrame(
            download_frame,
            on_add_callback=self.on_url_added
        )
        self.url_input_frame.pack(fill="x", pady=(0, 10))
        
        # Control buttons
        controls_frame = ttk.Frame(download_frame)
        controls_frame.pack(fill="x", pady=(0, 10))
        
        self.download_button = ModernButton(
            controls_frame,
            text="Start Download",
            command=self.start_download,
            style="success"
        )
        self.download_button.pack(side="left")
        
        self.stop_button = ModernButton(
            controls_frame,
            text="Stop Download",
            command=self.stop_download,
            style="danger"
        )
        self.stop_button.pack(side="left", padx=(10, 0))
        self.stop_button.configure(state="disabled")
        
        ModernButton(
            controls_frame,
            text="Open Download Folder",
            command=self.open_download_folder,
            style="secondary"
        ).pack(side="right")
        
        # Progress section
        progress_label = ttk.Label(
            download_frame,
            text="Download Progress:",
            font=("Segoe UI", 10, "bold")
        )
        progress_label.pack(anchor="w", pady=(10, 5))
        
        self.progress_frame = ProgressFrame(download_frame)
        self.progress_frame.pack(fill="x", pady=(0, 10))
        
        # Log section
        self.log_frame = LogFrame(download_frame)
        self.log_frame.pack(fill="both", expand=True)
    
    def create_library_tab(self):
        """Create the enhanced library/history tab with filtering and image cards"""
        library_frame = ttk.Frame(self.notebook)
        self.notebook.add(library_frame, text="Library")
        
        # Header
        header_frame = ttk.Frame(library_frame)
        header_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(
            header_frame,
            text="Downloaded Models",
            font=("Segoe UI", 14, "bold"),
            foreground="#2c3e50"
        ).pack(side="left")
        
        # Header controls
        header_controls = ttk.Frame(header_frame)
        header_controls.pack(side="right")
        
        # View toggle
        self.view_mode_var = tk.StringVar(value="cards")
        view_frame = ttk.Frame(header_controls)
        view_frame.pack(side="left", padx=(0, 10))
        
        ttk.Label(view_frame, text="View:").pack(side="left")
        view_combo = ttk.Combobox(
            view_frame,
            textvariable=self.view_mode_var,
            values=["cards", "list"],
            state="readonly",
            width=8
        )
        view_combo.pack(side="left", padx=(5, 0))
        view_combo.bind("<<ComboboxSelected>>", lambda e: self.switch_view_mode())
        
        ModernButton(
            header_controls,
            text="🔄 Refresh",
            command=self.refresh_library,
            style="primary"
        ).pack(side="right")
        
        # Filter frame
        self.filter_frame = FilterFrame(library_frame, on_filter_change=self.apply_filters)
        self.filter_frame.pack(fill="x", pady=(0, 10))
        
        # Library content with scrollbar
        library_content_frame = ttk.Frame(library_frame)
        library_content_frame.pack(fill="both", expand=True)
        
        # Canvas and scrollbar for scrollable content
        self.library_canvas = tk.Canvas(library_content_frame, bg="#ecf0f1")
        library_scrollbar = ttk.Scrollbar(library_content_frame, orient="vertical", command=self.library_canvas.yview)
        self.library_scrollable_frame = ttk.Frame(self.library_canvas)
        
        # Configure scrolling
        def configure_scroll_region(event=None):
            self.library_canvas.configure(scrollregion=self.library_canvas.bbox("all"))
        
        def configure_canvas_width(event):
            canvas_width = event.width
            self.library_canvas.itemconfig(self.canvas_window, width=canvas_width)
        
        self.library_scrollable_frame.bind("<Configure>", configure_scroll_region)
        self.library_canvas.bind("<Configure>", configure_canvas_width)
        
        self.canvas_window = self.library_canvas.create_window((0, 0), window=self.library_scrollable_frame, anchor="nw")
        self.library_canvas.configure(yscrollcommand=library_scrollbar.set)
        
        self.library_canvas.pack(side="left", fill="both", expand=True)
        library_scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel for better scrolling
        def _on_mousewheel(event):
            self.library_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def _bind_to_mousewheel(event):
            self.library_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            self.library_canvas.unbind_all("<MouseWheel>")
        
        self.library_canvas.bind('<Enter>', _bind_to_mousewheel)
        self.library_canvas.bind('<Leave>', _unbind_from_mousewheel)
        
        # Pagination controls
        pagination_frame = ttk.Frame(library_frame)
        pagination_frame.pack(fill="x", pady=(10, 0))
        
        # Results info
        self.results_var = tk.StringVar(value="")
        results_label = ttk.Label(pagination_frame, textvariable=self.results_var, font=("Segoe UI", 9))
        results_label.pack(side="left")
        
        # Load more button
        self.load_more_button = ModernButton(
            pagination_frame,
            text="📄 Load More Models",
            command=self.load_more_models,
            style="secondary"
        )
        self.load_more_button.pack(side="right")
        
        # Initialize library state
        self.library_items = []
        self.all_models = []
        self.filtered_models = []
        self.displayed_count = 0
        self.models_per_page = 20  # Show 20 models at a time
        
        # Initial library load
        self.refresh_library()
    
    def create_settings_tab(self):
        """Create the settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        # Settings content
        settings_content = ttk.Frame(settings_frame)
        settings_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ttk.Label(
            settings_content,
            text="Settings",
            font=("Segoe UI", 14, "bold"),
            foreground="#2c3e50"
        ).pack(anchor="w", pady=(0, 20))
        
        # API Key section
        api_section = ttk.LabelFrame(settings_content, text="CivitAI API Configuration", padding=15)
        api_section.pack(fill="x", pady=(0, 20))
        
        ttk.Label(api_section, text="API Key:").pack(anchor="w")
        api_key_frame = ttk.Frame(api_section)
        api_key_frame.pack(fill="x", pady=(5, 0))
        
        self.api_key_entry = ttk.Entry(api_key_frame, textvariable=self.api_key_var, show="*", width=50)
        self.api_key_entry.pack(side="left", fill="x", expand=True)
        
        ModernButton(
            api_key_frame,
            text="Show/Hide",
            command=self.toggle_api_key_visibility,
            style="secondary"
        ).pack(side="right", padx=(10, 0))
        
        ttk.Label(
            api_section,
            text="Get your API key from: https://civitai.com/user/account",
            font=("Segoe UI", 8),
            foreground="#7f8c8d"
        ).pack(anchor="w", pady=(5, 0))
        
        # Download directory section
        dir_section = ttk.LabelFrame(settings_content, text="Download Directory", padding=15)
        dir_section.pack(fill="x", pady=(0, 20))
        
        ttk.Label(dir_section, text="Download Path:").pack(anchor="w")
        dir_frame = ttk.Frame(dir_section)
        dir_frame.pack(fill="x", pady=(5, 0))
        
        self.dir_entry = ttk.Entry(dir_frame, textvariable=self.download_dir_var, width=50)
        self.dir_entry.pack(side="left", fill="x", expand=True)
        
        ModernButton(
            dir_frame,
            text="Browse",
            command=self.browse_download_directory,
            style="secondary"
        ).pack(side="right", padx=(10, 0))
        
        # Download settings section
        download_section = ttk.LabelFrame(settings_content, text="Download Settings", padding=15)
        download_section.pack(fill="x", pady=(0, 20))
        
        # Max preview images
        images_frame = ttk.Frame(download_section)
        images_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(images_frame, text="Max Preview Images:").pack(side="left")
        self.max_images_var = tk.IntVar(value=Config.MAX_PREVIEW_IMAGES)
        images_spin = ttk.Spinbox(images_frame, from_=0, to=10, textvariable=self.max_images_var, width=10)
        images_spin.pack(side="right")
        
        # Save settings button
        ModernButton(
            settings_content,
            text="Save Settings",
            command=self.save_settings,
            style="success"
        ).pack(pady=(20, 0))
    
    def create_status_bar(self, parent):
        """Create the status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill="x", side="bottom", pady=(10, 0))
        
        # Status label
        status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            foreground="#7f8c8d"
        )
        status_label.pack(side="left")
        
        # Version info
        version_label = ttk.Label(
            status_frame,
            text="v1.0.0",
            font=("Segoe UI", 9),
            foreground="#bdc3c7"
        )
        version_label.pack(side="right")
    
    def setup_download_manager(self):
        """Setup the download manager with callbacks"""
        self.download_manager = GUIDownloadManager(
            progress_callback=self.update_progress,
            log_callback=self.add_log,
            status_callback=self.update_status
        )
    
    def start_download(self):
        """Start the download process"""
        urls = self.url_input_frame.get_urls()
        
        if not urls:
            messagebox.showwarning("No URLs", "Please add some CivitAI URLs to download.")
            return
        
        if self.download_manager.start_download(urls):
            self.download_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            self.progress_frame.reset()
            self.add_log(f"Starting download of {len(urls)} models", "INFO")
        
        # Start checking download status
        self.check_download_status()
    
    def stop_download(self):
        """Stop the download process"""
        self.download_manager.stop_download()
        self.download_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
    
    def check_download_status(self):
        """Check download status periodically"""
        if self.download_manager.is_busy():
            # Schedule next check
            self.root.after(1000, self.check_download_status)
        else:
            # Download finished
            self.download_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.refresh_library()  # Refresh library to show new downloads
    
    def update_progress(self, percentage, status=""):
        """Update progress bar"""
        self.progress_frame.update_progress(percentage, status)
    
    def update_status(self, status):
        """Update status bar"""
        self.status_var.set(status)
    
    def add_log(self, message, level="INFO"):
        """Add log message"""
        self.log_frame.add_log(message, level)
    
    def on_url_added(self, url):
        """Callback when URL is added"""
        self.add_log(f"Added URL to queue: {url}", "INFO")
    
    def refresh_library(self):
        """Refresh the library of downloaded models with filtering"""
        # Clear existing items first
        self.clear_library_display()
        
        # Reset pagination
        self.displayed_count = 0
        
        # Get downloaded models
        try:
            metadata_manager = MetadataManager()
            metadata_files = metadata_manager.find_existing_downloads(Config.BASE_MODEL_DIR)
            
            self.add_log(f"Found {len(metadata_files)} metadata files", "INFO")
            
            if not metadata_files:
                self.show_no_models_message()
                return
            
            # Load model summaries (only if not already loaded or if forced refresh)
            if not hasattr(self, 'all_models') or not self.all_models:
                self.all_models = []
                for metadata_file in metadata_files:
                    try:
                        summary = metadata_manager.get_download_summary(metadata_file)
                        if summary:
                            self.all_models.append(summary)
                            self.add_log(f"Loaded model: {summary.get('model_name', 'Unknown')}", "INFO")
                    except Exception as e:
                        self.add_log(f"Error loading metadata from {metadata_file}: {e}", "ERROR")
                
                self.add_log(f"Successfully loaded {len(self.all_models)} models", "INFO")
            
            # Apply current filters
            self.apply_filters()
            
        except Exception as e:
            self.add_log(f"Error refreshing library: {e}", "ERROR")
            self.show_no_models_message()
    
    def apply_filters(self):
        """Apply current filter settings to the model list"""
        try:
            filters = self.filter_frame.get_filters()
            
            # Filter models
            self.filtered_models = []
            for model in self.all_models:
                # Hide unknown filter
                if filters["hide_unknown"]:
                    if (model.get("model_type", "").lower() == "unknown" or 
                        model.get("base_model", "").lower() == "unknown"):
                        continue
                
                # Search filter
                if filters["search"]:
                    search_text = filters["search"]
                    if not any(search_text in str(model.get(field, "")).lower() 
                              for field in ["model_name", "model_type", "base_model"]):
                        continue
                
                # Type filter
                if filters["type"] != "All":
                    if model.get("model_type", "").lower() != filters["type"].lower():
                        continue
                
                # Base model filter
                if filters["base"] != "All":
                    if filters["base"].lower() not in model.get("base_model", "").lower():
                        continue
                
                self.filtered_models.append(model)
            
            self.add_log(f"Filtered to {len(self.filtered_models)} models", "INFO")
            
            # Sort models
            self.sort_models(filters["sort"])
            
            # Reset display and show first page
            self.displayed_count = 0
            self.clear_library_display()
            self.load_more_models()
            
            # Update results info
            total = len(self.filtered_models)
            self.results_var.set(f"Showing {min(self.displayed_count, total)} of {total} models")
            
        except Exception as e:
            self.add_log(f"Error applying filters: {e}", "ERROR")
    
    def sort_models(self, sort_option):
        """Sort models based on selected option"""
        if sort_option == "Date (Newest)":
            self.filtered_models.sort(key=lambda x: x.get("downloaded_at", ""), reverse=True)
        elif sort_option == "Date (Oldest)":
            self.filtered_models.sort(key=lambda x: x.get("downloaded_at", ""))
        elif sort_option == "Name (A-Z)":
            self.filtered_models.sort(key=lambda x: x.get("model_name", "").lower())
        elif sort_option == "Name (Z-A)":
            self.filtered_models.sort(key=lambda x: x.get("model_name", "").lower(), reverse=True)
        elif sort_option == "Type":
            self.filtered_models.sort(key=lambda x: x.get("model_type", "").lower())
        elif sort_option == "Base Model":
            self.filtered_models.sort(key=lambda x: x.get("base_model", "").lower())
    
    def load_more_models(self):
        """Load more models (pagination)"""
        start_idx = self.displayed_count
        end_idx = min(start_idx + self.models_per_page, len(self.filtered_models))
        
        if start_idx >= len(self.filtered_models):
            return  # No more models to load
        
        view_mode = self.view_mode_var.get()
        
        if view_mode == "cards":
            self.load_model_cards(start_idx, end_idx)
        else:
            self.load_model_list(start_idx, end_idx)
        
        self.displayed_count = end_idx
        
        # Update button state
        if self.displayed_count >= len(self.filtered_models):
            self.load_more_button.configure(state="disabled", text="All Models Loaded")
        else:
            remaining = len(self.filtered_models) - self.displayed_count
            self.load_more_button.configure(
                state="normal", 
                text=f"📄 Load More ({remaining} remaining)"
            )
        
        # Update results info
        total = len(self.filtered_models)
        self.results_var.set(f"Showing {self.displayed_count} of {total} models")
    
    def load_model_cards(self, start_idx, end_idx):
        """Load models as image cards"""
        try:
            self.add_log(f"Loading cards {start_idx} to {end_idx}", "INFO")
            
            # Create grid container for cards
            cards_per_row = 3  # Adjust based on window size
            current_row_frame = None
            
            for i in range(start_idx, end_idx):
                model_info = self.filtered_models[i]
                self.add_log(f"Creating card for: {model_info.get('model_name', 'Unknown')}", "INFO")
                
                # Create row frame if needed
                if (i - start_idx) % cards_per_row == 0:
                    current_row_frame = ttk.Frame(self.library_scrollable_frame)
                    current_row_frame.pack(fill="x", padx=10, pady=5, anchor="n")
                
                # Create model card with image
                try:
                    card = ModelCard(current_row_frame, model_info, show_image=True)
                    card.pack(side="left", padx=5, pady=5, anchor="n")
                    self.library_items.append(card)
                    self.add_log(f"Successfully created card for: {model_info.get('model_name', 'Unknown')}", "INFO")
                except Exception as card_error:
                    self.add_log(f"Error creating card: {card_error}", "ERROR")
            
            # Update canvas scroll region
            self.library_canvas.update_idletasks()
            self.library_canvas.configure(scrollregion=self.library_canvas.bbox("all"))
                    
        except Exception as e:
            self.add_log(f"Error loading model cards: {e}", "ERROR")
    
    def load_model_list(self, start_idx, end_idx):
        """Load models as simple list"""
        try:
            for i in range(start_idx, end_idx):
                model_info = self.filtered_models[i]
                
                # Create simple model card
                card = ModelCard(self.library_scrollable_frame, model_info, show_image=False)
                card.pack(fill="x", padx=10, pady=2, anchor="n")
                self.library_items.append(card)
            
            # Update canvas scroll region
            self.library_canvas.update_idletasks()
            self.library_canvas.configure(scrollregion=self.library_canvas.bbox("all"))
            
        except Exception as e:
            self.add_log(f"Error loading model list: {e}", "ERROR")
    
    def clear_library_display(self):
        """Clear library display"""
        for item in self.library_items:
            try:
                item.destroy()
            except:
                pass  # Handle any destruction errors
        self.library_items.clear()
        
        # Reset scroll position to top and clear any cached layouts
        self.library_canvas.yview_moveto(0)
        self.library_canvas.update_idletasks()
        
        # Force canvas to recalculate its layout
        self.library_canvas.configure(scrollregion=(0, 0, 0, 0))
    
    def show_no_models_message(self):
        """Show message when no models are found"""
        self.results_var.set("No models found")
        self.load_more_button.configure(state="disabled", text="No Models")
        
        no_models_frame = ttk.Frame(self.library_scrollable_frame)
        no_models_frame.pack(expand=True, fill="both")
        
        message_text = f"📁 No downloaded models found in:\n{Config.BASE_MODEL_DIR}\n\nDownload some models from the Download tab!"
        
        no_models_label = ttk.Label(
            no_models_frame,
            text=message_text,
            font=("Segoe UI", 12),
            foreground="#7f8c8d",
            justify="center"
        )
        no_models_label.pack(expand=True)
        self.library_items.append(no_models_frame)
        
        self.add_log(f"No models found in directory: {Config.BASE_MODEL_DIR}", "WARNING")
    
    def create_model_card(self, model_info):
        """Create a model card for the library (legacy method - now handled by ModelCard class)"""
        # This method is now handled by the enhanced ModelCard class
        # Keeping for compatibility
        return ModelCard(self.library_scrollable_frame, model_info, show_image=False)
    
    def open_download_folder(self):
        """Open the download folder in file explorer"""
        try:
            os.startfile(str(Config.BASE_MODEL_DIR))
        except AttributeError:
            # For non-Windows systems
            import subprocess
            subprocess.run(["open" if os.name == "posix" else "xdg-open", str(Config.BASE_MODEL_DIR)])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {e}")
    
    def open_model_folder(self, folder_path):
        """Open a specific model folder"""
        try:
            os.startfile(folder_path)
        except AttributeError:
            import subprocess
            subprocess.run(["open" if os.name == "posix" else "xdg-open", folder_path])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {e}")
    
    def browse_download_directory(self):
        """Browse for download directory"""
        folder = filedialog.askdirectory(
            title="Select Download Directory",
            initialdir=self.download_dir_var.get()
        )
        if folder:
            self.download_dir_var.set(folder)
    
    def toggle_api_key_visibility(self):
        """Toggle API key visibility"""
        current_show = self.api_key_entry.cget("show")
        self.api_key_entry.configure(show="" if current_show else "*")
    
    def save_settings(self):
        """Save settings"""
        # Update config (in a real app, you'd save to file)
        Config.API_KEY = self.api_key_var.get()
        Config.BASE_MODEL_DIR = Path(self.download_dir_var.get())
        Config.MAX_PREVIEW_IMAGES = self.max_images_var.get()
        
        # Update headers with new API key
        Config.HEADERS = {"Authorization": f"Bearer {Config.API_KEY}" if Config.API_KEY else ""}
        
        messagebox.showinfo("Settings", "Settings saved successfully!")
        self.add_log("Settings updated", "INFO")
    
    def check_configuration(self):
        """Check initial configuration"""
        if not Config.API_KEY:
            self.add_log("No API key configured. Some models may require authentication.", "WARNING")
        
        if not Config.BASE_MODEL_DIR.exists():
            try:
                Config.BASE_MODEL_DIR.mkdir(parents=True, exist_ok=True)
                self.add_log(f"Created download directory: {Config.BASE_MODEL_DIR}", "INFO")
            except Exception as e:
                self.add_log(f"Could not create download directory: {e}", "ERROR")
        
        # Check if PIL is available for image display
        try:
            from PIL import Image, ImageTk
            self.add_log("PIL (Pillow) available for image preview", "INFO")
        except ImportError:
            self.add_log("PIL (Pillow) not found. Install with: pip install Pillow", "WARNING")
            self.add_log("Images will use basic tkinter support (PNG only)", "INFO")
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
CivitAI Model Downloader Help

How to use:
1. Enter CivitAI model URLs in the URL field
2. Click "Add URL" or press Enter to add to queue
3. Click "Start Download" to begin downloading
4. Monitor progress in the log and progress bar

URL Formats:
• https://civitai.com/models/12345 (latest version)
• https://civitai.com/models/12345?modelVersionId=67890 (specific version)

Features:
• Automatic file organization by model type
• Preview image downloads
• HTML documentation generation
• Download history in Library tab

Settings:
• API Key: Get from https://civitai.com/user/account
• Download Directory: Where models are saved
• Max Preview Images: Number of preview images to download

Tips:
• Models are organized automatically by type and base model
• Each model gets its own folder with all files
• Use the Library tab to view downloaded models
• Check the log for detailed information
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("600x500")
        help_window.transient(self.root)
        help_window.grab_set()
        
        text_widget = tk.Text(help_window, wrap="word", padx=20, pady=20)
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", help_text)
        text_widget.configure(state="disabled")
        
        close_button = ModernButton(
            help_window,
            text="Close",
            command=help_window.destroy,
            style="primary"
        )
        close_button.pack(pady=10)
    
    def switch_view_mode(self):
        """Switch between view modes without reloading data"""
        # Clear display but keep the model data
        self.clear_library_display()
        
        # Reset pagination for the new view
        self.displayed_count = 0
        
        # Load models with the new view mode
        self.load_more_models()
    
    def _on_mousewheel(self, event):
        """Handle mousewheel scrolling (legacy method - now handled by enhanced binding)"""
        # This method is kept for compatibility but actual scrolling is handled
        # by the enhanced mousewheel binding in create_library_tab
        pass
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    """Main entry point for GUI application"""
    app = CivitAIDownloaderGUI()
    app.run()

if __name__ == "__main__":
    main()