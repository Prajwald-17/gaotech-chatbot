import json
from typing import List, Dict, Optional
from .lightweight_vector_store import LightweightVectorStore
import openai
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ChatbotEngine:
    def __init__(self, 
                 openai_api_key: Optional[str] = None,
                 use_openai_embeddings: bool = False,
                 model_name: str = "gpt-3.5-turbo"):
        
        # Use provided key or load from environment
        if not openai_api_key:
            openai_api_key = os.getenv('OPENAI_API_KEY')
        
        self.vector_store = LightweightVectorStore(use_openai=use_openai_embeddings, 
                                                 openai_api_key=openai_api_key)
        self.openai_api_key = openai_api_key
        self.model_name = model_name
        
        # Load vector store
        if not self.vector_store.load_index():
            print("Warning: Vector store not found. Please run the setup process first.")
        
        # Set up OpenAI if key provided
        if openai_api_key:
            self.use_openai = True
            print(f"OpenAI API key loaded. Using {model_name} for responses.")
        else:
            self.use_openai = False
            print("No OpenAI API key provided. Using free alternatives.")
    
    def retrieve_context(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve relevant context from vector store"""
        try:
            results = self.vector_store.search(query, top_k=top_k)
            return results
        except Exception as e:
            print(f"Error retrieving context: {e}")
            return []
    
    def build_prompt(self, query: str, context_chunks: List[Dict]) -> str:
        """Build the prompt for the language model"""
        
        # System prompt
        system_prompt = """You are a helpful AI assistant for Real Estate IoT website (www.realestateiot.com). 
You provide accurate information based on the website content provided below. 

Guidelines:
- Answer questions based ONLY on the provided context
- If the context doesn't contain relevant information, say so politely
- Be helpful, professional, and concise
- Include specific details when available
- If asked about services, pricing, or contact information, refer to the website content
- Always maintain a professional tone suitable for real estate and IoT industry"""
        
        # Build context from retrieved chunks
        context_text = ""
        for i, chunk in enumerate(context_chunks):
            source_info = f"Source: {chunk['source']['title']} ({chunk['source']['url']})"
            context_text += f"\n--- Context {i+1} ---\n{source_info}\n{chunk['text']}\n"
        
        # Build final prompt
        prompt = f"""{system_prompt}

WEBSITE CONTENT:
{context_text}

USER QUESTION: {query}

ANSWER (based on the website content above):"""
        
        return prompt
    
    def generate_answer_openai(self, prompt: str) -> Dict:
        """Generate answer using OpenAI API"""
        try:
            client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content.strip()
            
            return {
                'answer': answer,
                'model': self.model_name,
                'status': 'success',
                'tokens_used': response.usage.total_tokens
            }
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return {
                'answer': f"I apologize, but I'm having trouble generating a response right now. Error: {str(e)}",
                'model': self.model_name,
                'status': 'error',
                'error': str(e)
            }
    
    def generate_answer_free(self, query: str, context_chunks: List[Dict]) -> Dict:
        """Generate answer using free alternatives (template-based)"""
        
        # Simple template-based response for free version
        if not context_chunks:
            return {
                'answer': "I don't have specific information about that topic in my knowledge base. Please visit realestateiot.com for more details or contact them directly.",
                'model': 'template-based',
                'status': 'success'
            }
        
        # Extract the query to provide more targeted responses
        query_lower = query.lower()
        
        # Extract key information from context
        relevant_info = []
        sources = set()
        
        for chunk in context_chunks:
            relevant_info.append(chunk['text'])
            sources.add(chunk['source']['url'])
        
        # Build more intelligent template response based on query type
        answer = self._build_contextual_answer(query_lower, relevant_info, sources)
        
        return {
            'answer': answer,
            'model': 'template-based',
            'status': 'success'
        }
    
    def _build_contextual_answer(self, query_lower: str, relevant_info: List[str], sources: set) -> str:
        """Build a contextual answer based on the query type"""
        
        # Combine all relevant information
        full_context = " ".join(relevant_info)
        
        # Extract key sentences based on query keywords
        key_sentences = []
        
        # Split context into sentences
        sentences = full_context.split('. ')
        
        # Define keyword categories
        keywords_map = {
            'what is': ['Real Estate IoT', 'company', 'about', 'services'],
            'how does': ['work', 'function', 'operate', 'help'],
            'benefits': ['benefit', 'advantage', 'improve', 'efficiency'],
            'hvac': ['HVAC', 'heating', 'cooling', 'climate', 'temperature'],
            'lighting': ['lighting', 'light', 'illumination', 'LED'],
            'security': ['security', 'surveillance', 'CCTV', 'alarm', 'intrusion'],
            'energy': ['energy', 'power', 'consumption', 'efficiency', 'monitoring'],
            'smart': ['smart', 'IoT', 'automation', 'technology'],
            'career': ['career', 'job', 'internship', 'opportunity', 'position'],
            'contact': ['contact', 'reach', 'phone', 'email', 'address']
        }
        
        # Find relevant sentences based on query
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for category, keywords in keywords_map.items():
                if any(keyword.lower() in query_lower for keyword in keywords):
                    if any(keyword.lower() in sentence_lower for keyword in keywords):
                        key_sentences.append(sentence.strip())
                        break
        
        # If no specific matches, use first few sentences
        if not key_sentences:
            key_sentences = sentences[:3]
        
        # Remove duplicates and empty sentences
        key_sentences = list(dict.fromkeys([s for s in key_sentences if s.strip()]))
        
        # Build answer
        if 'what is' in query_lower or 'about' in query_lower:
            answer = "Real Estate IoT is a company that specializes in smart building solutions. "
        elif 'how' in query_lower:
            answer = "Here's how it works: "
        elif 'benefit' in query_lower:
            answer = "The key benefits include: "
        elif 'career' in query_lower or 'job' in query_lower:
            answer = "Regarding career opportunities: "
        elif 'contact' in query_lower:
            answer = "To contact Real Estate IoT: "
        else:
            answer = "Based on Real Estate IoT's website: "
        
        # Add the most relevant information
        if key_sentences:
            answer += key_sentences[0]
            if len(key_sentences) > 1:
                answer += f" {key_sentences[1]}"
        
        # Add sources
        if sources:
            source_list = list(sources)[:2]
            answer += f"\n\nFor more information, visit: {', '.join(source_list)}"
        
        return answer
    
    def chat(self, query: str, include_sources: bool = True) -> Dict:
        """Main chat function"""
        
        # Retrieve relevant context
        context_chunks = self.retrieve_context(query, top_k=5)
        
        # Build prompt
        prompt = self.build_prompt(query, context_chunks)
        
        # Generate answer
        if self.use_openai:
            result = self.generate_answer_openai(prompt)
        else:
            result = self.generate_answer_free(query, context_chunks)
        
        # Add metadata
        result.update({
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'context_chunks_count': len(context_chunks),
            'sources': [chunk['source'] for chunk in context_chunks] if include_sources else []
        })
        
        return result
    
    def get_conversation_starter(self) -> List[str]:
        """Get suggested conversation starters based on website content"""
        return [
            "What is Real Estate IoT and what do you do?",
            "What IoT solutions do you offer for buildings?",
            "What career opportunities are available?",
            "How can I contact Real Estate IoT?"
        ]

def main():
    """Test the chatbot engine"""
    
    # Initialize chatbot (without OpenAI key for free version)
    # To use OpenAI: chatbot = ChatbotEngine(openai_api_key="your-key-here")
    chatbot = ChatbotEngine()
    
    print("Real Estate IoT Chatbot")
    print("=" * 50)
    
    # Show conversation starters
    starters = chatbot.get_conversation_starter()
    print("\nSuggested questions:")
    for i, starter in enumerate(starters[:5], 1):
        print(f"{i}. {starter}")
    
    print("\nType 'quit' to exit, 'starters' to see suggestions again")
    print("-" * 50)
    
    # Chat loop
    while True:
        query = input("\nYou: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if query.lower() == 'starters':
            print("\nSuggested questions:")
            for i, starter in enumerate(starters, 1):
                print(f"{i}. {starter}")
            continue
        
        if not query:
            continue
        
        print("\nBot: Thinking...")
        
        # Get response
        response = chatbot.chat(query, include_sources=True)
        
        print(f"\nBot: {response['answer']}")
        
        # Show sources if available
        if response.get('sources') and len(response['sources']) > 0:
            print(f"\nSources:")
            for i, source in enumerate(response['sources'][:3], 1):
                print(f"{i}. {source['title']} - {source['url']}")
        
        # Show metadata for debugging
        if response.get('model'):
            print(f"\n[Model: {response['model']}, Chunks: {response['context_chunks_count']}]")

if __name__ == "__main__":
    main()