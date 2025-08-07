# 🏠 Real Estate IoT Intelligent Chatbot System

An advanced AI-powered chatbot system designed to provide intelligent, context-aware responses about Real Estate IoT solutions, smart building technologies, and related services. Built with modern web technologies and powered by OpenAI GPT models with sophisticated vector search capabilities.

## 🔗 Quick Access Links

| Resource | Link | Description |
|----------|------|-------------|
| **🌐 Live Application** | [https://realestatechatbot-production-160a.up.railway.app/](https://realestatechatbot-production-160a.up.railway.app/) | Try the chatbot system live |
| **📂 GitHub Repository** | [https://github.com/Prajwald-17/realestate_chatbot.git](https://github.com/Prajwald-17/realestate_chatbot.git) | Complete source code and documentation |
| **🚀 Deployment Platform** | [Railway](https://railway.app) | Cloud hosting and deployment |

## 🌟 Key Features & Capabilities

### 🤖 AI-Powered Intelligence
- **OpenAI GPT Integration**: Utilizes GPT-3.5-turbo for natural, context-aware conversations
- **Dual-Mode Operation**: Works with or without OpenAI API key (free fallback mode)
- **Smart Context Retrieval**: Advanced vector search for relevant information discovery
- **Intelligent Response Generation**: Contextual answers with source attribution

### 🔍 Advanced Search Technology
- **Vector Database**: Lightweight TF-IDF and OpenAI embeddings for semantic search
- **Content Processing**: Automated web scraping and intelligent text chunking
- **Fallback Mechanisms**: Multiple layers of search and response strategies
- **Real-time Performance**: Optimized for fast query processing and response generation

### 🎨 Modern User Experience
- **Responsive Web Interface**: Clean, professional design that works on all devices
- **Real-time Chat**: Interactive conversation with typing indicators and smooth animations
- **Conversation Starters**: Intelligent question suggestions to guide user interactions
- **Source Transparency**: Direct links to original content sources for verification

### 🛠️ Technical Excellence
- **Scalable Architecture**: Modular design with clear separation of concerns
- **Production Ready**: Deployed on Railway with proper error handling and monitoring
- **Comprehensive Testing**: Full test suite ensuring reliability and performance
- **Easy Deployment**: One-click setup and deployment configuration

## 📋 Detailed Project Description

### 🎯 Project Purpose & Vision
The Real Estate IoT Intelligent Chatbot System was developed to bridge the information gap between potential clients and Real Estate IoT services. This system automatically collects, processes, and serves information about smart building technologies, IoT solutions, and related services through an intuitive conversational interface.

### 🏗️ System Architecture Overview
The chatbot system follows a sophisticated multi-layered architecture:

1. **Data Collection Layer**: Automated web scraping system that extracts content from Real Estate IoT websites
2. **Processing Layer**: Advanced text processing pipeline that chunks, cleans, and indexes content
3. **Intelligence Layer**: AI-powered response generation using OpenAI GPT models with vector search
4. **Interface Layer**: Modern web application providing seamless user interaction
5. **Deployment Layer**: Production-ready hosting on Railway with proper monitoring and scaling

### 🔧 How the Code Was Created - Development Journey

#### Phase 1: Research & Planning (Architecture Design)
- **Problem Analysis**: Identified the need for an intelligent information retrieval system for Real Estate IoT
- **Technology Selection**: Chose Python/Flask for rapid development, OpenAI for AI capabilities, and Railway for deployment
- **Architecture Design**: Designed modular system with clear separation between data collection, processing, and serving

#### Phase 2: Core Development (Backend Systems)
```python
# 1. Web Scraping Engine (website_scraper.py)
# - Built robust scraper using BeautifulSoup and requests
# - Implemented intelligent content extraction with multiple fallback strategies
# - Added rate limiting and error handling for reliable data collection

# 2. Text Processing Pipeline (text_chunker.py)
# - Developed smart text chunking algorithm with context preservation
# - Implemented sentence-boundary splitting for coherent chunks
# - Added metadata tracking for source attribution

# 3. Vector Search System (lightweight_vector_store.py)
# - Created dual-mode vector store (OpenAI embeddings + TF-IDF)
# - Implemented efficient similarity search with cosine distance
# - Added fallback text matching for robustness
```

#### Phase 3: AI Integration (Intelligence Layer)
```python
# 4. Chatbot Engine (chatbot_engine.py)
# - Integrated OpenAI GPT-3.5-turbo for natural language generation
# - Developed sophisticated prompt engineering for context-aware responses
# - Implemented dual-mode operation (AI + template-based fallbacks)
# - Added conversation starter generation and source attribution
```

#### Phase 4: Web Interface Development (Frontend)
```html
<!-- 5. Modern Web Interface (templates/index.html) -->
<!-- - Designed responsive chat interface with CSS Grid and Flexbox -->
<!-- - Implemented real-time messaging with JavaScript fetch API -->
<!-- - Added typing indicators, message bubbles, and smooth animations -->
<!-- - Ensured mobile-first responsive design -->
```

#### Phase 5: Integration & Testing (Quality Assurance)
```python
# 6. Flask Web Application (web_interface.py)
# - Created RESTful API endpoints for chat functionality
# - Implemented proper error handling and status monitoring
# - Added CORS support and production-ready configurations

# 7. Comprehensive Testing Suite
# - Built automated tests for all system components
# - Implemented integration tests for end-to-end functionality
# - Added performance benchmarks and reliability checks
```

#### Phase 6: Deployment & Production (DevOps)
```bash
# 8. Production Deployment
# - Configured Railway deployment with Procfile and railway.json
# - Set up environment variable management for API keys
# - Implemented proper logging and monitoring
# - Added automated dependency management with requirements.txt
```

### 🧠 Technical Innovation & Problem Solving

#### Challenge 1: Efficient Content Processing
**Problem**: Large websites with diverse content structures
**Solution**: Developed intelligent content extraction with multiple CSS selectors and fallback strategies

#### Challenge 2: Vector Search Performance
**Problem**: Need for fast similarity search without expensive infrastructure
**Solution**: Implemented lightweight TF-IDF with optional OpenAI embeddings upgrade path

#### Challenge 3: AI Response Quality
**Problem**: Ensuring relevant, accurate responses with proper source attribution
**Solution**: Advanced prompt engineering with context injection and source tracking

#### Challenge 4: Production Reliability
**Problem**: Handling various failure modes in production environment
**Solution**: Multi-layer fallback systems and comprehensive error handling

## 🛠️ Technology Stack & Dependencies

### Core Technologies
- **Backend Framework**: Python 3.8+ with Flask 2.2+
- **AI/ML Stack**: OpenAI GPT API, scikit-learn (TF-IDF), NumPy
- **Web Scraping**: BeautifulSoup4, requests, lxml parser
- **Frontend**: HTML5, CSS3 (Grid/Flexbox), Vanilla JavaScript
- **Deployment**: Railway Platform, Gunicorn WSGI Server
- **Data Storage**: JSON files, pickle serialization, FAISS indexing

## 📋 System Requirements & Prerequisites

### 🖥️ Hardware Requirements
- **Minimum**: 2GB RAM, 1GB free disk space
- **Recommended**: 4GB RAM, 2GB free disk space
- **Processor**: Any modern CPU (Intel/AMD x64 or ARM64)
- **Network**: Stable internet connection for initial setup and AI features

### 💻 Software Requirements

#### Essential Requirements
- **Python**: Version 3.8 or higher (3.11.9 recommended for production)
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Internet Connection**: Required for initial setup, web scraping, and OpenAI integration

#### Optional Requirements
- **OpenAI API Key**: For enhanced AI responses (system works without it)
- **Git**: For cloning the repository (or download ZIP directly)
- **Code Editor**: VS Code, PyCharm, or any text editor for customization

### 📦 Python Dependencies (Automatically Installed)

#### Core Web Framework
```txt
flask>=2.2.0                 # Web application framework
gunicorn>=20.1.0             # Production WSGI server
python-dotenv>=0.19.0        # Environment variable management
```

#### AI & Machine Learning
```txt
openai>=1.0.0                # OpenAI GPT API integration
numpy>=1.21.0,<1.25.0        # Numerical computing
scikit-learn>=1.3.0,<1.4.0   # Machine learning algorithms (TF-IDF)
```

#### Web Scraping & Processing
```txt
requests>=2.28.0             # HTTP library for web scraping
beautifulsoup4>=4.11.0       # HTML/XML parsing
lxml>=4.9.0                  # Fast XML/HTML parser
nltk>=3.8                    # Natural language processing
```

### 🔑 API Keys & Configuration

#### OpenAI API Key (Optional but Recommended)
1. **Sign up** at [OpenAI Platform](https://platform.openai.com/)
2. **Navigate** to API Keys section
3. **Create** a new API key
4. **Copy** the key (starts with `sk-`)
5. **Add** to `.env` file: `OPENAI_API_KEY=your_key_here`

**Benefits with OpenAI Key**:
- Natural, conversational responses
- Better context understanding
- Improved answer quality
- Advanced reasoning capabilities

**Without OpenAI Key**:
- Template-based responses
- Keyword matching search
- Basic functionality maintained
- No additional costs

### 🚀 Quick Start Installation Guide

#### Option 1: Automated Setup (Recommended)
```bash
# 1. Clone the repository
git clone https://github.com/Prajwald-17/realestate_chatbot.git
cd realestate_chatbot

# 2. Run automated setup (installs everything)
python setup.py

# 3. Start the application
python start.py
```

#### Option 2: Manual Installation
```bash
# 1. Clone repository
git clone https://github.com/Prajwald-17/realestate_chatbot.git
cd realestate_chatbot

# 2. Create virtual environment (recommended)
python -m venv chatbot_env
# Windows:
chatbot_env\Scripts\activate
# macOS/Linux:
source chatbot_env/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create environment file
echo "OPENAI_API_KEY=your_key_here" > .env

# 5. Initialize data (scrape and process content)
python website_scraper.py
python text_chunker.py
python rebuild_lightweight_store.py

# 6. Start the application
python web_interface.py
```

### 🔧 Configuration Options

#### Environment Variables (.env file)
```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-key-here

# Flask Configuration
FLASK_ENV=development          # or 'production'
FLASK_DEBUG=True              # Set to False in production
PORT=5000                     # Server port

# Chatbot Configuration
USE_OPENAI_EMBEDDINGS=False   # True for better search (costs API credits)
MODEL_NAME=gpt-3.5-turbo     # OpenAI model to use
MAX_TOKENS=500               # Maximum response length
```

#### Customization Options
- **Conversation Starters**: Edit in `chatbot_engine.py`
- **UI Styling**: Modify `templates/index.html`
- **Scraping Targets**: Update URLs in `website_scraper.py`
- **Response Templates**: Customize in `chatbot_engine.py`

## 🚀 Deployment Guide

### Production Deployment on Railway

#### Automatic Deployment (Recommended)
1. **Fork Repository**: Fork the GitHub repository to your account
2. **Connect Railway**: Link your GitHub account to Railway
3. **Deploy**: Railway automatically detects and deploys the Flask app
4. **Environment Variables**: Set `OPENAI_API_KEY` in Railway dashboard
5. **Custom Domain**: Optional - configure custom domain in Railway settings

#### Manual Railway Deployment
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

## 👨‍💻 Author & Acknowledgments

### Project Author
**Prajwal** - Full Stack Developer & AI Enthusiast
- 📧 Email: [Contact via GitHub](https://github.com/Prajwald-17)
- 🔗 GitHub: [@Prajwald-17](https://github.com/Prajwald-17)
- 💼 LinkedIn: [Connect with me](https://linkedin.com/in/prajwal-developer)

### Acknowledgments & Credits
- **OpenAI** - For providing advanced GPT models and embeddings
- **Railway** - For reliable and easy deployment platform
- **Real Estate IoT** - For domain expertise and content source
- **Flask Community** - For excellent web framework and documentation
- **scikit-learn** - For machine learning tools and TF-IDF implementation
- **BeautifulSoup** - For robust web scraping capabilities


## 🎯 Quick Start Summary

1. **Clone**: `git clone https://github.com/Prajwald-17/realestate_chatbot.git`
2. **Setup**: `python setup.py`
3. **Start**: `python start.py`
4. **Visit**: `http://localhost:5000`
5. **Deploy**: Connect to Railway for production

---

## 📞 Support & Contact

### Getting Help
- **🐛 Bug Reports**: [Open GitHub Issue](https://github.com/Prajwald-17/realestate_chatbot/issues)
- **💡 Feature Requests**: [GitHub Discussions](https://github.com/Prajwald-17/realestate_chatbot/discussions)
- **📚 Documentation**: Check this README and inline code comments
- **💬 Questions**: Open an issue with the "question" label


**🚀 Ready to get started? Try the live demo at [https://realestatechatbot-production-160a.up.railway.app/](https://realestatechatbot-production-160a.up.railway.app/) or clone the repository to run locally!**
