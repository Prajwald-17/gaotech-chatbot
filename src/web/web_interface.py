from flask import Flask, render_template, request, jsonify
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.core.chatbot_engine import ChatbotEngine
import json

app = Flask(__name__)

# Initialize chatbot
chatbot = None

def init_chatbot():
    """Initialize the chatbot engine"""
    global chatbot
    
    try:
        # Get OpenAI API key from environment variable if available
        openai_key = os.getenv('OPENAI_API_KEY')
        
        chatbot = ChatbotEngine(
            openai_api_key=openai_key,
            use_openai_embeddings=False,  # Use free embeddings by default
            model_name="gpt-3.5-turbo" if openai_key else "free"
        )
        print("Chatbot initialized successfully")
    except Exception as e:
        print(f"Error initializing chatbot: {e}")
        chatbot = None

@app.route('/')
def index():
    """Main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """Chat API endpoint"""
    try:
        data = request.get_json()
        query = data.get('message', '').strip()
        
        if not query:
            return jsonify({
                'error': 'Empty message',
                'status': 'error'
            }), 400
        
        # Get response from chatbot
        response = chatbot.chat(query, include_sources=True)
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/starters')
def get_starters():
    """Get conversation starters"""
    try:
        if chatbot:
            starters = chatbot.get_conversation_starter()
            return jsonify({'starters': starters})
        else:
            # Fallback starters if chatbot not initialized
            fallback_starters = [
                "What is Real Estate IoT and what do you do?",
                "What IoT solutions do you offer for buildings?",
                "What career opportunities are available?",
                "How can I contact Real Estate IoT?"
            ]
            return jsonify({'starters': fallback_starters})
    except Exception as e:
        return jsonify({'error': str(e), 'starters': []}), 500

@app.route('/api/status')
def get_status():
    """Get chatbot status"""
    try:
        return jsonify({
            'status': 'ready' if chatbot else 'error',
            'model': chatbot.model_name if chatbot else 'not initialized',
            'vector_store_loaded': bool(chatbot and hasattr(chatbot, 'vector_store') and chatbot.vector_store)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e),
            'model': 'not initialized',
            'vector_store_loaded': False
        })

# Initialize chatbot when module is imported (for gunicorn)
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

# Setup NLTK data if needed
try:
    import nltk
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except Exception as e:
    print(f"NLTK setup warning: {e}")

init_chatbot()

if __name__ == '__main__':
    print("Starting Real Estate IoT Chatbot Web Interface...")
    
    # Get port from environment variable
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"Visit: http://localhost:{port}")
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)