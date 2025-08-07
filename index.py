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
    print("Falling back to test version...")
    
    # Import the test version as fallback
    try:
        import sys
        import os
        test_file = os.path.join(os.path.dirname(__file__), 'test_index.py')
        
        # Import test_index module
        import importlib.util
        spec = importlib.util.spec_from_file_location("test_index", test_file)
        test_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_module)
        app = test_module.app
        print("Successfully loaded test version as fallback")
        
    except Exception as fallback_error:
        print(f"Fallback error: {fallback_error}")
        # Create minimal Flask app as last resort
        from flask import Flask, jsonify
        
        app = Flask(__name__)
        
        @app.route('/')
        def home():
            return jsonify({
                "status": "error",
                "message": "Service temporarily unavailable",
                "error": str(e),
                "fallback_error": str(fallback_error)
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