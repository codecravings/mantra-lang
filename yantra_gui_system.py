#!/usr/bin/env python3
"""
Yantra GUI System for Mantra Programming Language
Advanced features implementation: GUI creation with Sanskrit syntax
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum

# =============================================================================
# YANTRA (GUI) SYSTEM - EXTENDED AST NODES
# =============================================================================

@dataclass
class YantraNode:
    """GUI element creation with properties"""
    element_type: str
    properties: Dict[str, Any]
    children: List['YantraNode'] = None

@dataclass
class ShaktiNode:
    """Power expression for complex operations"""
    expression_type: str
    properties: Dict[str, Any]

@dataclass
class SutraNode:
    """Function composition chain"""
    functions: List[Any]

@dataclass
class RagaNode:
    """Data flow pattern"""
    source: Any
    transformations: List[Any]

@dataclass
class MandalNode:
    """Circular data structure"""
    elements: List[Any]

# =============================================================================
# YANTRA GUI IMPLEMENTATION
# =============================================================================

class YantraWidget:
    """Base class for all Yantra GUI widgets"""
    def __init__(self, widget_type: str, properties: Dict[str, Any]):
        self.widget_type = widget_type
        self.properties = properties
        self.tk_widget = None
        self.event_handlers = {}
    
    def create_widget(self, parent):
        """Create the actual tkinter widget"""
        if self.widget_type == "window":
            return self.create_window()
        elif self.widget_type == "label":
            return self.create_label(parent)
        elif self.widget_type == "button":
            return self.create_button(parent)
        elif self.widget_type == "entry":
            return self.create_entry(parent)
        elif self.widget_type == "text":
            return self.create_text(parent)
        elif self.widget_type == "frame":
            return self.create_frame(parent)
        elif self.widget_type == "menu":
            return self.create_menu(parent)
        else:
            raise ValueError(f"Unknown widget type: {self.widget_type}")
    
    def create_window(self):
        """Create a window (top-level)"""
        window = tk.Tk()
        window.title(self.properties.get('title', 'Mantra Application'))
        
        # Set size
        width = int(self.properties.get('width', 400))
        height = int(self.properties.get('height', 300))
        window.geometry(f"{width}x{height}")
        
        # Set other properties
        if 'resizable' in self.properties:
            resizable = self.properties['resizable']
            if isinstance(resizable, bool):
                window.resizable(resizable, resizable)
        
        if 'background' in self.properties:
            window.configure(bg=self.properties['background'])
        
        self.tk_widget = window
        return window
    
    def create_label(self, parent):
        """Create a label widget"""
        label = tk.Label(parent)
        
        # Set text
        if 'text' in self.properties:
            label.config(text=self.properties['text'])
        
        # Set font
        if 'font' in self.properties:
            label.config(font=self.properties['font'])
        
        # Set colors
        if 'color' in self.properties:
            label.config(fg=self.properties['color'])
        if 'background' in self.properties:
            label.config(bg=self.properties['background'])
        
        # Pack with options
        pack_options = {}
        if 'padding' in self.properties:
            pack_options['pady'] = self.properties['padding']
        
        label.pack(**pack_options)
        self.tk_widget = label
        return label
    
    def create_button(self, parent):
        """Create a button widget"""
        def button_clicked():
            if 'action' in self.properties:
                action = self.properties['action']
                if callable(action):
                    action()
                else:
                    print(f"Button '{self.properties.get('text', 'Button')}' clicked!")
        
        button = tk.Button(parent, command=button_clicked)
        
        # Set properties
        if 'text' in self.properties:
            button.config(text=self.properties['text'])
        
        if 'width' in self.properties:
            button.config(width=int(self.properties['width']) // 10)  # Approximate character width
        
        if 'height' in self.properties:
            button.config(height=int(self.properties['height']) // 20)  # Approximate line height
        
        if 'font' in self.properties:
            button.config(font=self.properties['font'])
        
        if 'color' in self.properties:
            button.config(fg=self.properties['color'])
        
        if 'background' in self.properties:
            button.config(bg=self.properties['background'])
        
        # Pack the button
        pack_options = {'pady': 5}
        if 'padding' in self.properties:
            pack_options['pady'] = self.properties['padding']
        
        button.pack(**pack_options)
        self.tk_widget = button
        return button
    
    def create_entry(self, parent):
        """Create an entry (text input) widget"""
        entry = tk.Entry(parent)
        
        # Set properties
        if 'width' in self.properties:
            entry.config(width=int(self.properties['width']) // 10)
        
        if 'font' in self.properties:
            entry.config(font=self.properties['font'])
        
        if 'placeholder' in self.properties:
            placeholder = self.properties['placeholder']
            entry.insert(0, placeholder)
            entry.config(fg='gray')
            
            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg='black')
            
            def on_focus_out(event):
                if entry.get() == '':
                    entry.insert(0, placeholder)
                    entry.config(fg='gray')
            
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)
        
        # Pack the entry
        pack_options = {'pady': 5}
        if 'padding' in self.properties:
            pack_options['pady'] = self.properties['padding']
        
        entry.pack(**pack_options)
        self.tk_widget = entry
        return entry
    
    def create_text(self, parent):
        """Create a text widget for multi-line input"""
        text = tk.Text(parent)
        
        # Set properties
        if 'width' in self.properties:
            text.config(width=int(self.properties['width']) // 10)
        
        if 'height' in self.properties:
            text.config(height=int(self.properties['height']) // 20)
        
        if 'font' in self.properties:
            text.config(font=self.properties['font'])
        
        # Pack the text widget
        pack_options = {'pady': 5}
        text.pack(**pack_options)
        self.tk_widget = text
        return text
    
    def create_frame(self, parent):
        """Create a frame container"""
        frame = tk.Frame(parent)
        
        # Set properties
        if 'background' in self.properties:
            frame.config(bg=self.properties['background'])
        
        if 'border' in self.properties:
            frame.config(relief='solid', borderwidth=1)
        
        # Pack the frame
        pack_options = {'pady': 5, 'fill': 'x'}
        frame.pack(**pack_options)
        self.tk_widget = frame
        return frame
    
    def create_menu(self, parent):
        """Create a menu"""
        menu = tk.Menu(parent)
        
        # Add menu items if specified
        if 'items' in self.properties:
            for item in self.properties['items']:
                if isinstance(item, str):
                    menu.add_command(label=item)
                elif isinstance(item, dict):
                    menu.add_command(label=item.get('text', 'Item'), 
                                   command=item.get('action', lambda: None))
        
        self.tk_widget = menu
        return menu

class YantraApplication:
    """Main application manager for Yantra GUI"""
    def __init__(self):
        self.widgets = []
        self.main_window = None
        self.is_running = False
    
    def add_widget(self, widget: YantraWidget):
        """Add a widget to the application"""
        self.widgets.append(widget)
    
    def create_window(self, properties: Dict[str, Any]):
        """Create the main application window"""
        window_widget = YantraWidget("window", properties)
        self.main_window = window_widget.create_widget(None)
        return self.main_window
    
    def run(self):
        """Run the GUI application"""
        if not self.main_window:
            # Create default window if none exists
            self.main_window = self.create_window({
                'title': 'Mantra Application',
                'width': 400,
                'height': 300
            })
        
        # Create all widgets
        for widget in self.widgets:
            if widget.widget_type != "window":  # Skip window widgets
                widget.create_widget(self.main_window)
        
        # Add a default close handler
        def on_closing():
            self.is_running = False
            self.main_window.destroy()
        
        self.main_window.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Start the GUI in a separate thread
        def run_gui():
            self.is_running = True
            self.main_window.mainloop()
        
        gui_thread = threading.Thread(target=run_gui, daemon=True)
        gui_thread.start()
        
        return f"Yantra application started with {len(self.widgets)} widgets"

# =============================================================================
# SHAKTI (POWER EXPRESSIONS) SYSTEM
# =============================================================================

class ShaktiProcessor:
    """Processor for Shakti power expressions"""
    
    @staticmethod
    def process_web_server(properties: Dict[str, Any]):
        """Create a simple web server"""
        port = properties.get('port', 8000)
        routes = properties.get('routes', [])
        
        try:
            # Try to use Flask if available
            from flask import Flask
            app = Flask(__name__)
            
            @app.route('/')
            def home():
                return f"<h1>Mantra Web Server</h1><p>Routes: {', '.join(routes)}</p>"
            
            # Start server in background thread
            def run_server():
                app.run(port=port, debug=False)
            
            server_thread = threading.Thread(target=run_server, daemon=True)
            server_thread.start()
            
            return f"Web server started on http://localhost:{port}"
        
        except ImportError:
            # Fallback to simple HTTP server
            import http.server
            import socketserver
            
            def run_simple_server():
                with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
                    httpd.serve_forever()
            
            server_thread = threading.Thread(target=run_simple_server, daemon=True)
            server_thread.start()
            
            return f"Simple HTTP server started on http://localhost:{port}"
    
    @staticmethod
    def process_database(properties: Dict[str, Any]):
        """Handle database operations"""
        db_type = properties.get('type', 'sqlite')
        db_file = properties.get('file', 'mantra.db')
        tables = properties.get('tables', [])
        
        if db_type == 'sqlite':
            try:
                import sqlite3
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                
                # Create tables if specified
                for table in tables:
                    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY)")
                
                conn.commit()
                conn.close()
                
                return f"SQLite database '{db_file}' created with tables: {', '.join(tables)}"
            except Exception as e:
                return f"Database error: {e}"
        
        return f"Database type '{db_type}' not yet supported"
    
    @staticmethod
    def process_file_operations(properties: Dict[str, Any]):
        """Handle file operations"""
        operation = properties.get('operation', 'read')
        filename = properties.get('file', 'mantra_file.txt')
        content = properties.get('content', '')
        
        try:
            if operation == 'read':
                with open(filename, 'r', encoding='utf-8') as f:
                    data = f.read()
                return f"Read {len(data)} characters from {filename}"
            
            elif operation == 'write':
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                return f"Written to {filename}"
            
            elif operation == 'append':
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write(content)
                return f"Appended to {filename}"
            
        except Exception as e:
            return f"File operation error: {e}"

# =============================================================================
# SUTRA (FUNCTION COMPOSITION) SYSTEM
# =============================================================================

class SutraComposer:
    """Function composition system"""
    
    @staticmethod
    def compose(*functions):
        """Compose multiple functions into one"""
        def composed_function(x):
            result = x
            for func in functions:
                if callable(func):
                    result = func(result)
                else:
                    # Handle Mantra function objects
                    result = func  # Simplified for now
            return result
        
        return composed_function

# =============================================================================
# RAGA (DATA FLOW) SYSTEM
# =============================================================================

class RagaProcessor:
    """Data flow processing system"""
    
    @staticmethod
    def process_flow(data, transformations):
        """Process data through a series of transformations"""
        result = data
        for transform in transformations:
            if callable(transform):
                result = transform(result)
            else:
                # Handle Mantra function objects
                result = transform  # Simplified for now
        
        return result

# =============================================================================
# MANDAL (CIRCULAR DATA) SYSTEM
# =============================================================================

class MandalStructure:
    """Circular data structure with special properties"""
    
    def __init__(self, elements):
        self.elements = list(elements)
        self.current_index = 0
    
    def next(self):
        """Get next element in circular fashion"""
        if not self.elements:
            return None
        
        value = self.elements[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.elements)
        return value
    
    def previous(self):
        """Get previous element in circular fashion"""
        if not self.elements:
            return None
        
        self.current_index = (self.current_index - 1) % len(self.elements)
        return self.elements[self.current_index]
    
    def current(self):
        """Get current element"""
        if not self.elements:
            return None
        return self.elements[self.current_index]
    
    def all(self):
        """Get all elements"""
        return self.elements.copy()
    
    def size(self):
        """Get size of mandal"""
        return len(self.elements)
    
    def __str__(self):
        return f"Mandal({self.elements}) at position {self.current_index}"
    
    def __repr__(self):
        return self.__str__()

# =============================================================================
# INTEGRATION WITH MAIN INTERPRETER
# =============================================================================

# Global application instance
yantra_app = YantraApplication()

def create_yantra_widget(element_type: str, properties: Dict[str, Any]):
    """Create a yantra widget and add it to the application"""
    widget = YantraWidget(element_type, properties)
    yantra_app.add_widget(widget)
    return widget

def process_shakti_expression(expression_type: str, properties: Dict[str, Any]):
    """Process a shakti power expression"""
    if expression_type == "gui_app":
        return yantra_app.create_window(properties)
    elif expression_type == "web_server":
        return ShaktiProcessor.process_web_server(properties)
    elif expression_type == "database":
        return ShaktiProcessor.process_database(properties)
    elif expression_type == "file_ops":
        return ShaktiProcessor.process_file_operations(properties)
    else:
        return f"Unknown shakti expression: {expression_type}"

def start_yantra_application():
    """Start the yantra GUI application"""
    return yantra_app.run()

# Export functions for use in interpreter
__all__ = [
    'YantraWidget', 'YantraApplication', 'ShaktiProcessor',
    'SutraComposer', 'RagaProcessor', 'MandalStructure',
    'create_yantra_widget', 'process_shakti_expression', 'start_yantra_application'
]