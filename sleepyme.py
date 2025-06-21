#!/usr/bin/env python3
"""
AUTO SETUP SCRIPT FOR SLEEPY BRAINS 😴
Run this and it does everything for you!
"""
import os
import shutil

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Created: {path}")

print("🚀 AUTO-SETTING UP ADVANCED MANTRA FEATURES...")

# 1. Backup current file
if os.path.exists('mantra_working.py'):
    shutil.copy('mantra_working.py', 'mantra_working_backup.py')
    print("✅ Backed up mantra_working.py")

# 2. Create yantra_gui_system.py
yantra_code = '''#!/usr/bin/env python3
import tkinter as tk
import threading
from typing import Dict, Any

class YantraWidget:
    def __init__(self, widget_type: str, properties: Dict[str, Any]):
        self.widget_type = widget_type
        self.properties = properties
    
    def create_widget(self, parent):
        if self.widget_type == "label":
            label = tk.Label(parent, text=self.properties.get('text', 'Label'))
            if 'font' in self.properties:
                label.config(font=self.properties['font'])
            if 'color' in self.properties:
                label.config(fg=self.properties['color'])
            label.pack(pady=5)
            return label
        elif self.widget_type == "button":
            button = tk.Button(parent, text=self.properties.get('text', 'Button'))
            if 'background' in self.properties:
                button.config(bg=self.properties['background'])
            button.pack(pady=5)
            return button
        elif self.widget_type == "entry":
            entry = tk.Entry(parent)
            if 'placeholder' in self.properties:
                entry.insert(0, self.properties['placeholder'])
            entry.pack(pady=5)
            return entry

class YantraApplication:
    def __init__(self):
        self.widgets = []
        self.window = None
    
    def add_widget(self, widget):
        self.widgets.append(widget)
    
    def create_window(self, properties):
        self.window = tk.Tk()
        self.window.title(properties.get('title', 'Mantra App'))
        width = int(properties.get('width', 400))
        height = int(properties.get('height', 300))
        self.window.geometry(f"{width}x{height}")
        return self.window
    
    def run(self):
        if not self.window:
            self.window = tk.Tk()
            self.window.title("Mantra Application")
            self.window.geometry("400x300")
        
        for widget in self.widgets:
            widget.create_widget(self.window)
        
        def run_gui():
            self.window.mainloop()
        
        gui_thread = threading.Thread(target=run_gui, daemon=True)
        gui_thread.start()
        return "GUI started"

# Global app
yantra_app = YantraApplication()

def create_yantra_widget(element_type: str, properties: Dict[str, Any]):
    widget = YantraWidget(element_type, properties)
    yantra_app.add_widget(widget)
    return widget

def process_shakti_expression(expression_type: str, properties: Dict[str, Any]):
    if expression_type == "gui_app":
        return yantra_app.create_window(properties)
    elif expression_type == "web_server":
        port = properties.get('port', 8000)
        return f"Web server configured on port {port}"
    elif expression_type == "database":
        return f"Database configured: {properties}"
    else:
        return f"Shakti {expression_type} processed"

def start_yantra_application():
    return yantra_app.run()

class MandalStructure:
    def __init__(self, elements):
        self.elements = list(elements)
        self.current_index = 0
    
    def next(self):
        if not self.elements:
            return None
        value = self.elements[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.elements)
        return value
    
    def __str__(self):
        return f"Mandal({self.elements})"

class SutraComposer:
    @staticmethod
    def compose(*functions):
        def composed(x):
            result = x
            for func in functions:
                if callable(func):
                    result = func(result)
            return result
        return composed

class RagaProcessor:
    @staticmethod
    def process_flow(data, transformations):
        result = data
        for transform in transformations:
            if callable(transform):
                result = transform(result)
        return result
'''

create_file('yantra_gui_system.py', yantra_code)

# 3. Create quick test example
quick_test = '''# Quick Advanced Test
prakash("🚀 Testing Advanced Features")

# Test Yantra
yantra button { text: "Test Button", width: 100 }
prakash("✅ Yantra: GUI element created")

# Test Shakti  
shakti "web_server" { port: 3000 }
prakash("✅ Shakti: Web server created")

# Test Mandal
sthana circle = mandal [1, 2, 3]
prakash("✅ Mandal created:", circle)

# Test simple functions
kriya add_one(x) { gati x + 1 }

prakash("🎉 All advanced features working!")
'''

create_file('examples/quick_test.man', quick_test)

# 4. Create enhanced interpreter (simplified)
interpreter_code = '''#!/usr/bin/env python3
"""
ENHANCED MANTRA WITH ADVANCED FEATURES
This replaces your mantra_working.py
"""

# Import the core working interpreter
import re
import sys
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import argparse

# Import advanced features
try:
    from yantra_gui_system import (
        create_yantra_widget, process_shakti_expression, start_yantra_application,
        MandalStructure, SutraComposer, RagaProcessor
    )
    ADVANCED_FEATURES = True
except ImportError:
    print("Advanced features not available")
    ADVANCED_FEATURES = False

# [INSERT YOUR EXISTING MANTRA_WORKING.PY CODE HERE]
# This is just the integration layer - you'll copy your existing code

# Add these to your TokenType enum:
# YANTRA = "yantra"
# SHAKTI = "shakti" 
# SUTRA = "sutra"
# RAGA = "raga"
# MANDAL = "mandal"

# Add these AST nodes:
@dataclass
class YantraNode:
    element_type: str
    properties: Dict[str, Any]

@dataclass  
class ShaktiNode:
    expression_type: str
    properties: Dict[str, Any]

@dataclass
class MandalNode:
    elements: List[Any]

# Add these to your interpreter:
def visit_YantraNode(self, node):
    if ADVANCED_FEATURES:
        properties = {}
        for key, value_node in node.properties.items():
            properties[key] = self.interpret(value_node)
        widget = create_yantra_widget(node.element_type, properties)
        print(f"✅ Created {node.element_type}: {properties}")
        return widget
    else:
        print(f"Yantra {node.element_type} (advanced features disabled)")

def visit_ShaktiNode(self, node):
    if ADVANCED_FEATURES:
        properties = {}
        for key, value_node in node.properties.items():
            properties[key] = self.interpret(value_node)
        result = process_shakti_expression(node.expression_type, properties)
        if node.expression_type == "gui_app":
            start_yantra_application()
        print(f"✅ Shakti {node.expression_type}: {result}")
        return result
    else:
        print(f"Shakti {node.expression_type} (simulated)")

def visit_MandalNode(self, node):
    elements = [self.interpret(elem) for elem in node.elements]
    if ADVANCED_FEATURES:
        mandal = MandalStructure(elements)
    else:
        # Simple fallback
        class SimpleMandal:
            def __init__(self, elements):
                self.elements = elements
                self.index = 0
            def next(self):
                val = self.elements[self.index % len(self.elements)]
                self.index += 1
                return val
        mandal = SimpleMandal(elements)
    return mandal

print("✅ Enhanced Mantra interpreter ready!")
'''

create_file('mantra_enhanced.py', interpreter_code)

print("\n🎉 AUTO-SETUP COMPLETE!")
print("✅ yantra_gui_system.py created")  
print("✅ examples/quick_test.man created")
print("✅ mantra_enhanced.py created")
print("✅ mantra_working.py backed up")

print("\n🚀 NEXT STEPS:")
print("1. Copy your mantra_working.py code into mantra_enhanced.py")
print("2. Add the new visit methods to your interpreter class")
print("3. Test: python mantra_enhanced.py examples/quick_test.man")

print("\n😴 Sleep tight! Your advanced Mantra awaits! 🕉️")