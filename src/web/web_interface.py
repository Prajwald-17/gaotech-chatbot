from flask import Flask, render_template, request, jsonify, render_template_string
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.core.chatbot_engine import ChatbotEngine
import json

# Set template folder path
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
app = Flask(__name__, template_folder=template_dir)

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
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Template error: {e}")
        # Fallback to inline HTML
        return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GaoTech Intelligent Chatbot</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }
        .chat-container { background: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .chat-header { text-align: center; color: #2c3e50; margin-bottom: 20px; }
        .messages { height: 400px; overflow-y: auto; border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 5px; }
        .message { margin: 10px 0; padding: 10px; border-radius: 8px; }
        .user { background: #e3f2fd; text-align: right; }
        .bot { background: #f5f5f5; }
        .input-area { display: flex; gap: 10px; }
        input[type="text"] { flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 5px; }
        button { padding: 12px 20px; background: #2196f3; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #1976d2; }
        .starters { margin: 15px 0; }
        .starter-btn { display: inline-block; margin: 5px; padding: 8px 15px; background: #e8f4fd; border: 1px solid #2196f3; border-radius: 20px; cursor: pointer; font-size: 14px; }
        .starter-btn:hover { background: #2196f3; color: white; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>🏠 GaoTech Intelligent Chatbot</h1>
            <p>Ask me about Real Estate IoT solutions and smart building technologies</p>
        </div>
        
        <div class="starters" id="starters">
            <div class="starter-btn" onclick="sendMessage('What IoT solutions does GaoTech offer?')">What IoT solutions does GaoTech offer?</div>
            <div class="starter-btn" onclick="sendMessage('Tell me about smart building technologies')">Tell me about smart building technologies</div>
            <div class="starter-btn" onclick="sendMessage('How can GaoTech help with property management?')">How can GaoTech help with property management?</div>
        </div>
        
        <div class="messages" id="messages"></div>
        
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="Ask about GaoTech IoT solutions..." onkeypress="if(event.key==='Enter') sendMessage()">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        function sendMessage(text) {
            const input = document.getElementById('messageInput');
            const message = text || input.value.trim();
            if (!message) return;

            addMessage(message, 'user');
            if (!text) input.value = '';

            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                addMessage(data.response || data.answer || 'Sorry, I encountered an error.', 'bot');
            })
            .catch(error => {
                addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            });
        }

        function addMessage(text, sender) {
            const messages = document.getElementById('messages');
            const div = document.createElement('div');
            div.className = `message ${sender}`;
            div.textContent = text;
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }

        // Add welcome message
        addMessage('Hello! I\\'m the GaoTech chatbot. Ask me about our Real Estate IoT solutions and smart building technologies!', 'bot');
    </script>
</body>
</html>
        """)

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """Chat API endpoint"""
    try:
        data = request.get_json()
        query = data.get('message', '').strip()
        
        if not query:
            return jsonify({
                'response': 'Please enter a message.',
                'status': 'error'
            }), 400
        
        # Check if chatbot is initialized
        if not chatbot:
            return jsonify({
                'response': 'I apologize, but the chatbot service is currently initializing. Please try again in a moment.',
                'status': 'error'
            })
        
        # Get response from chatbot
        response = chatbot.chat(query, include_sources=True)
        
        # Ensure response has the right format
        if 'answer' in response and 'response' not in response:
            response['response'] = response['answer']
        
        # Make sure we have a response field
        if 'response' not in response:
            response['response'] = "I apologize, but I couldn't generate a proper response. Please try again."
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Chat API error: {e}")
        return jsonify({
            'response': 'I apologize, but I encountered an error. Please try again.',
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/debug', methods=['POST'])
def debug_chat():
    """Debug chat endpoint"""
    try:
        data = request.get_json()
        query = data.get('message', 'test')
        
        debug_info = {
            'chatbot_initialized': chatbot is not None,
            'query_received': query,
            'chatbot_type': str(type(chatbot)) if chatbot else None
        }
        
        if chatbot:
            try:
                # Test vector store
                context = chatbot.retrieve_context(query, top_k=2)
                debug_info['context_chunks'] = len(context)
                debug_info['context_sample'] = context[:1] if context else []
                
                # Test response generation
                response = chatbot.generate_answer_free(query, context)
                debug_info['response_keys'] = list(response.keys())
                debug_info['response'] = response
                
            except Exception as e:
                debug_info['error'] = str(e)
        
        return jsonify(debug_info)
        
    except Exception as e:
        return jsonify({'error': str(e)})

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
try:
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
except:
    pass

init_chatbot()

if __name__ == '__main__':
    print("Starting Real Estate IoT Chatbot Web Interface...")
    
    # Get port from environment variable
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"Visit: http://localhost:{port}")
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)