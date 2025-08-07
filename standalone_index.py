#!/usr/bin/env python3
"""
Standalone GaoTech Chatbot
=========================

Self-contained version with all functionality in one file.
"""

from flask import Flask, render_template_string, request, jsonify
import os
import re
from collections import Counter
import json

app = Flask(__name__)

# Simple vector store class
class SimpleVectorStore:
    def __init__(self):
        self.chunks = []
        self.processed_chunks = []
        
    def preprocess_text(self, text):
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())
        words = [word for word in text.split() if len(word) > 2]
        return words
    
    def calculate_similarity(self, query_words, chunk_words):
        if not query_words or not chunk_words:
            return 0.0
        
        query_counter = Counter(query_words)
        chunk_counter = Counter(chunk_words)
        intersection = sum((query_counter & chunk_counter).values())
        union = sum((query_counter | chunk_counter).values())
        
        return intersection / union if union > 0 else 0.0
    
    def add_chunks(self, chunks):
        self.chunks = chunks
        self.processed_chunks = []
        
        for chunk in chunks:
            processed_text = self.preprocess_text(chunk.get('content', ''))
            self.processed_chunks.append({
                'words': processed_text,
                'original': chunk
            })
    
    def search(self, query, top_k=5):
        if not self.processed_chunks:
            return []
        
        query_words = self.preprocess_text(query)
        if not query_words:
            return []
        
        similarities = []
        for i, processed_chunk in enumerate(self.processed_chunks):
            similarity = self.calculate_similarity(query_words, processed_chunk['words'])
            similarities.append((similarity, i))
        
        similarities.sort(reverse=True)
        
        results = []
        for similarity, idx in similarities[:top_k]:
            if similarity > 0:
                chunk = self.processed_chunks[idx]['original'].copy()
                chunk['similarity'] = similarity
                results.append(chunk)
        
        return results

# Simple chatbot engine
class SimpleChatbotEngine:
    def __init__(self):
        self.vector_store = SimpleVectorStore()
        self._load_default_content()
        
    def _load_default_content(self):
        default_chunks = [
            {
                "content": "GaoTech is a leading provider of Real Estate IoT solutions and smart building technologies. We specialize in transforming traditional buildings into intelligent, connected spaces.",
                "source": {"title": "About GaoTech", "url": "https://gaotech.com/about"}
            },
            {
                "content": "GaoTech's comprehensive IoT solutions transform buildings into intelligent, connected environments. Our offerings include: Smart Environmental Sensors for real-time monitoring of temperature, humidity, air quality, and occupancy levels; Automated Lighting Systems with motion detection, daylight harvesting, and energy-efficient LED controls; Intelligent HVAC Control featuring zone-based climate management, predictive scheduling, and energy optimization; Advanced Security Monitoring with smart cameras, access control, intrusion detection, and mobile alerts; Energy Management Systems providing detailed consumption analytics, peak demand management, and automated load balancing; Water Management Solutions including leak detection, usage monitoring, and conservation automation. All systems integrate seamlessly through our centralized IoT platform, providing building owners with complete visibility and control while reducing operational costs by up to 35%.",
                "source": {"title": "IoT Solutions", "url": "https://gaotech.com/iot-solutions"}
            },
            {
                "content": "GaoTech's smart building technologies create intelligent, responsive environments that adapt to occupant needs while maximizing efficiency. Our comprehensive smart building solutions include: Automated Lighting Control with occupancy sensors, daylight harvesting, and circadian rhythm optimization; Intelligent HVAC Systems featuring predictive climate control, zone-based management, and air quality monitoring; Energy Optimization through real-time consumption tracking, demand response automation, and renewable energy integration; Advanced Security Integration combining access control, video surveillance, intrusion detection, and emergency response systems; Real-time Monitoring Dashboards providing building managers with comprehensive insights into all building systems; Space Utilization Analytics to optimize office layouts and resource allocation; Predictive Maintenance Systems that identify potential issues before they become costly problems. Our smart building platform integrates all these technologies into a unified ecosystem, typically resulting in 25-40% energy savings and significantly improved occupant comfort and productivity.",
                "source": {"title": "Smart Buildings", "url": "https://gaotech.com/smart-buildings"}
            },
            {
                "content": "GaoTech provides comprehensive real estate technology services designed to revolutionize property management. Our services include: Advanced Property Management Systems that streamline operations and automate routine tasks; Tenant Engagement Platforms featuring mobile apps, digital communication tools, and service request portals; Maintenance Automation with predictive maintenance scheduling, work order management, and vendor coordination; Building Performance Analytics offering real-time dashboards, energy usage reports, and operational insights; Smart Building Integration connecting all systems for centralized control; and 24/7 Technical Support ensuring your systems run smoothly. Our solutions are designed to increase operational efficiency by up to 40% while improving tenant satisfaction and reducing costs.",
                "source": {"title": "Property Management Services", "url": "https://gaotech.com/services"}
            },
            {
                "content": "GaoTech's energy management solutions help reduce building operating costs by up to 30% through intelligent monitoring, automated controls, and predictive maintenance.",
                "source": {"title": "Energy Management", "url": "https://gaotech.com/energy"}
            },
            {
                "content": "Our property management platform integrates with existing building systems to provide centralized control, automated reporting, and enhanced tenant experiences.",
                "source": {"title": "Property Management", "url": "https://gaotech.com/property-management"}
            },
            {
                "content": "Contact GaoTech for more information about our smart building solutions and IoT implementations. We offer free consultations and custom solution design.",
                "source": {"title": "Contact", "url": "https://gaotech.com/contact"}
            }
        ]
        self.vector_store.add_chunks(default_chunks)
    
    def chat(self, query, include_sources=True):
        try:
            # Get relevant context
            context_chunks = self.vector_store.search(query, top_k=3)
            
            # Generate response based on context
            if context_chunks:
                # Use the most relevant chunk
                best_chunk = context_chunks[0]
                response = best_chunk['content']
                
                # Add some context-aware modifications
                query_lower = query.lower()
                if 'cost' in query_lower or 'price' in query_lower:
                    response += " Our solutions are designed to provide excellent ROI through energy savings and operational efficiency."
                elif 'contact' in query_lower:
                    response += " You can reach out to our team for a personalized consultation and quote."
                elif 'how' in query_lower:
                    response += " Our expert team will work with you to design and implement the perfect solution for your building."
                
                result = {
                    'response': response,
                    'status': 'success'
                }
                
                if include_sources:
                    result['sources'] = [chunk['source'] for chunk in context_chunks[:2]]
                
                return result
            else:
                # Fallback response
                return {
                    'response': "Thank you for your question about GaoTech! We're a leading provider of Real Estate IoT solutions and smart building technologies. Our services include smart sensors, automated systems, energy management, and property management solutions. How can I help you learn more about our specific offerings?",
                    'status': 'success'
                }
                
        except Exception as e:
            return {
                'response': "I apologize, but I'm experiencing technical difficulties. Please try asking your question again.",
                'status': 'error',
                'error': str(e)
            }

