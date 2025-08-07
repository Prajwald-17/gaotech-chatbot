#!/usr/bin/env python3
"""
Main Application Entry Point
============================

This is the main entry point for the Real Estate IoT Chatbot application.
It imports and runs the Flask web interface.
"""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.web.web_interface import app

if __name__ == '__main__':
    print("🏠 Real Estate IoT Chatbot - Starting Web Interface...")
    
    # Get port from environment variable
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"🌐 Visit: http://localhost:{port}")
    print("💡 Press Ctrl+C to stop the server")
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)