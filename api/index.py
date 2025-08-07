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
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.web.web_interface import app

# This is required for Vercel
def handler(request):
    return app(request.environ, lambda status, headers: None)

# Export the app for Vercel
application = app

if __name__ == '__main__':
    app.run(debug=True)