# Initialize chatbot
chatbot = SimpleChatbotEngine()

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏠 GaoTech Intelligent Chatbot</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh; display: flex; justify-content: center; align-items: center;
        }
        .chat-container { 
            width: 90%; max-width: 800px; height: 90vh; background: white; 
            border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); 
            display: flex; flex-direction: column; overflow: hidden;
        }
        .chat-header { 
            background: linear-gradient(135deg, #2c3e50, #3498db); color: white; 
            padding: 20px; text-align: center;
        }
        .chat-header h1 { font-size: 1.8em; margin-bottom: 5px; }
        .chat-header p { opacity: 0.9; font-size: 0.9em; }
        .starters { 
            padding: 15px; background: #f8f9fa; border-bottom: 1px solid #e9ecef;
            display: flex; flex-wrap: wrap; gap: 8px;
        }
        .starter-btn { 
            padding: 8px 15px; background: #e3f2fd; border: 1px solid #2196f3; 
            border-radius: 20px; cursor: pointer; font-size: 13px; transition: all 0.3s;
        }
        .starter-btn:hover { background: #2196f3; color: white; }
        .messages { 
            flex: 1; overflow-y: auto; padding: 20px; background: #fafafa;
        }
        .message { 
            margin: 15px 0; padding: 12px 16px; border-radius: 12px; max-width: 80%;
            animation: fadeIn 0.3s ease-in;
        }
        .user { 
            background: linear-gradient(135deg, #667eea, #764ba2); color: white; 
            margin-left: auto; text-align: right;
        }
        .bot { 
            background: white; border: 1px solid #e0e0e0; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .input-area { 
            padding: 20px; background: white; border-top: 1px solid #e0e0e0;
            display: flex; gap: 10px;
        }
        input[type="text"] { 
            flex: 1; padding: 12px 16px; border: 2px solid #e0e0e0; 
            border-radius: 25px; font-size: 14px; outline: none;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus { border-color: #2196f3; }
        button { 
            padding: 12px 24px; background: linear-gradient(135deg, #2196f3, #1976d2); 
            color: white; border: none; border-radius: 25px; cursor: pointer;
            font-weight: 600; transition: transform 0.2s;
        }
        button:hover { transform: translateY(-1px); }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .typing { opacity: 0.7; font-style: italic; }
        .typing-dots { 
            display: inline-block; 
            margin: 0 2px; 
            opacity: 0.3; 
            transition: opacity 0.3s ease;
            font-size: 20px;
            color: #2196f3;
        }
        .sources { margin-top: 8px; font-size: 12px; opacity: 0.7; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>🏠 GaoTech Intelligent Chatbot</h1>
            <p>Your AI assistant for Real Estate IoT solutions and smart building technologies</p>
        </div>
        
        <div class="starters">
            <div class="starter-btn" onclick="sendMessage('What IoT solutions does GaoTech offer?')">🔧 IoT Solutions</div>
            <div class="starter-btn" onclick="sendMessage('Tell me about smart building technologies')">🏢 Smart Buildings</div>
            <div class="starter-btn" onclick="sendMessage('How can GaoTech help with energy management?')">⚡ Energy Management</div>
            <div class="starter-btn" onclick="sendMessage('What property management services do you provide?')">🏠 Property Management</div>
        </div>
        
        <div class="messages" id="messages"></div>
        
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="Ask about GaoTech's IoT solutions, smart buildings, or services..." onkeypress="if(event.key==='Enter') sendMessage()">
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
            
            // Show typing indicator with animation
            const typingId = addTypingIndicator();

            fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                // Remove typing indicator
                removeTypingIndicator(typingId);
                
                let responseText = data.response || data.answer || 'Sorry, I encountered an error.';
                
                // Add message with typing animation
                typeMessage(responseText, data.sources);
            })
            .catch(error => {
                removeTypingIndicator(typingId);
                typeMessage('Sorry, I encountered an error. Please try again.');
            });
        }

        function addTypingIndicator() {
            const messages = document.getElementById('messages');
            const div = document.createElement('div');
            const messageId = 'typing-' + Date.now();
            div.id = messageId;
            div.className = 'message bot typing';
            div.innerHTML = '<span class="typing-dots">●</span><span class="typing-dots">●</span><span class="typing-dots">●</span>';
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
            
            // Animate typing dots
            const dots = div.querySelectorAll('.typing-dots');
            let currentDot = 0;
            const interval = setInterval(() => {
                dots.forEach(dot => dot.style.opacity = '0.3');
                dots[currentDot].style.opacity = '1';
                currentDot = (currentDot + 1) % dots.length;
            }, 500);
            
            div.dataset.interval = interval;
            return messageId;
        }

        function removeTypingIndicator(typingId) {
            const typingEl = document.getElementById(typingId);
            if (typingEl) {
                clearInterval(typingEl.dataset.interval);
                typingEl.remove();
            }
        }

        function typeMessage(text, sources) {
            const messages = document.getElementById('messages');
            const div = document.createElement('div');
            const messageId = 'msg-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
            div.id = messageId;
            div.className = 'message bot';
            messages.appendChild(div);
            
            let index = 0;
            const typeSpeed = 30; // milliseconds per character
            
            function typeChar() {
                if (index < text.length) {
                    div.textContent = text.substring(0, index + 1);
                    index++;
                    setTimeout(typeChar, typeSpeed);
                    messages.scrollTop = messages.scrollHeight;
                } else {
                    // Add sources after typing is complete
                    if (sources && sources.length > 0) {
                        const sourcesText = 'Sources: ' + sources.map(s => s.title || 'GaoTech Knowledge Base').join(', ');
                        const sourcesEl = document.createElement('div');
                        sourcesEl.className = 'sources';
                        sourcesEl.textContent = sourcesText;
                        div.appendChild(sourcesEl);
                    }
                }
            }
            
            typeChar();
            return messageId;
        }

        function addMessage(text, sender) {
            const messages = document.getElementById('messages');
            const div = document.createElement('div');
            const messageId = 'msg-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
            div.id = messageId;
            div.className = `message ${sender}`;
            div.textContent = text;
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
            return messageId;
        }

        // Add welcome message
        window.onload = function() {
            addMessage('Hello! I\\'m the GaoTech AI assistant. I can help you learn about our Real Estate IoT solutions, smart building technologies, and property management services. What would you like to know?', 'bot');
        };
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Main chat interface"""
    return render_template_string(HTML_TEMPLATE)

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
        
        # Get response from chatbot
        response = chatbot.chat(query, include_sources=True)
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'response': 'I apologize, but I encountered an error. Please try again.',
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/status')
def status():
    """Status endpoint"""
    return jsonify({
        "status": "success",
        "message": "GaoTech Intelligent Chatbot is running",
        "version": "standalone-1.0",
        "features": ["Smart responses", "Context search", "Source attribution"]
    })

@app.route('/api/starters')
def starters():
    """Conversation starters"""
    return jsonify({
        "starters": [
            "What IoT solutions does GaoTech offer?",
            "Tell me about smart building technologies",
            "How can GaoTech help with energy management?",
            "What property management services do you provide?",
            "How much can I save with GaoTech solutions?",
            "How do I get started with GaoTech?"
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)