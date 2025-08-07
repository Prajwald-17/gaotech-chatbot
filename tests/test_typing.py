#!/usr/bin/env python3
"""
Test script to verify the typing animation and always-visible prompts
"""

import webbrowser
import time
import subprocess
import sys
import os

def test_interface():
    """Test the updated interface features"""
    
    print("🧪 Testing Updated Real Estate IoT Chatbot Interface")
    print("="*60)
    
    print("✅ Features to test:")
    print("   1. Prompt questions always visible (sticky at top)")
    print("   2. Bot responses typed with cursor animation")
    print("   3. Clickable prompt questions work anytime")
    print("   4. Natural typing speed (20-50ms per character)")
    print("   5. Blinking cursor animation")
    
    print("\n🚀 Starting web server...")
    
    # Start the web interface
    try:
        # Start server in background
        server_process = subprocess.Popen([
            sys.executable, 
            "web_interface.py"
        ], cwd=os.getcwd())
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Open browser
        print("🌐 Opening browser at http://localhost:5000")
        webbrowser.open("http://localhost:5000")
        
        print("\n" + "="*60)
        print("🎯 TESTING CHECKLIST:")
        print("="*60)
        print("□ 1. Prompt questions visible at top of page")
        print("□ 2. Prompt questions stay visible when scrolling")
        print("□ 3. Click a prompt question - bot response types with cursor")
        print("□ 4. Type a custom question - bot response types with cursor")
        print("□ 5. Prompt questions still clickable after conversation starts")
        print("□ 6. Cursor blinks naturally during typing")
        print("□ 7. Sources appear after typing completes")
        print("□ 8. Multiple conversations work properly")
        
        print("\n💡 Test Questions to Try:")
        print("   • What is Real Estate IoT?")
        print("   • How do smart access control systems work?")
        print("   • Tell me about HVAC automation")
        print("   • What career opportunities are available?")
        
        print("\n⏳ Server running... Press Ctrl+C to stop")
        
        # Keep server running
        try:
            server_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            server_process.terminate()
            server_process.wait()
            print("✅ Server stopped")
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_interface()