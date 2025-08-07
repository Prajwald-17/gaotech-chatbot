#!/usr/bin/env python3
"""
Debug Entry Point for Vercel
============================

Debug version to see what's happening with imports.
"""

import os
import sys
from flask import Flask, jsonify

# Add paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, current_dir)
sys.path.insert(0, src_dir)

app = Flask(__name__)

@app.route('/')
def debug_home():
    """Debug information"""
    debug_info = {
        "current_dir": current_dir,
        "src_dir": src_dir,
        "sys_path": sys.path[:5],  # First 5 paths
        "files_in_current": os.listdir(current_dir) if os.path.exists(current_dir) else "Not found",
        "files_in_src": os.listdir(src_dir) if os.path.exists(src_dir) else "Not found",
    }
    
    # Try importing step by step
    import_results = {}
    
    try:
        import src
        import_results["src"] = "✅ Success"
    except Exception as e:
        import_results["src"] = f"❌ Error: {e}"
    
    try:
        import src.web
        import_results["src.web"] = "✅ Success"
    except Exception as e:
        import_results["src.web"] = f"❌ Error: {e}"
    
    try:
        import src.core
        import_results["src.core"] = "✅ Success"
    except Exception as e:
        import_results["src.core"] = f"❌ Error: {e}"
    
    try:
        from src.core.simple_vector_store import SimpleVectorStore
        import_results["SimpleVectorStore"] = "✅ Success"
    except Exception as e:
        import_results["SimpleVectorStore"] = f"❌ Error: {e}"
    
    try:
        from src.core.chatbot_engine import ChatbotEngine
        import_results["ChatbotEngine"] = "✅ Success"
    except Exception as e:
        import_results["ChatbotEngine"] = f"❌ Error: {e}"
    
    try:
        from src.web.web_interface import app as web_app
        import_results["web_interface"] = "✅ Success"
    except Exception as e:
        import_results["web_interface"] = f"❌ Error: {e}"
    
    return jsonify({
        "debug_info": debug_info,
        "import_results": import_results,
        "message": "Debug information for Vercel deployment"
    })

@app.route('/api/status')
def status():
    return jsonify({"status": "debug", "message": "Debug version running"})

if __name__ == '__main__':
    app.run(debug=True)