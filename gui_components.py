import tkinter as tk
from tkinter import ttk
import threading
import sys
import os
from pathlib import Path
from datetime import datetime

class ModernButton(tk.Button):
    """Modern styled button with hover effects"""
    
    def __init__(self, parent, text="", command=None, style="primary", **kwargs):
        # Color schemes
        styles = {
            "primary": {
                "bg": "#3498db",
                "fg": "white",
                "hover_bg": "#2980b9",
                "active_bg": "#1f618d"
            },
            "success": {
                "bg": "#27ae60", 
                "fg": "white",
                "hover_bg": "#219a52",
                "active_bg": "#1e8449"
            },
            "danger": {
                "bg": "#e74c3c",
                "fg": "white", 
                "hover_bg": "#c0392b",
                "active_bg": "#a93226"
            },
            "secondary": {
                "bg": "#95a5a6",
                "fg": "white",
                "hover_bg": "#7f8c8d", 
                "active_bg": "#6c7b7d"
            }
        }
        
        self.style_config = styles.get(style, styles["primary"])
        
        # Default button configuration
        default_config = {
            "text": text,
            "command": command,
            "bg": self.style_config["bg"],
            "fg": self.style_config["fg"],
            "font": ("Segoe UI", 10, "bold"),
            "bd": 0,
            "relief": "flat",
            "cursor": "hand2",
            "padx": 20,
            "pady": 8
        }
        default_config.update(kwargs)
        
        super().__init__(parent, **default_config)
        
        # Bind hover events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<ButtonRelease-1>", self._on_release)
    
    def _on_enter(self, event):
        self.config(bg=self.style_config["hover_bg"])
    
    def _on_leave(self, event):
        self.config(bg=self.style_config["bg"])
    
    def _on_click(self, event):
        self.config(bg=self.style_config["active_bg"])
    
    def _on_release(self, event):
        self.config(bg=self.style_config["hover_bg"])

