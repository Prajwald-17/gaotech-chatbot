import json
import re
import os
from typing import List, Dict, Tuple
from collections import Counter
import math

class SimpleVectorStore:
    """
    Ultra-lightweight vector store using simple text matching
    No external ML dependencies required
    """
    
    def __init__(self):
        self.chunks = []
        self.processed_chunks = []
        
    def preprocess_text(self, text: str) -> List[str]:
        """Simple text preprocessing"""
        # Convert to lowercase and remove special characters
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())
        # Split into words and remove empty strings
        words = [word for word in text.split() if len(word) > 2]
        return words
    
    def calculate_similarity(self, query_words: List[str], chunk_words: List[str]) -> float:
        """Calculate simple word overlap similarity"""
        if not query_words or not chunk_words:
            return 0.0
        
        # Count word frequencies
        query_counter = Counter(query_words)
        chunk_counter = Counter(chunk_words)
        
        # Calculate intersection
        intersection = sum((query_counter & chunk_counter).values())
        
        # Calculate union
        union = sum((query_counter | chunk_counter).values())
        
        # Jaccard similarity
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def add_chunks(self, chunks: List[Dict]):
        """Add text chunks to the store"""
        self.chunks = chunks
        self.processed_chunks = []
        
        for chunk in chunks:
            processed_text = self.preprocess_text(chunk.get('content', ''))
            self.processed_chunks.append({
                'words': processed_text,
                'original': chunk
            })
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for similar chunks"""
        if not self.processed_chunks:
            return []
        
        query_words = self.preprocess_text(query)
        if not query_words:
            return []
        
        # Calculate similarities
        similarities = []
        for i, processed_chunk in enumerate(self.processed_chunks):
            similarity = self.calculate_similarity(query_words, processed_chunk['words'])
            similarities.append((similarity, i))
        
        # Sort by similarity (descending)
        similarities.sort(reverse=True)
        
        # Return top_k results
        results = []
        for similarity, idx in similarities[:top_k]:
            if similarity > 0:  # Only return chunks with some similarity
                chunk = self.processed_chunks[idx]['original'].copy()
                chunk['similarity'] = similarity
                results.append(chunk)
        
        return results
    
    def load_index(self, data_dir: str = "data") -> bool:
        """Load chunks from JSON file"""
        try:
            # Try different possible paths
            possible_paths = [
                os.path.join(data_dir, "text_chunks.json"),
                os.path.join(os.path.dirname(__file__), "..", "..", data_dir, "text_chunks.json"),
                os.path.join(os.getcwd(), data_dir, "text_chunks.json")
            ]
            
            for chunks_file in possible_paths:
                if os.path.exists(chunks_file):
                    with open(chunks_file, 'r', encoding='utf-8') as f:
                        chunks = json.load(f)
                    self.add_chunks(chunks)
                    print(f"Loaded {len(chunks)} chunks from {chunks_file}")
                    return True
            
            # If no file found, create some default chunks
            print("No chunks file found, using default content")
            self._create_default_chunks()
            return True
            
        except Exception as e:
            print(f"Error loading chunks: {e}")
            # Create default chunks as fallback
            self._create_default_chunks()
            return True
    
    def _create_default_chunks(self):
        """Create default chunks if no data file is found"""
        default_chunks = [
            {
                "content": "GaoTech is a leading provider of Real Estate IoT solutions and smart building technologies.",
                "source": {"title": "About GaoTech", "url": "https://gaotech.com/about"}
            },
            {
                "content": "Our IoT solutions include smart sensors, automated systems, and energy management for buildings.",
                "source": {"title": "IoT Solutions", "url": "https://gaotech.com/solutions"}
            },
            {
                "content": "We provide comprehensive real estate technology services including property management systems.",
                "source": {"title": "Services", "url": "https://gaotech.com/services"}
            },
            {
                "content": "Contact us for more information about our smart building solutions and IoT implementations.",
                "source": {"title": "Contact", "url": "https://gaotech.com/contact"}
            }
        ]
        self.add_chunks(default_chunks)
        print(f"Created {len(default_chunks)} default chunks")
    
    def save_index(self, data_dir: str = "data"):
        """Save chunks to JSON file"""
        try:
            os.makedirs(data_dir, exist_ok=True)
            chunks_file = os.path.join(data_dir, "text_chunks.json")
            with open(chunks_file, 'w', encoding='utf-8') as f:
                json.dump(self.chunks, f, indent=2, ensure_ascii=False)
            print(f"Saved {len(self.chunks)} chunks to {chunks_file}")
        except Exception as e:
            print(f"Error saving chunks: {e}")