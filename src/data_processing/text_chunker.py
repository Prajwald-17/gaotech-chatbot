import json
import re
from typing import List, Dict
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import os

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class TextChunker:
    def __init__(self, chunk_size: int = 400, overlap: int = 50):
        self.chunk_size = chunk_size  # Target words per chunk
        self.overlap = overlap  # Overlapping words between chunks
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:()\-\'""]', ' ', text)
        # Remove extra spaces
        text = ' '.join(text.split())
        return text.strip()
    
    def split_by_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        try:
            sentences = sent_tokenize(text)
            return [s.strip() for s in sentences if s.strip()]
        except:
            # Fallback to simple splitting if NLTK fails
            sentences = re.split(r'[.!?]+', text)
            return [s.strip() for s in sentences if s.strip()]
    
    def count_words(self, text: str) -> int:
        """Count words in text"""
        return len(text.split())
    
    def create_chunks_from_text(self, text: str, source_info: Dict) -> List[Dict]:
        """Create chunks from a single text"""
        cleaned_text = self.clean_text(text)
        sentences = self.split_by_sentences(cleaned_text)
        
        chunks = []
        current_chunk = []
        current_word_count = 0
        
        for sentence in sentences:
            sentence_word_count = self.count_words(sentence)
            
            # If adding this sentence would exceed chunk size, finalize current chunk
            if current_word_count + sentence_word_count > self.chunk_size and current_chunk:
                chunk_text = ' '.join(current_chunk)
                chunks.append({
                    'text': chunk_text,
                    'word_count': current_word_count,
                    'source': source_info,
                    'chunk_id': len(chunks)
                })
                
                # Start new chunk with overlap
                if self.overlap > 0 and len(current_chunk) > 1:
                    # Keep last few sentences for overlap
                    overlap_sentences = []
                    overlap_words = 0
                    for i in range(len(current_chunk) - 1, -1, -1):
                        sentence_words = self.count_words(current_chunk[i])
                        if overlap_words + sentence_words <= self.overlap:
                            overlap_sentences.insert(0, current_chunk[i])
                            overlap_words += sentence_words
                        else:
                            break
                    
                    current_chunk = overlap_sentences
                    current_word_count = overlap_words
                else:
                    current_chunk = []
                    current_word_count = 0
            
            current_chunk.append(sentence)
            current_word_count += sentence_word_count
        
        # Add the last chunk if it has content
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                'text': chunk_text,
                'word_count': current_word_count,
                'source': source_info,
                'chunk_id': len(chunks)
            })
        
        return chunks
    
    def chunk_scraped_content(self, scraped_content: List[Dict]) -> List[Dict]:
        """Process all scraped content and create chunks"""
        all_chunks = []
        
        for page in scraped_content:
            if page['status'] != 'success':
                continue
            
            content = page['content']
            source_info = {
                'url': page['url'],
                'title': content['title'],
                'description': content['description'],
                'headings': content['headings']
            }
            
            # Create chunks from main content
            if content['content']:
                chunks = self.create_chunks_from_text(content['content'], source_info)
                all_chunks.extend(chunks)
            
            # Create chunks from headings if they contain substantial content
            headings_text = ' '.join(content['headings'])
            if headings_text and len(headings_text.split()) > 10:
                heading_source = source_info.copy()
                heading_source['content_type'] = 'headings'
                heading_chunks = self.create_chunks_from_text(headings_text, heading_source)
                all_chunks.extend(heading_chunks)
        
        # Add global chunk IDs
        for i, chunk in enumerate(all_chunks):
            chunk['global_chunk_id'] = i
        
        return all_chunks
    
    def save_chunks(self, chunks: List[Dict], filename: str = 'text_chunks.json'):
        """Save chunks to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        print(f"Chunks saved to {filename}")
    
    def load_scraped_content(self, filename: str = 'data/scraped_content.json') -> List[Dict]:
        """Load scraped content from JSON file"""
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

def main():
    # Create chunker
    chunker = TextChunker(chunk_size=400, overlap=50)
    
    # Load scraped content
    try:
        scraped_content = chunker.load_scraped_content()
        print(f"Loaded {len(scraped_content)} scraped pages")
    except FileNotFoundError:
        print("Scraped content not found. Please run website_scraper.py first.")
        return
    
    # Create chunks
    chunks = chunker.chunk_scraped_content(scraped_content)
    
    print(f"\nChunking completed!")
    print(f"Total chunks created: {len(chunks)}")
    
    # Save chunks
    chunker.save_chunks(chunks, 'data/text_chunks.json')
    
    # Print summary statistics
    word_counts = [chunk['word_count'] for chunk in chunks]
    avg_words = sum(word_counts) / len(word_counts) if word_counts else 0
    
    print(f"\nChunk Statistics:")
    print(f"Average words per chunk: {avg_words:.1f}")
    print(f"Min words: {min(word_counts) if word_counts else 0}")
    print(f"Max words: {max(word_counts) if word_counts else 0}")
    
    # Show sample chunks
    print(f"\nSample chunks:")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\nChunk {i+1} (from {chunk['source']['title']}):")
        print(f"Words: {chunk['word_count']}")
        print(f"Text preview: {chunk['text'][:200]}...")

if __name__ == "__main__":
    main()