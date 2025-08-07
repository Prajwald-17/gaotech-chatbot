#!/usr/bin/env python3
"""
Vercel Entry Point
==================

Simple entry point for Vercel deployment.
"""

import os
import sys

# Add paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, current_dir)
sys.path.insert(0, src_dir)

try:
    # Try importing the web interface
    from src.web.web_interface import app
    print("Successfully imported web interface")
except ImportError as e:
    print(f"Import error: {e}")
    # Create a minimal Flask app as fallback
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return jsonify({
            "status": "error",
            "message": "Import failed",
            "error": str(e)
        })
    
    @app.route('/api/status')
    def status():
        return jsonify({
            "status": "error", 
            "message": "Service temporarily unavailable"
        })

# Ensure app is available at module level
application = app

if __name__ == '__main__':
    app.run(debug=True)