class ProgressFrame(ttk.Frame):
    """Frame for displaying download progress"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self, 
            variable=self.progress_var,
            mode='determinate',
            length=400
        )
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to download")
        self.status_label = ttk.Label(
            self,
            textvariable=self.status_var,
            font=("Segoe UI", 9)
        )
        self.status_label.pack(pady=2)
        
        # Speed and ETA labels
        info_frame = ttk.Frame(self)
        info_frame.pack(fill="x", padx=10)
        
        self.speed_var = tk.StringVar(value="")
        self.eta_var = tk.StringVar(value="")
        
        ttk.Label(info_frame, textvariable=self.speed_var, font=("Segoe UI", 8)).pack(side="left")
        ttk.Label(info_frame, textvariable=self.eta_var, font=("Segoe UI", 8)).pack(side="right")
    
    def update_progress(self, percentage, status="", speed="", eta=""):
        """Update progress bar and status"""
        self.progress_var.set(percentage)
        if status:
            self.status_var.set(status)
        self.speed_var.set(speed)
        self.eta_var.set(eta)
        self.update_idletasks()
    
    def reset(self):
        """Reset progress to initial state"""
        self.progress_var.set(0)
        self.status_var.set("Ready to download")
        self.speed_var.set("")
        self.eta_var.set("")

class LogFrame(ttk.Frame):
    """Frame for displaying logs with different levels"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(self)
        text_frame.pack(fill="both", expand=True)
        
        self.text_widget = tk.Text(
            text_frame,
            wrap="word",
            font=("Consolas", 9),
            bg="#f8f9fa",
            fg="#2c3e50",
            selectbackground="#3498db",
            height=12
        )
        
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
        self.text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configure text tags for different log levels
        self.text_widget.tag_configure("INFO", foreground="#2c3e50")
        self.text_widget.tag_configure("WARNING", foreground="#f39c12")
        self.text_widget.tag_configure("ERROR", foreground="#e74c3c")
        self.text_widget.tag_configure("SUCCESS", foreground="#27ae60")
        self.text_widget.tag_configure("TIMESTAMP", foreground="#7f8c8d", font=("Consolas", 8))
        
        # Controls frame
        controls_frame = ttk.Frame(self)
        controls_frame.pack(fill="x", pady=(5, 0))
        
        ModernButton(
            controls_frame,
            text="Clear Log",
            command=self.clear_log,
            style="secondary"
        ).pack(side="right")
        
        ttk.Label(
            controls_frame,
            text="Log Output:",
            font=("Segoe UI", 10, "bold")
        ).pack(side="left")
    
    def add_log(self, message, level="INFO"):
        """Add a log message with timestamp and level"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.text_widget.insert("end", f"[{timestamp}] ", "TIMESTAMP")
        self.text_widget.insert("end", f"{level}: ", level)
        self.text_widget.insert("end", f"{message}\n", level)
        
        # Auto-scroll to bottom
        self.text_widget.see("end")
        self.update_idletasks()
    
    def clear_log(self):
        """Clear all log messages"""
        self.text_widget.delete(1.0, "end")

class ModelCard(ttk.Frame):
    """Enhanced card widget for displaying model information with optional image"""
    
    def __init__(self, parent, model_info, show_image=True, **kwargs):
        super().__init__(parent, relief="solid", borderwidth=1, **kwargs)
        
        self.model_info = model_info
        self.show_image = show_image
        
        # Debug: Print model info to check what we're receiving
        print(f"Creating card for: {model_info}")
        
        # Force a minimum size and ensure content is visible
        if show_image:
            self.configure(width=300, height=400)
        else:
            self.configure(width=400, height=120)
        
        # Create content immediately - don't rely on pack_propagate
        self.create_card_content()
    
    def create_card_content(self):
        """Create the card content directly"""
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        if self.show_image:
            self.create_image_content(main_frame)
        else:
            self.create_list_content(main_frame)
    
    def create_image_content(self, parent):
        """Create image card content"""
        # Image area
        image_frame = ttk.Frame(parent, height=180)
        image_frame.pack(fill="x", pady=(0, 10))
        image_frame.pack_propagate(False)
        
        # Check if PIL is available at startup
        self.pil_available = self.check_pil_available()
        
        if not self.pil_available:
            # Create PIL installation prompt
            self.create_pil_install_prompt(image_frame)
        else:
            # Create normal image label
            self.image_label = tk.Label(
                image_frame,
                text="🖼️ Loading Image...",
                bg="#f0f0f0",
                font=("Segoe UI", 10),
                fg="#666666"
            )
            self.image_label.pack(expand=True, fill="both")
            
            # Load image if PIL is available
            self.load_preview_image()
        
        # Info area
        info_frame = ttk.Frame(parent)
        info_frame.pack(fill="both", expand=True)
        
        # Model name
        name = self.model_info.get("model_name", "Unknown Model")
        name_label = tk.Label(
            info_frame,
            text=name,
            font=("Segoe UI", 11, "bold"),
            fg="#2c3e50",
            bg="#ffffff",
            anchor="w",
            justify="left"
        )
        name_label.pack(fill="x", pady=(0, 5))
        
        # Type
        model_type = self.model_info.get("model_type", "Unknown")
        type_label = tk.Label(
            info_frame,
            text=f"Type: {model_type}",
            font=("Segoe UI", 9),
            fg="#34495e",
            bg="#ffffff",
            anchor="w"
        )
        type_label.pack(fill="x")
        
        # Base model
        base_model = self.model_info.get("base_model", "Unknown")
        base_label = tk.Label(
            info_frame,
            text=f"Base: {base_model}",
            font=("Segoe UI", 9),
            fg="#34495e",
            bg="#ffffff",
            anchor="w"
        )
        base_label.pack(fill="x")
        
        # Date
        date_str = self.model_info.get('downloaded_at', '')[:10] if self.model_info.get('downloaded_at') else 'Unknown'
        date_label = tk.Label(
            info_frame,
            text=f"Downloaded: {date_str}",
            font=("Segoe UI", 8),
            fg="#7f8c8d",
            bg="#ffffff",
            anchor="w"
        )
        date_label.pack(fill="x")
        
        # Buttons
        self.create_buttons(info_frame)
    
    def check_pil_available(self):
        """Check if PIL is available"""
        try:
            from PIL import Image, ImageTk
            return True
        except ImportError:
            return False
    
    def create_pil_install_prompt(self, parent):
        """Create a user-friendly PIL installation prompt"""
        # Container for the prompt
        prompt_frame = tk.Frame(parent, bg="#fff3cd", relief="solid", borderwidth=1)
        prompt_frame.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Icon and message
        icon_label = tk.Label(
            prompt_frame,
            text="📦",
            font=("Segoe UI", 20),
            bg="#fff3cd",
            fg="#856404"
        )
        icon_label.pack(pady=(10, 5))
        
        message_label = tk.Label(
            prompt_frame,
            text="Image Support Missing",
            font=("Segoe UI", 10, "bold"),
            bg="#fff3cd",
            fg="#856404"
        )
        message_label.pack()
        
        install_label = tk.Label(
            prompt_frame,
            text="Install Pillow for image previews",
            font=("Segoe UI", 8),
            bg="#fff3cd",
            fg="#856404"
        )
        install_label.pack(pady=(2, 10))
        
        # Install command that can be copied
        command_frame = tk.Frame(prompt_frame, bg="#fff3cd")
        command_frame.pack(pady=(0, 10))
        
        command_label = tk.Label(
            command_frame,
            text="pip install Pillow",
            font=("Consolas", 9),
            bg="#ffffff",
            fg="#000000",
            relief="solid",
            borderwidth=1,
            padx=10,
            pady=2
        )
        command_label.pack()
        
        # Make the command selectable
        def select_command(event):
            # This doesn't work perfectly in tkinter, but shows the intent
            pass
        
        command_label.bind("<Button-1>", select_command)
        
        # Instructions
        help_label = tk.Label(
            prompt_frame,
            text="Run this command in your terminal\nthen restart the application",
            font=("Segoe UI", 7),
            bg="#fff3cd",
            fg="#856404",
            justify="center"
        )
        help_label.pack(pady=(0, 5))
    
    def load_preview_image(self):
        """Load preview image asynchronously (only if PIL is available)"""
        if not self.pil_available:
            return
            
        import threading
        
        def load_image():
            try:
                # Look for preview images in the model folder
                model_location = Path(self.model_info.get("location", ""))
                
                if model_location.exists():
                    # Look for preview images - specifically preview_01.jpeg first
                    priority_files = [
                        model_location / "preview_01.jpeg",
                        model_location / "preview_01.jpg", 
                        model_location / "preview_01.png",
                        model_location / "preview_01.webp"
                    ]
                    
                    image_file = None
                    # Check priority files first
                    for img_file in priority_files:
                        if img_file.exists():
                            image_file = img_file
                            break
                    
                    # If no priority files found, look for any preview images
                    if not image_file:
                        for ext in ['.jpg', '.jpeg', '.png', '.webp']:
                            found_files = list(model_location.glob(f"preview_*{ext}"))
                            if found_files:
                                image_file = found_files[0]
                                break
                    
                    if image_file:
                        try:
                            from PIL import Image, ImageTk
                            
                            # Load and resize image
                            image = Image.open(image_file)
                            image.thumbnail((270, 170), Image.Resampling.LANCZOS)
                            
                            # Convert to PhotoImage
                            photo = ImageTk.PhotoImage(image)
                            
                            # Update in main thread
                            self.after(0, lambda: self.update_image_display(photo))
                            return
                            
                        except Exception as e:
                            self.after(0, lambda: self.update_image_display(None, f"Error loading image"))
                            return
                
                # No image found
                self.after(0, lambda: self.update_image_display(None, "No preview available"))
                    
            except Exception as e:
                self.after(0, lambda: self.update_image_display(None, f"Error: {str(e)[:20]}..."))
        
        # Start loading in background thread
        threading.Thread(target=load_image, daemon=True).start()
    
    def create_list_content(self, parent):
        """Create list view content"""
        # Model name
        name = self.model_info.get("model_name", "Unknown Model")
        name_label = tk.Label(
            parent,
            text=name,
            font=("Segoe UI", 12, "bold"),
            fg="#2c3e50",
            bg="#ffffff",
            anchor="w"
        )
        name_label.pack(fill="x", pady=(0, 5))
        
        # Details frame
        details_frame = ttk.Frame(parent)
        details_frame.pack(fill="x", pady=(0, 5))
        
        # Type and Base in one line
        model_type = self.model_info.get("model_type", "Unknown")
        base_model = self.model_info.get("base_model", "Unknown")
        
        details_text = f"Type: {model_type} | Base: {base_model}"
        details_label = tk.Label(
            details_frame,
            text=details_text,
            font=("Segoe UI", 9),
            fg="#34495e",
            bg="#ffffff",
            anchor="w"
        )
        details_label.pack(fill="x")
        
        # Date
        date_str = self.model_info.get('downloaded_at', '')[:10] if self.model_info.get('downloaded_at') else 'Unknown'
        date_label = tk.Label(
            details_frame,
            text=f"Downloaded: {date_str}",
            font=("Segoe UI", 8),
            fg="#7f8c8d",
            bg="#ffffff",
            anchor="w"
        )
        date_label.pack(fill="x")
        
        # Buttons
        self.create_buttons(parent)
    
    def create_buttons(self, parent):
        """Create action buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", pady=(10, 0))
        
        # Open folder button
        open_btn = tk.Button(
            button_frame,
            text="📁 Open",
            command=self.open_model_folder,
            bg="#95a5a6",
            fg="white",
            font=("Segoe UI", 8),
            relief="flat",
            cursor="hand2"
        )
        open_btn.pack(side="left", padx=(0, 5))
        
        # View online button (if URL available)
        if self.model_info.get("original_url"):
            online_btn = tk.Button(
                button_frame,
                text="🌐 View",
                command=self.view_online,
                bg="#3498db",
                fg="white",
                font=("Segoe UI", 8),
                relief="flat",
                cursor="hand2"
            )
            online_btn.pack(side="left")
    
    def update_image_display(self, photo=None, error_msg=None):
        """Update image display in main thread"""
        if hasattr(self, 'image_label') and self.image_label:
            if photo:
                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo  # Keep reference
            else:
                error_text = error_msg or "🖼️ No Preview"
                self.image_label.configure(
                    image="",
                    text=error_text,
                    bg="#f0f0f0",
                    fg="#666666"
                )
    
    def open_model_folder(self):
        """Open model folder in file explorer"""
        try:
            import subprocess
            folder_path = self.model_info.get("location", "")
            
            if os.path.exists(folder_path):
                if os.name == 'nt':  # Windows
                    os.startfile(folder_path)
                elif os.name == 'posix':  # macOS and Linux
                    subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", folder_path])
        except Exception as e:
            print(f"Could not open folder: {e}")
    
    def view_online(self):
        """Open original CivitAI page"""
        try:
            import webbrowser
            url = self.model_info.get("original_url")
            if url:
                webbrowser.open(url)
        except Exception as e:
            print(f"Could not open URL: {e}")
    
    # Legacy methods for compatibility
    def update_status(self, status, progress=None):
        """Update the card status and progress"""
        pass  # Simplified for now

