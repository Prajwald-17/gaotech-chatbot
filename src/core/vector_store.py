import json
import numpy as np
import faiss
import pickle
from typing import List, Dict, Tuple
import openai
from sentence_transformers import SentenceTransformer
import os
from datetime import datetime

class VectorStore:
    def __init__(self, use_openai: bool = False, openai_api_key: str = None):
        self.use_openai = use_openai
        self.dimension = 384  # Default for sentence-transformers
        self.index = None
        self.chunks = []
        self.embeddings = []
        
        if use_openai and openai_api_key:
            openai.api_key = openai_api_key
            self.dimension = 1536  # OpenAI embedding dimension
            self.embedding_model = "text-embedding-ada-002"
        else:
            # Use free sentence-transformers model
            print("Loading sentence transformer model...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.dimension = 384
    
    def get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for a single text"""
        if self.use_openai:
            try:
                response = openai.Embedding.create(
                    model=self.embedding_model,
                    input=text
                )
                return np.array(response['data'][0]['embedding'], dtype=np.float32)
            except Exception as e:
                print(f"OpenAI embedding error: {e}")
                # Fallback to sentence transformer
                return self.model.encode([text])[0].astype(np.float32)
        else:
            return self.model.encode([text])[0].astype(np.float32)
    
    def get_embeddings_batch(self, texts: List[str], batch_size: int = 32) -> List[np.ndarray]:
        """Get embeddings for multiple texts"""
        embeddings = []
        
        if self.use_openai:
            # Process in batches for OpenAI API
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                try:
                    response = openai.Embedding.create(
                        model=self.embedding_model,
                        input=batch
                    )
                    batch_embeddings = [np.array(item['embedding'], dtype=np.float32) 
                                      for item in response['data']]
                    embeddings.extend(batch_embeddings)
                    print(f"Processed {min(i + batch_size, len(texts))}/{len(texts)} embeddings")
                except Exception as e:
                    print(f"OpenAI batch embedding error: {e}")
                    # Fallback to sentence transformer for this batch
                    batch_embeddings = self.model.encode(batch).astype(np.float32)
                    embeddings.extend(batch_embeddings)
        else:
            # Use sentence transformer for all
            print("Creating embeddings with sentence transformer...")
            embeddings = self.model.encode(texts, batch_size=batch_size, 
                                         show_progress_bar=True).astype(np.float32)
        
        return embeddings
    
    def create_index(self, chunks: List[Dict]):
        """Create FAISS index from chunks"""
        print("Creating vector index...")
        
        # Store chunks
        self.chunks = chunks
        
        # Extract texts for embedding
        texts = [chunk['text'] for chunk in chunks]
        
        # Get embeddings
        self.embeddings = self.get_embeddings_batch(texts)
        
        # Create FAISS index
        self.index = faiss.IndexFlatIP(self.dimension)  # Inner product (cosine similarity)
        
        # Normalize embeddings for cosine similarity
        embeddings_array = np.array(self.embeddings)
        faiss.normalize_L2(embeddings_array)
        
        # Add to index
        self.index.add(embeddings_array)
        
        print(f"Index created with {len(chunks)} chunks")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for similar chunks"""
        if self.index is None:
            raise ValueError("Index not created. Call create_index first.")
        
        # Get query embedding
        query_embedding = self.get_embedding(query)
        query_embedding = query_embedding.reshape(1, -1)
        
        # Normalize for cosine similarity
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding, top_k)
        
        # Return results with metadata
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx < len(self.chunks):  # Valid index
                result = self.chunks[idx].copy()
                result['similarity_score'] = float(score)
                result['rank'] = i + 1
                results.append(result)
        
        return results
    
    def save_index(self, base_filename: str = 'vector_store'):
        """Save the vector store to disk"""
        # Save FAISS index
        faiss.write_index(self.index, f"data/{base_filename}.faiss")
        
        # Save metadata
        metadata = {
            'chunks': self.chunks,
            'dimension': self.dimension,
            'use_openai': self.use_openai,
            'created_at': datetime.now().isoformat(),
            'total_chunks': len(self.chunks)
        }
        
        with open(f"data/{base_filename}_metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # Save embeddings
        with open(f"data/{base_filename}_embeddings.pkl", 'wb') as f:
            pickle.dump(self.embeddings, f)
        
        print(f"Vector store saved to data/{base_filename}.*")
    
    def load_index(self, base_filename: str = 'vector_store'):
        """Load the vector store from disk"""
        try:
            # Check if files exist first
            required_files = [
                f"data/{base_filename}.faiss",
                f"data/{base_filename}_metadata.json",
                f"data/{base_filename}_embeddings.pkl"
            ]
            
            for file_path in required_files:
                if not os.path.exists(file_path):
                    print(f"Vector store file not found: {file_path}")
                    return False
            
            # Load FAISS index
            self.index = faiss.read_index(f"data/{base_filename}.faiss")
            
            # Load metadata
            with open(f"data/{base_filename}_metadata.json", 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            self.chunks = metadata['chunks']
            self.dimension = metadata['dimension']
            
            # Load embeddings
            with open(f"data/{base_filename}_embeddings.pkl", 'rb') as f:
                self.embeddings = pickle.load(f)
            
            print(f"Vector store loaded: {len(self.chunks)} chunks")
            return True
            
        except (FileNotFoundError, RuntimeError, Exception) as e:
            print(f"Vector store loading failed: {e}")
            return False
    
    def load_chunks(self, filename: str = 'data/text_chunks.json') -> List[Dict]:
        """Load chunks from JSON file"""
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

def main():
    # Initialize vector store (using free model by default)
    # To use OpenAI, set: vector_store = VectorStore(use_openai=True, openai_api_key="your-key")
    vector_store = VectorStore(use_openai=False)
    
    # Try to load existing index
    if vector_store.load_index():
        print("Loaded existing vector store")
    else:
        # Create new index
        try:
            chunks = vector_store.load_chunks()
            print(f"Loaded {len(chunks)} chunks")
            
            vector_store.create_index(chunks)
            vector_store.save_index()
            
        except FileNotFoundError:
            print("Text chunks not found. Please run text_chunker.py first.")
            return
    
    # Test search
    print("\n" + "="*50)
    print("Testing vector search...")
    
    test_queries = [
        "What is Real Estate IoT?",
        "How does IoT help in real estate?",
        "What services do you offer?",
        "Smart building technology",
        "Property management solutions"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        results = vector_store.search(query, top_k=3)
        
        for i, result in enumerate(results):
            print(f"\n  Result {i+1} (Score: {result['similarity_score']:.3f}):")
            print(f"  Source: {result['source']['title']}")
            print(f"  URL: {result['source']['url']}")
            print(f"  Text: {result['text'][:200]}...")

if __name__ == "__main__":
    # Create data directory
    os.makedirs('data', exist_ok=True)
    main()