#!/usr/bin/env python3
"""
Quick start script for Real Estate IoT Chatbot
This script provides an easy way to start the chatbot system.
"""

import os
import sys
import subprocess
import webbrowser
import time
from threading import Timer

def check_setup():
    """Check if the system is set up"""
    required_files = [
        'data/scraped_content.json',
        'data/text_chunks.json', 
        'data/vector_store.faiss'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    return len(missing_files) == 0, missing_files

def open_browser():
    """Open browser after a delay"""
    time.sleep(3)  # Wait for server to start
    try:
        webbrowser.open('http://localhost:5000')
        print("🌐 Opened browser at http://localhost:5000")
    except:
        print("💡 Please open your browser and go to: http://localhost:5000")

def main():
    """Main function"""
    print("🏠 Real Estate IoT Chatbot - Quick Start")
    print("=" * 50)
    
    # Check if system is set up
    is_setup, missing_files = check_setup()
    
    if not is_setup:
        print("❌ System not set up yet!")
        print("Missing files:")
        for file in missing_files:
            print(f"  - {file}")
        
        print("\n🔧 Running setup first...")
        try:
            subprocess.run([sys.executable, 'setup.py'], check=True)
            print("✅ Setup completed!")
        except subprocess.CalledProcessError:
            print("❌ Setup failed. Please run 'python setup.py' manually.")
            return False
        except FileNotFoundError:
            print("❌ setup.py not found. Please ensure you're in the correct directory.")
            return False
    
    # Start the web interface
    print("\n🚀 Starting Real Estate IoT Chatbot...")
    print("📡 Server will start at: http://localhost:5000")
    print("🌐 Browser will open automatically")
    print("\n💡 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Open browser after delay
    Timer(3.0, open_browser).start()
    
    try:
        # Start Flask app
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n\n👋 Chatbot stopped. Goodbye!")
    except FileNotFoundError:
        print("❌ app.py not found. Please ensure you're in the correct directory.")
        return False
    except Exception as e:
        print(f"❌ Error starting chatbot: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Failed to start chatbot.")
        print("💡 Try running 'python setup.py' first, then 'python app.py'")
        sys.exit(1)