class FilterFrame(ttk.Frame):
    """Frame for filtering and sorting options"""
    
    def __init__(self, parent, on_filter_change=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.on_filter_change = on_filter_change
        
        # Filter controls
        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill="x", pady=(0, 10))
        
        # Search
        search_frame = ttk.Frame(filter_frame)
        search_frame.pack(side="left", fill="x", expand=True)
        
        ttk.Label(search_frame, text="Search:", font=("Segoe UI", 9)).pack(side="left")
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side="left", padx=(5, 10))
        search_entry.bind("<KeyRelease>", self._on_filter_change)
        
        # Type filter
        ttk.Label(search_frame, text="Type:", font=("Segoe UI", 9)).pack(side="left")
        
        self.type_var = tk.StringVar(value="All")
        type_combo = ttk.Combobox(
            search_frame,
            textvariable=self.type_var,
            values=["All", "Checkpoint", "LoRA", "TextualInversion", "Hypernetwork", "ControlNet"],
            state="readonly",
            width=12
        )
        type_combo.pack(side="left", padx=(5, 10))
        type_combo.bind("<<ComboboxSelected>>", self._on_filter_change)
        
        # Base model filter
        ttk.Label(search_frame, text="Base:", font=("Segoe UI", 9)).pack(side="left")
        
        self.base_var = tk.StringVar(value="All")
        base_combo = ttk.Combobox(
            search_frame,
            textvariable=self.base_var,
            values=["All", "FLUX.1 [Dev]", "FLUX.1 [Schnell]", "SDXL 1.0", "SD 1.5", "Pony", "Illustrious XL"],
            state="readonly",
            width=15
        )
        base_combo.pack(side="left", padx=(5, 10))
        base_combo.bind("<<ComboboxSelected>>", self._on_filter_change)
        
        # Hide unknown checkbox
        self.hide_unknown_var = tk.BooleanVar(value=True)
        hide_unknown_cb = ttk.Checkbutton(
            search_frame,
            text="Hide Unknown",
            variable=self.hide_unknown_var,
            command=self._on_filter_change
        )
        hide_unknown_cb.pack(side="left", padx=(10, 0))
        
        # Sort options
        sort_frame = ttk.Frame(filter_frame)
        sort_frame.pack(side="right")
        
        ttk.Label(sort_frame, text="Sort by:", font=("Segoe UI", 9)).pack(side="left")
        
        self.sort_var = tk.StringVar(value="Date (Newest)")
        sort_combo = ttk.Combobox(
            sort_frame,
            textvariable=self.sort_var,
            values=["Date (Newest)", "Date (Oldest)", "Name (A-Z)", "Name (Z-A)", "Type", "Base Model"],
            state="readonly",
            width=15
        )
        sort_combo.pack(side="left", padx=(5, 0))
        sort_combo.bind("<<ComboboxSelected>>", self._on_filter_change)
    
    def _on_filter_change(self, event=None):
        """Handle filter change events"""
        if self.on_filter_change:
            self.on_filter_change()
    
    def get_filters(self):
        """Get current filter settings"""
        return {
            "search": self.search_var.get().lower().strip(),
            "type": self.type_var.get(),
            "base": self.base_var.get(),
            "hide_unknown": self.hide_unknown_var.get(),
            "sort": self.sort_var.get()
        }

