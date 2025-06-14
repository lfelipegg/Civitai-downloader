"""
Model Components - Model cards and display widgets
"""

import tkinter as tk
from tkinter import ttk
import threading
import sys
import os
import webbrowser
from pathlib import Path

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