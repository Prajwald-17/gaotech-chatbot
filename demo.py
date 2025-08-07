#!/usr/bin/env python3
"""
Demo script for Real Estate IoT Chatbot
This script demonstrates the complete chatbot functionality with sample queries.
"""

from chatbot_engine import ChatbotEngine
import json
from datetime import datetime

def print_separator(title=""):
    """Print a nice separator"""
    if title:
        print(f"\n{'='*20} {title} {'='*20}")
    else:
        print("="*60)

def demo_chatbot():
    """Demonstrate the chatbot with sample queries"""
    
    print("🏠 Real Estate IoT Chatbot Demo")
    print_separator()
    
    # Initialize chatbot
    print("🔧 Initializing chatbot...")
    chatbot = ChatbotEngine()
    
    # Sample queries that demonstrate different aspects
    demo_queries = [
        {
            "query": "What is Real Estate IoT?",
            "description": "Basic information about the company/service"
        },
        {
            "query": "How does IoT help in property management?",
            "description": "Specific use case question"
        },
        {
            "query": "What smart building technologies do you offer?",
            "description": "Service-specific inquiry"
        },
        {
            "query": "How can IoT improve energy efficiency in buildings?",
            "description": "Technical benefits question"
        },
        {
            "query": "What are the benefits of HVAC automation?",
            "description": "Specific technology question"
        }
    ]
    
    print(f"🤖 Running {len(demo_queries)} demo queries...\n")
    
    results = []
    
    for i, demo in enumerate(demo_queries, 1):
        print_separator(f"Query {i}")
        print(f"📝 Question: {demo['query']}")
        print(f"💡 Type: {demo['description']}")
        print("\n🔍 Processing...")
        
        # Get response
        response = chatbot.chat(demo['query'], include_sources=True)
        
        print(f"\n🤖 Response:")
        print(f"{response['answer']}")
        
        # Show sources
        if response.get('sources'):
            print(f"\n📚 Sources ({len(response['sources'])} found):")
            for j, source in enumerate(response['sources'][:3], 1):
                print(f"  {j}. {source['title']}")
                print(f"     URL: {source['url']}")
        
        # Show metadata
        print(f"\n📊 Metadata:")
        print(f"  Model: {response.get('model', 'N/A')}")
        print(f"  Context chunks: {response.get('context_chunks_count', 0)}")
        print(f"  Timestamp: {response.get('timestamp', 'N/A')}")
        
        results.append(response)
        print("\n" + "-"*60)
    
    # Summary
    print_separator("Demo Summary")
    print(f"✅ Successfully processed {len(results)} queries")
    print(f"🎯 All responses generated using website content")
    print(f"📊 Average context chunks per query: {sum(r.get('context_chunks_count', 0) for r in results) / len(results):.1f}")
    
    # Show conversation starters
    print(f"\n💡 Additional conversation starters:")
    starters = chatbot.get_conversation_starter()
    for i, starter in enumerate(starters[:5], 1):
        print(f"  {i}. {starter}")
    
    print(f"\n🌐 Web interface available at: http://localhost:5000")
    print(f"🚀 The chatbot is ready for real-time conversations!")

def show_system_info():
    """Show information about the system components"""
    
    print_separator("System Information")
    
    # Check data files
    import os
    data_files = [
        ('data/scraped_content.json', 'Website content'),
        ('data/text_chunks.json', 'Text chunks'),
        ('data/vector_store.faiss', 'Vector index'),
        ('data/vector_store_metadata.json', 'Metadata'),
        ('data/vector_store_embeddings.pkl', 'Embeddings')
    ]
    
    print("📁 Data Files:")
    for file_path, description in data_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"  ✅ {description}: {file_path} ({size:,} bytes)")
        else:
            print(f"  ❌ {description}: {file_path} (missing)")
    
    # Load and show content stats
    try:
        with open('data/scraped_content.json', 'r', encoding='utf-8') as f:
            scraped_data = json.load(f)
        
        with open('data/text_chunks.json', 'r', encoding='utf-8') as f:
            chunks_data = json.load(f)
        
        print(f"\n📊 Content Statistics:")
        print(f"  Pages scraped: {len(scraped_data)}")
        print(f"  Text chunks created: {len(chunks_data)}")
        
        if chunks_data:
            word_counts = [chunk.get('word_count', 0) for chunk in chunks_data]
            print(f"  Average words per chunk: {sum(word_counts) / len(word_counts):.1f}")
            print(f"  Total words processed: {sum(word_counts):,}")
        
        # Show sample content
        if scraped_data:
            sample_page = scraped_data[0]
            if sample_page.get('status') == 'success':
                content = sample_page.get('content', {})
                print(f"\n📄 Sample Page:")
                print(f"  Title: {content.get('title', 'N/A')}")
                print(f"  URL: {sample_page.get('url', 'N/A')}")
                print(f"  Content preview: {content.get('content', '')[:200]}...")
    
    except Exception as e:
        print(f"❌ Error loading content stats: {e}")

def main():
    """Main demo function"""
    
    # Show system info first
    show_system_info()
    
    # Run chatbot demo
    demo_chatbot()
    
    print(f"\n🎉 Demo completed successfully!")
    print(f"💡 To interact with the chatbot:")
    print(f"   1. Web interface: http://localhost:5000")
    print(f"   2. Command line: python chatbot_engine.py")
    print(f"   3. Quick start: python start.py")

if __name__ == "__main__":
    main()