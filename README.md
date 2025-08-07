# 🏠 GaoTech Intelligent Chatbot System

An advanced AI-powered chatbot system designed to provide intelligent, context-aware responses about Real Estate IoT solutions, smart building technologies, and related services.

## 🔗 Quick Access Links

| Resource | Link | Description |
|----------|------|-------------|
| **📂 GitHub Repository** | [https://github.com/Prajwald-17/gaotech-chatbot.git](https://github.com/Prajwald-17/gaotech-chatbot.git) | Complete source code and documentation |
| **🌐 Live Application** | Coming Soon | Try the chatbot system live |

## 📁 Project Structure

```
gaotech-chatbot/
├── src/                          # Source code
│   ├── core/                     # Core chatbot functionality
│   │   ├── chatbot_engine.py     # Main chatbot logic
│   │   ├── lightweight_vector_store.py  # Vector search implementation
│   │   └── vector_store.py       # Alternative vector store
│   ├── data_processing/          # Data collection and processing
│   │   ├── website_scraper.py    # Web scraping functionality
│   │   ├── text_chunker.py       # Text processing and chunking
│   │   ├── rebuild_lightweight_store.py  # Vector store rebuilding
│   │   └── nltk_setup.py         # NLTK initialization
│   └── web/                      # Web interface
│       ├── web_interface.py      # Flask web application
│       └── templates/            # HTML templates
│           └── index.html        # Main chat interface
├── tests/                        # Test suite
│   ├── test_system.py           # System integration tests
│   ├── test_improved_responses.py  # Response quality tests
│   ├── test_4_questions.py      # Core functionality tests
│   └── test_typing.py           # Typing and performance tests
├── data/                        # Data storage
│   ├── scraped_content.json    # Raw scraped content
│   ├── text_chunks.json        # Processed text chunks
│   ├── vector_store.faiss       # FAISS vector index
│   └── vector_store_*.json      # Vector store metadata
├── deployment/                  # Deployment configuration
│   ├── Procfile                # Railway deployment config
│   ├── railway.json            # Railway settings
│   └── runtime.txt             # Python runtime version
├── docs/                       # Documentation
│   └── README.md              # Detailed documentation
├── requirements.txt            # Python dependencies
├── setup.py                   # Automated setup script
├── start.py                   # Quick start script
└── demo.py                    # Demo/testing script
```

## 🚀 Quick Start

1. **Clone and Setup**:
   ```bash
   git clone https://github.com/Prajwald-17/gaotech-chatbot.git
   cd gaotech-chatbot
   python setup.py
   ```

2. **Start the Application**:
   ```bash
   python start.py
   ```

3. **Visit**: `http://localhost:5000`

## 🌟 Key Features

### 🤖 AI-Powered Intelligence
- **OpenAI GPT Integration**: Utilizes GPT-3.5-turbo for natural conversations
- **Dual-Mode Operation**: Works with or without OpenAI API key
- **Smart Context Retrieval**: Advanced vector search for relevant information
- **Intelligent Response Generation**: Contextual answers with source attribution

### 🔍 Advanced Search Technology
- **Vector Database**: Lightweight TF-IDF and OpenAI embeddings
- **Content Processing**: Automated web scraping and text chunking
- **Fallback Mechanisms**: Multiple layers of search strategies
- **Real-time Performance**: Optimized for fast query processing

### 🎨 Modern User Experience
- **Responsive Web Interface**: Clean, professional design
- **Real-time Chat**: Interactive conversation with typing indicators
- **Conversation Starters**: Intelligent question suggestions
- **Source Transparency**: Direct links to original content sources

## 🛠️ Technology Stack

- **Backend**: Python 3.8+ with Flask 2.2+
- **AI/ML**: OpenAI GPT API, scikit-learn (TF-IDF), NumPy
- **Web Scraping**: BeautifulSoup4, requests, lxml
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Deployment**: Railway Platform, Gunicorn WSGI Server
- **Data Storage**: JSON files, pickle serialization, FAISS indexing

## 📋 System Requirements

### Hardware Requirements
- **Minimum**: 2GB RAM, 1GB free disk space
- **Recommended**: 4GB RAM, 2GB free disk space
- **Network**: Stable internet connection

### Software Requirements
- **Python**: Version 3.8 or higher (3.11.9 recommended)
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Optional**: OpenAI API Key for enhanced AI responses

## 🔧 Configuration

### Environment Variables (.env file)
```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-key-here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000

# Chatbot Configuration
USE_OPENAI_EMBEDDINGS=False
MODEL_NAME=gpt-3.5-turbo
MAX_TOKENS=500
```

## 🚀 Deployment

### Railway Deployment
1. Fork the repository
2. Connect to Railway
3. Set environment variables
4. Deploy automatically

## 👨‍💻 Author

**Prajwal** - Full Stack Developer & AI Enthusiast
- 📧 Email: [Contact via GitHub](https://github.com/Prajwald-17)
- 🔗 GitHub: [@Prajwald-17](https://github.com/Prajwald-17)

## 📞 Support

- **🐛 Bug Reports**: [Open GitHub Issue](https://github.com/Prajwald-17/gaotech-chatbot/issues)
- **💡 Feature Requests**: [GitHub Discussions](https://github.com/Prajwald-17/gaotech-chatbot/discussions)
- **📚 Documentation**: Check this README and inline code comments

---

**🚀 Ready to get started? Try the live demo or clone the repository to run locally!**