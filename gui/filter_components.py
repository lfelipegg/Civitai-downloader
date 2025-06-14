"""
Filter Components - Search and filtering widgets
"""

import tkinter as tk
from tkinter import ttk

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