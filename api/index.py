#!/usr/bin/env python3
"""
Vercel API Entry Point
=====================

This is the entry point for Vercel deployment.
It imports and exposes the Flask application.
"""

import os
import sys

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')

sys.path.insert(0, parent_dir)
sys.path.insert(0, src_dir)

try:
    from src.web.web_interface import app
except ImportError:
    # Fallback import path
    sys.path.insert(0, os.path.join(parent_dir, 'src', 'web'))
    from web_interface import app

# Export the app for Vercel
app = app

if __name__ == '__main__':
    app.run(debug=True)