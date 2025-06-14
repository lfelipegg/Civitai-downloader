"""
URL Components - URL input and management widgets
"""

import tkinter as tk
from tkinter import ttk, filedialog
import os
from .core_components import ModernButton

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
        
        # URL list section
        self._create_url_list(input_frame)
    
    def _create_url_list(self, parent):
        """Create the URL list section"""
        list_frame = ttk.Frame(parent)
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