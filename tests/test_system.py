#!/usr/bin/env python3
"""
Test script for the Real Estate IoT Chatbot system
This script tests each component to ensure everything is working correctly.
"""

import os
import sys
import json
from datetime import datetime

def test_file_exists(filepath, description):
    """Test if a file exists"""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description}: {filepath} (NOT FOUND)")
        return False

def test_import(module_name, description):
    """Test if a module can be imported"""
    try:
        __import__(module_name)
        print(f"✓ {description}: {module_name}")
        return True
    except ImportError as e:
        print(f"✗ {description}: {module_name} (IMPORT ERROR: {e})")
        return False

def test_data_file(filepath, description, min_size=0):
    """Test if a data file exists and has content"""
    if not os.path.exists(filepath):
        print(f"✗ {description}: {filepath} (NOT FOUND)")
        return False
    
    try:
        file_size = os.path.getsize(filepath)
        if file_size < min_size:
            print(f"✗ {description}: {filepath} (TOO SMALL: {file_size} bytes)")
            return False
        
        # Try to load JSON files
        if filepath.endswith('.json'):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    print(f"✓ {description}: {filepath} ({len(data)} items, {file_size} bytes)")
                else:
                    print(f"✓ {description}: {filepath} ({file_size} bytes)")
        else:
            print(f"✓ {description}: {filepath} ({file_size} bytes)")
        
        return True
        
    except Exception as e:
        print(f"✗ {description}: {filepath} (ERROR: {e})")
        return False

def test_vector_store():
    """Test vector store functionality"""
    try:
        from vector_store import VectorStore
        
        vs = VectorStore(use_openai=False)
        if vs.load_index():
            print("✓ Vector store: Loaded successfully")
            
            # Test search
            results = vs.search("What is IoT?", top_k=3)
            if results:
                print(f"✓ Vector search: Found {len(results)} results")
                return True
            else:
                print("✗ Vector search: No results found")
                return False
        else:
            print("✗ Vector store: Failed to load")
            return False
            
    except Exception as e:
        print(f"✗ Vector store test failed: {e}")
        return False

def test_chatbot_engine():
    """Test chatbot engine"""
    try:
        from chatbot_engine import ChatbotEngine
        
        chatbot = ChatbotEngine()
        response = chatbot.chat("What is Real Estate IoT?")
        
        if response and response.get('answer'):
            print("✓ Chatbot engine: Generated response successfully")
            print(f"  Sample response: {response['answer'][:100]}...")
            return True
        else:
            print("✗ Chatbot engine: Failed to generate response")
            return False
            
    except Exception as e:
        print(f"✗ Chatbot engine test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Real Estate IoT Chatbot System Test")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Core files exist
    print("\n📁 Testing Core Files:")
    files_to_test = [
        ('website_scraper.py', 'Website scraper'),
        ('text_chunker.py', 'Text chunker'),
        ('vector_store.py', 'Vector store'),
        ('chatbot_engine.py', 'Chatbot engine'),
        ('web_interface.py', 'Web interface'),
        ('requirements.txt', 'Requirements file'),
        ('templates/index.html', 'HTML template')
    ]
    
    for filepath, description in files_to_test:
        if test_file_exists(filepath, description):
            tests_passed += 1
        total_tests += 1
    
    # Test 2: Required modules can be imported
    print("\n📦 Testing Module Imports:")
    modules_to_test = [
        ('requests', 'HTTP requests'),
        ('bs4', 'BeautifulSoup'),
        ('nltk', 'Natural Language Toolkit'),
        ('numpy', 'NumPy'),
        ('faiss', 'FAISS vector search'),
        ('sentence_transformers', 'Sentence Transformers'),
        ('flask', 'Flask web framework')
    ]
    
    for module_name, description in modules_to_test:
        if test_import(module_name, description):
            tests_passed += 1
        total_tests += 1
    
    # Test 3: Data files exist and have content
    print("\n💾 Testing Data Files:")
    data_files_to_test = [
        ('data/scraped_content.json', 'Scraped website content', 1000),
        ('data/text_chunks.json', 'Text chunks', 1000),
        ('data/vector_store.faiss', 'FAISS index', 1000),
        ('data/vector_store_metadata.json', 'Vector store metadata', 100),
        ('data/vector_store_embeddings.pkl', 'Embeddings', 1000)
    ]
    
    for filepath, description, min_size in data_files_to_test:
        if test_data_file(filepath, description, min_size):
            tests_passed += 1
        total_tests += 1
    
    # Test 4: Vector store functionality
    print("\n🔍 Testing Vector Store:")
    if test_vector_store():
        tests_passed += 1
    total_tests += 1
    
    # Test 5: Chatbot engine
    print("\n🤖 Testing Chatbot Engine:")
    if test_chatbot_engine():
        tests_passed += 1
    total_tests += 1
    
    # Results
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    
    success_rate = (tests_passed / total_tests) * 100
    
    print(f"Tests passed: {tests_passed}/{total_tests} ({success_rate:.1f}%)")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED! System is ready to use.")
        print("\nNext steps:")
        print("1. Run: python web_interface.py")
        print("2. Open: http://localhost:5000")
        print("3. Start chatting!")
        return True
    else:
        print("❌ Some tests failed. Please check the issues above.")
        print("\nTo fix issues:")
        print("1. Run: python setup.py")
        print("2. Check that all dependencies are installed")
        print("3. Ensure data files were created properly")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)