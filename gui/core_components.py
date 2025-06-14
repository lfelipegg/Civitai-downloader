"""
Core GUI Components - Basic reusable widgets
"""

import tkinter as tk
from tkinter import ttk
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