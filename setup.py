#!/usr/bin/env python3
"""
Real Estate IoT Chatbot Setup Script
This script sets up the complete chatbot system step by step.
"""

import os
import sys
import subprocess
import json
from datetime import datetime

def print_step(step_num, title, description):
    """Print formatted step information"""
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {title}")
    print(f"{'='*60}")
    print(description)
    print()

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error in {description}:")
        print(f"  Command: {command}")
        print(f"  Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    
    packages = [
        "requests>=2.28.0",
        "beautifulsoup4>=4.11.0", 
        "nltk>=3.8",
        "numpy>=1.21.0",
        "faiss-cpu>=1.7.0",
        "sentence-transformers>=2.2.0",
        "flask>=2.2.0",
        "python-dotenv>=0.19.0",
        "lxml>=4.9.0"
    ]
    
    for package in packages:
        if not run_command(f"pip install {package}", f"Installing {package.split('>=')[0]}"):
            return False
    
    return True

def setup_directories():
    """Create necessary directories"""
    directories = ['data', 'templates', 'static']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    return True

def run_scraper():
    """Run the website scraper"""
    print("Starting website scraping...")
    try:
        import website_scraper
        print("✓ Website scraper completed")
        return True
    except Exception as e:
        print(f"✗ Website scraper failed: {e}")
        return False

def run_chunker():
    """Run the text chunker"""
    print("Starting text chunking...")
    try:
        import text_chunker
        print("✓ Text chunking completed")
        return True
    except Exception as e:
        print(f"✗ Text chunking failed: {e}")
        return False

def run_vector_store():
    """Create vector store"""
    print("Creating vector store...")
    try:
        import vector_store
        print("✓ Vector store created")
        return True
    except Exception as e:
        print(f"✗ Vector store creation failed: {e}")
        return False

def create_env_file():
    """Create .env file template"""
    env_content = """# Real Estate IoT Chatbot Configuration
# 
# Optional: Add your OpenAI API key to use GPT models
# OPENAI_API_KEY=your_openai_api_key_here
#
# Flask configuration
FLASK_ENV=development
FLASK_DEBUG=True
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✓ Created .env configuration file")
    return True

def main():
    """Main setup function"""
    print("🏠 Real Estate IoT Chatbot Setup")
    print("=" * 50)
    
    # Step 0: Check Python version
    if not check_python_version():
        return False
    
    # Step 1: Install requirements
    print_step(1, "Installing Dependencies", 
               "Installing required Python packages...")
    if not install_requirements():
        print("❌ Failed to install requirements")
        return False
    
    # Step 2: Setup directories
    print_step(2, "Setting Up Directories", 
               "Creating necessary directories...")
    if not setup_directories():
        print("❌ Failed to setup directories")
        return False
    
    # Step 3: Create environment file
    print_step(3, "Configuration Setup", 
               "Creating configuration files...")
    if not create_env_file():
        print("❌ Failed to create configuration")
        return False
    
    # Step 4: Run scraper
    print_step(4, "Website Content Collection", 
               "Scraping content from realestateiot.com...")
    if not run_scraper():
        print("❌ Failed to scrape website content")
        return False
    
    # Step 5: Run chunker
    print_step(5, "Text Processing", 
               "Breaking content into chunks...")
    if not run_chunker():
        print("❌ Failed to process text chunks")
        return False
    
    # Step 6: Create vector store
    print_step(6, "Vector Database Creation", 
               "Creating searchable vector database...")
    if not run_vector_store():
        print("❌ Failed to create vector store")
        return False
    
    # Success message
    print("\n" + "🎉" * 20)
    print("SETUP COMPLETED SUCCESSFULLY!")
    print("🎉" * 20)
    
    print(f"""
✅ All components are ready!

Next steps:
1. (Optional) Add your OpenAI API key to .env file for better responses
2. Run the chatbot: python web_interface.py
3. Open your browser to: http://localhost:5000

Files created:
- data/scraped_content.json (website content)
- data/text_chunks.json (processed chunks)
- data/vector_store.* (searchable database)
- .env (configuration file)

The chatbot is ready to answer questions about Real Estate IoT!
""")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)
    else:
        print("\n✅ Setup completed successfully!")
        sys.exit(0)