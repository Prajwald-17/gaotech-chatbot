#!/usr/bin/env python3
"""
Minimal Test Entry Point for Vercel
===================================

This is a minimal version to test if basic Flask works on Vercel.
"""

from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GaoTech Chatbot - Test</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .chat-container { border: 1px solid #ddd; border-radius: 8px; padding: 20px; }
        .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .user { background-color: #e3f2fd; text-align: right; }
        .bot { background-color: #f5f5f5; }
        input[type="text"] { width: 70%; padding: 10px; }
        button { padding: 10px 20px; background-color: #2196f3; color: white; border: none; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>🏠 GaoTech Intelligent Chatbot - Test Version</h1>
    <div class="chat-container">
        <div id="messages"></div>
        <div style="margin-top: 20px;">
            <input type="text" id="messageInput" placeholder="Ask about GaoTech IoT solutions..." onkeypress="if(event.key==='Enter') sendMessage()">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;

            // Add user message
            addMessage(message, 'user');
            input.value = '';

            // Send to API
            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                addMessage(data.response || 'Sorry, I encountered an error.', 'bot');
            })
            .catch(error => {
                addMessage('Sorry, I encountered an error.', 'bot');
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
        addMessage('Hello! I\\'m the GaoTech chatbot. Ask me about our IoT solutions!', 'bot');
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def status():
    """Status endpoint"""
    return jsonify({
        "status": "success",
        "message": "GaoTech Chatbot is running",
        "version": "test-1.0"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Simple chat endpoint"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower()
        
        # Simple keyword-based responses
        if 'iot' in user_message or 'sensor' in user_message:
            response = "GaoTech provides advanced IoT solutions including smart sensors, automated systems, and energy management for buildings. Our IoT technology helps optimize building performance and reduce costs."
        elif 'smart building' in user_message or 'building' in user_message:
            response = "Our smart building solutions include automated lighting, HVAC control, security systems, and energy monitoring. We help transform traditional buildings into intelligent, efficient spaces."
        elif 'contact' in user_message or 'reach' in user_message:
            response = "You can contact GaoTech for more information about our solutions. We're here to help with all your real estate IoT needs!"
        elif 'service' in user_message or 'what do you do' in user_message:
            response = "GaoTech specializes in Real Estate IoT solutions, smart building technologies, property management systems, and comprehensive technology services for the real estate industry."
        elif 'hello' in user_message or 'hi' in user_message:
            response = "Hello! Welcome to GaoTech. I'm here to help you learn about our Real Estate IoT solutions and smart building technologies. What would you like to know?"
        else:
            response = "Thank you for your question! GaoTech is a leading provider of Real Estate IoT solutions and smart building technologies. We offer comprehensive services including smart sensors, automated systems, and property management solutions. How can I help you learn more about our services?"
        
        return jsonify({
            "response": response,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "response": "I apologize, but I'm experiencing technical difficulties. Please try again later.",
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/api/starters')
def starters():
    """Conversation starters"""
    return jsonify({
        "starters": [
            "What IoT solutions does GaoTech offer?",
            "Tell me about smart building technologies",
            "How can GaoTech help with property management?",
            "What are the benefits of IoT in real estate?"
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)