class UrlInputFrame(ttk.Frame):
    """Frame for URL input with validation and multi-line support"""
    
    def __init__(self, parent, on_add_callback=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.on_add_callback = on_add_callback
        
        # Input section
        input_frame = ttk.Frame(self)
        input_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(
            input_frame,
            text="CivitAI Model URLs:",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")
        
        # URL entry - now using Text widget for multi-line support
        url_entry_frame = ttk.Frame(input_frame)
        url_entry_frame.pack(fill="x", pady=(5, 0))
        
        # Multi-line text widget with scrollbar
        text_frame = ttk.Frame(url_entry_frame)
        text_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.url_text = tk.Text(
            text_frame,
            height=3,
            font=("Segoe UI", 10),
            wrap="none"
        )
        
        # Scrollbar for text widget
        text_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.url_text.yview)
        self.url_text.configure(yscrollcommand=text_scrollbar.set)
        
        self.url_text.pack(side="left", fill="both", expand=True)
        text_scrollbar.pack(side="right", fill="y")
        
        # Placeholder text
        self.placeholder_text = "Enter CivitAI URLs (one per line):\nhttps://civitai.com/models/12345\nhttps://civitai.com/models/67890?modelVersionId=12345"
        self._show_placeholder()
        
        # Bind events for placeholder behavior
        self.url_text.bind("<FocusIn>", self._on_focus_in)
        self.url_text.bind("<FocusOut>", self._on_focus_out)
        self.url_text.bind("<KeyPress>", self._on_key_press)
        
        # Buttons frame
        buttons_frame = ttk.Frame(url_entry_frame)
        buttons_frame.pack(side="right", fill="y")
        
        # Add URLs button
        ModernButton(
            buttons_frame,
            text="Add URLs",
            command=self._add_urls,
            style="primary"
        ).pack(fill="x", pady=(0, 5))
        
        # Clear input button
        ModernButton(
            buttons_frame,
            text="Clear Input",
            command=self._clear_input,
            style="secondary"
        ).pack(fill="x")
        
        # URL list
        list_frame = ttk.Frame(input_frame)
        list_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Header with count
        list_header = ttk.Frame(list_frame)
        list_header.pack(fill="x", pady=(0, 5))
        
        self.queue_label = ttk.Label(
            list_header,
            text="Queue (0 URLs):",
            font=("Segoe UI", 9, "bold")
        )
        self.queue_label.pack(side="left")
        
        # Import/Export buttons
        import_export_frame = ttk.Frame(list_header)
        import_export_frame.pack(side="right")
        
        ModernButton(
            import_export_frame,
            text="📁 Import",
            command=self._import_urls,
            style="secondary"
        ).pack(side="left", padx=(0, 5))
        
        ModernButton(
            import_export_frame,
            text="💾 Export",
            command=self._export_urls,
            style="secondary"
        ).pack(side="left")
        
        # Listbox with scrollbar
        listbox_frame = ttk.Frame(list_frame)
        listbox_frame.pack(fill="both", expand=True, pady=(5, 0))
        
        self.url_listbox = tk.Listbox(
            listbox_frame,
            font=("Segoe UI", 9),
            height=6,
            selectmode="extended"
        )
        
        list_scrollbar = ttk.Scrollbar(
            listbox_frame,
            orient="vertical",
            command=self.url_listbox.yview
        )
        self.url_listbox.configure(yscrollcommand=list_scrollbar.set)
        
        self.url_listbox.pack(side="left", fill="both", expand=True)
        list_scrollbar.pack(side="right", fill="y")
        
        # List controls
        list_controls = ttk.Frame(list_frame)
        list_controls.pack(fill="x", pady=(5, 0))
        
        ModernButton(
            list_controls,
            text="Remove Selected",
            command=self._remove_selected,
            style="danger"
        ).pack(side="left")
        
        ModernButton(
            list_controls,
            text="Clear All",
            command=self._clear_all,
            style="secondary"
        ).pack(side="left", padx=(10, 0))
        
        # URL validation status
        self.status_var = tk.StringVar(value="")
        self.status_label = ttk.Label(
            list_controls,
            textvariable=self.status_var,
            font=("Segoe UI", 8),
            foreground="#7f8c8d"
        )
        self.status_label.pack(side="right")
    
    def _show_placeholder(self):
        """Show placeholder text"""
        self.url_text.delete(1.0, "end")
        self.url_text.insert(1.0, self.placeholder_text)
        self.url_text.configure(fg="#999999")
        self._placeholder_active = True
    
    def _hide_placeholder(self):
        """Hide placeholder text"""
        if self._placeholder_active:
            self.url_text.delete(1.0, "end")
            self.url_text.configure(fg="#000000")
            self._placeholder_active = False
    
    def _on_focus_in(self, event):
        """Handle focus in event"""
        self._hide_placeholder()
    
    def _on_focus_out(self, event):
        """Handle focus out event"""
        content = self.url_text.get(1.0, "end").strip()
        if not content:
            self._show_placeholder()
    
    def _on_key_press(self, event):
        """Handle key press events"""
        if self._placeholder_active:
            self._hide_placeholder()
        
        # Handle Ctrl+A for select all
        if event.keysym == 'a' and event.state & 0x4:  # Ctrl key
            self.url_text.tag_add("sel", "1.0", "end")
            return "break"
    
    def _add_urls(self):
        """Add URLs from text input to the list"""
        if self._placeholder_active:
            return
        
        content = self.url_text.get(1.0, "end").strip()
        if not content:
            self.status_var.set("No URLs entered")
            return
        
        # Split by lines and clean up
        urls = [url.strip() for url in content.split('\n') if url.strip()]
        
        if not urls:
            self.status_var.set("No valid URLs found")
            return
        
        # Validate and add URLs
        valid_urls = []
        invalid_urls = []
        duplicate_urls = []
        existing_urls = set(self.get_urls())
        
        for url in urls:
            if url in existing_urls:
                duplicate_urls.append(url)
            elif self._is_valid_civitai_url(url):
                valid_urls.append(url)
                existing_urls.add(url)
            else:
                invalid_urls.append(url)
        
        # Add valid URLs to listbox
        for url in valid_urls:
            self.url_listbox.insert("end", url)
            if self.on_add_callback:
                self.on_add_callback(url)
        
        # Update queue count
        self._update_queue_count()
        
        # Show status
        status_parts = []
        if valid_urls:
            status_parts.append(f"Added {len(valid_urls)} URLs")
        if duplicate_urls:
            status_parts.append(f"{len(duplicate_urls)} duplicates skipped")
        if invalid_urls:
            status_parts.append(f"{len(invalid_urls)} invalid URLs")
        
        self.status_var.set(" | ".join(status_parts))
        
        # Clear input after successful addition
        if valid_urls:
            self.url_text.delete(1.0, "end")
            self._show_placeholder()
    
    def _is_valid_civitai_url(self, url):
        """Validate if URL is a CivitAI model URL"""
        import re
        pattern = r'https?://civitai\.com/models/\d+(?:\?.*)?'
        return re.match(pattern, url) is not None
    
    def _clear_input(self):
        """Clear the input text area"""
        self.url_text.delete(1.0, "end")
        self._show_placeholder()
        self.status_var.set("Input cleared")
    
    def _import_urls(self):
        """Import URLs from a text file"""
        from tkinter import filedialog
        
        file_path = filedialog.askopenfilename(
            title="Import URLs from file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Insert content into text widget
                self._hide_placeholder()
                self.url_text.delete(1.0, "end")
                self.url_text.insert(1.0, content)
                
                self.status_var.set(f"Imported from {os.path.basename(file_path)}")
                
            except Exception as e:
                self.status_var.set(f"Import failed: {str(e)[:30]}...")
    
    def _export_urls(self):
        """Export URLs to a text file"""
        from tkinter import filedialog
        
        urls = self.get_urls()
        if not urls:
            self.status_var.set("No URLs to export")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export URLs to file",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for url in urls:
                        f.write(url + '\n')
                
                self.status_var.set(f"Exported {len(urls)} URLs to {os.path.basename(file_path)}")
                
            except Exception as e:
                self.status_var.set(f"Export failed: {str(e)[:30]}...")
    
    def _remove_selected(self):
        """Remove selected URLs from the list"""
        selected = self.url_listbox.curselection()
        if not selected:
            self.status_var.set("No URLs selected")
            return
        
        # Remove in reverse order to maintain indices
        for index in reversed(selected):
            self.url_listbox.delete(index)
        
        self._update_queue_count()
        self.status_var.set(f"Removed {len(selected)} URLs")
    
    def _clear_all(self):
        """Clear all URLs from the list"""
        count = self.url_listbox.size()
        self.url_listbox.delete(0, "end")
        self._update_queue_count()
        self.status_var.set(f"Cleared {count} URLs")
    
    def _update_queue_count(self):
        """Update the queue count label"""
        count = self.url_listbox.size()
        self.queue_label.configure(text=f"Queue ({count} URLs):")
    
    def get_urls(self):
        """Get all URLs in the list"""
        return [self.url_listbox.get(i) for i in range(self.url_listbox.size())]
    
    def add_url_programmatically(self, url):
        """Add URL programmatically"""
        if url and url not in self.get_urls():
            self.url_listbox.insert("end", url)
            self._update_queue_count()