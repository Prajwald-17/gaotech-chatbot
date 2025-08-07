#!/usr/bin/env python3
"""
Rebuild vector store using lightweight dependencies
"""

import json
import os
from lightweight_vector_store import LightweightVectorStore

def main():
    print("Rebuilding vector store with lightweight dependencies...")
    
    # Load existing chunks
    chunks_file = "data/text_chunks.json"
    if not os.path.exists(chunks_file):
        print(f"Error: {chunks_file} not found!")
        return
    
    with open(chunks_file, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    
    print(f"Loaded {len(chunks)} text chunks")
    
    # Create lightweight vector store
    openai_key = os.getenv('OPENAI_API_KEY')
    use_openai = bool(openai_key)
    
    vector_store = LightweightVectorStore(
        use_openai=use_openai,
        openai_api_key=openai_key
    )
    
    # Build index
    vector_store.build_index(chunks)
    
    # Save index
    vector_store.save_index("data/vector_store")
    
    print("Lightweight vector store rebuilt successfully!")

if __name__ == "__main__":
    main()