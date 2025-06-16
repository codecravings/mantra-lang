#!/usr/bin/env python3
import os

# Create missing README.md
with open("README.md", "w") as f:
    f.write("# Mantra Programming Language\n\nA Sanskrit-inspired programming language.\n")

# Create simple setup.py 
setup_content = '''from setuptools import setup, find_packages

setup(
    name="mantra-lang",
    version="0.1.0", 
    packages=find_packages(),
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "mantra=mantra.cli:main",
        ],
    },
)'''

with open("setup.py", "w") as f:
    f.write(setup_content)

print("✅ Fixed setup files. Now run: pip install -e .")
