import json
import numpy as np
import pickle
from typing import List, Dict, Tuple
import openai
import os
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class LightweightVectorStore:
    def __init__(self, use_openai: bool = False, openai_api_key: str = None):
        self.use_openai = use_openai
        self.chunks = []
        self.embeddings = []
        self.vectorizer = None
        
        if use_openai and openai_api_key:
            self.client = openai.OpenAI(api_key=openai_api_key)
            self.embedding_model = "text-embedding-3-small"
        else:
            # Use TF-IDF as lightweight alternative
            print("Using TF-IDF vectorization (lightweight alternative)")
            self.vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2),
                lowercase=True
            )
    
    def get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for a single text"""
        if self.use_openai:
            try:
                response = self.client.embeddings.create(
                    model=self.embedding_model,
                    input=text
                )
                return np.array(response.data[0].embedding, dtype=np.float32)
            except Exception as e:
                print(f"OpenAI embedding error: {e}")
                return self._get_tfidf_embedding(text)
        else:
            return self._get_tfidf_embedding(text)
    
    def _get_tfidf_embedding(self, text: str) -> np.ndarray:
        """Get TF-IDF embedding for text"""
        if self.vectorizer is None:
            print("Warning: Vectorizer not loaded, using zero vector")
            return np.zeros(1000, dtype=np.float32)
        
        try:
            # Check if vectorizer is fitted
            if not hasattr(self.vectorizer, 'idf_'):
                print("Warning: Vectorizer not fitted, using zero vector")
                return np.zeros(1000, dtype=np.float32)
            
            # Transform single text
            embedding = self.vectorizer.transform([text]).toarray()[0]
            return embedding.astype(np.float32)
        except Exception as e:
            print(f"TF-IDF embedding error: {e}")
            return np.zeros(1000, dtype=np.float32)
    
    def build_index(self, chunks: List[Dict]):
        """Build the vector index from text chunks"""
        print(f"Building lightweight vector index for {len(chunks)} chunks...")
        
        self.chunks = chunks
        texts = [chunk.get('content', chunk.get('text', '')) for chunk in chunks]
        
        if self.use_openai:
            # Use OpenAI embeddings
            self.embeddings = []
            for i, text in enumerate(texts):
                if i % 10 == 0:
                    print(f"Processing chunk {i+1}/{len(texts)}")
                embedding = self.get_embedding(text)
                self.embeddings.append(embedding)
            self.embeddings = np.array(self.embeddings)
        else:
            # Use TF-IDF
            print("Fitting TF-IDF vectorizer...")
            self.embeddings = self.vectorizer.fit_transform(texts).toarray()
            self.embeddings = self.embeddings.astype(np.float32)
        
        print(f"Vector index built with shape: {self.embeddings.shape}")
        return True
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for similar chunks"""
        if len(self.chunks) == 0 or len(self.embeddings) == 0:
            return []
        
        try:
            # Get query embedding
            query_embedding = self.get_embedding(query)
            
            # If embedding is all zeros (vectorizer not working), do simple text matching
            if np.all(query_embedding == 0):
                print("Using fallback text matching")
                return self._fallback_text_search(query, top_k)
            
            if len(query_embedding.shape) == 1:
                query_embedding = query_embedding.reshape(1, -1)
            
            # Calculate similarities
            similarities = cosine_similarity(query_embedding, self.embeddings)[0]
            
            # Get top k results
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.1:  # Minimum similarity threshold
                    result = self.chunks[idx].copy()
                    result['similarity'] = float(similarities[idx])
                    results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Search error: {e}")
            return self._fallback_text_search(query, top_k)
    
    def _fallback_text_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Fallback text search using simple keyword matching"""
        query_words = set(query.lower().split())
        results = []
        
        for chunk in self.chunks:
            text = chunk.get('content', chunk.get('text', '')).lower()
            text_words = set(text.split())
            
            # Calculate simple word overlap score
            overlap = len(query_words.intersection(text_words))
            if overlap > 0:
                result = chunk.copy()
                result['similarity'] = overlap / len(query_words)
                results.append(result)
        
        # Sort by similarity and return top k
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]
    
    def save_index(self, base_path: str = "data/vector_store"):
        """Save the vector index"""
        try:
            os.makedirs(os.path.dirname(base_path), exist_ok=True)
            
            # Save chunks
            with open(f"{base_path}_chunks.json", 'w', encoding='utf-8') as f:
                json.dump(self.chunks, f, ensure_ascii=False, indent=2)
            
            # Save embeddings
            with open(f"{base_path}_embeddings.pkl", 'wb') as f:
                pickle.dump(self.embeddings, f)
            
            # Save vectorizer if using TF-IDF
            if not self.use_openai and self.vectorizer:
                with open(f"{base_path}_vectorizer.pkl", 'wb') as f:
                    pickle.dump(self.vectorizer, f)
            
            # Save metadata
            metadata = {
                'use_openai': self.use_openai,
                'num_chunks': len(self.chunks),
                'embedding_shape': self.embeddings.shape if len(self.embeddings) > 0 else None,
                'created_at': datetime.now().isoformat()
            }
            
            with open(f"{base_path}_metadata.json", 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"Vector store saved to {base_path}")
            return True
            
        except Exception as e:
            print(f"Error saving vector store: {e}")
            return False
    
    def load_index(self, base_path: str = "data/vector_store") -> bool:
        """Load the vector index"""
        try:
            # Load chunks
            chunks_path = f"{base_path}_chunks.json"
            if not os.path.exists(chunks_path):
                print(f"Chunks file not found: {chunks_path}")
                return False
                
            with open(chunks_path, 'r', encoding='utf-8') as f:
                self.chunks = json.load(f)
            
            # Load embeddings
            embeddings_path = f"{base_path}_embeddings.pkl"
            if not os.path.exists(embeddings_path):
                print(f"Embeddings file not found: {embeddings_path}")
                return False
                
            with open(embeddings_path, 'rb') as f:
                self.embeddings = pickle.load(f)
            
            # Load vectorizer if using TF-IDF
            if not self.use_openai:
                vectorizer_path = f"{base_path}_vectorizer.pkl"
                vectorizer_loaded = False
                
                # Try to load existing vectorizer
                if os.path.exists(vectorizer_path):
                    try:
                        with open(vectorizer_path, 'rb') as f:
                            self.vectorizer = pickle.load(f)
                        
                        # Check if vectorizer is properly fitted
                        if hasattr(self.vectorizer, 'idf_'):
                            print("TF-IDF vectorizer loaded successfully")
                            vectorizer_loaded = True
                        else:
                            print("Loaded vectorizer is not fitted")
                    except Exception as e:
                        print(f"Error loading vectorizer: {e}")
                
                # Rebuild vectorizer if loading failed or not fitted
                if not vectorizer_loaded and len(self.chunks) > 0:
                    print("Rebuilding vectorizer from chunks...")
                    texts = [chunk.get('content', chunk.get('text', '')) for chunk in self.chunks]
                    self.vectorizer = TfidfVectorizer(
                        max_features=1000,
                        stop_words='english',
                        ngram_range=(1, 2),
                        lowercase=True
                    )
                    self.vectorizer.fit(texts)
                    print("Vectorizer rebuilt successfully")
                    
                    # Save the rebuilt vectorizer
                    try:
                        with open(vectorizer_path, 'wb') as f:
                            pickle.dump(self.vectorizer, f)
                        print("Rebuilt vectorizer saved")
                    except Exception as e:
                        print(f"Warning: Could not save rebuilt vectorizer: {e}")
            
            print(f"Vector store loaded: {len(self.chunks)} chunks, embeddings shape: {self.embeddings.shape}")
            return True
            
        except Exception as e:
            print(f"Error loading vector store: {e}")
            return False