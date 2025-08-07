# System Architecture Documentation

## Overview

The Real Estate IoT Chatbot is built with a modular, scalable architecture that separates concerns into distinct layers. This document provides a detailed overview of the system architecture, components, and data flow.

## Architecture Layers

### 1. Presentation Layer (`src/web/`)
- **Purpose**: User interface and API endpoints
- **Components**:
  - `web_interface.py`: Flask web application with REST API
  - `templates/index.html`: Responsive chat interface
  - `static/`: CSS, JavaScript, and other static assets

### 2. Business Logic Layer (`src/core/`)
- **Purpose**: Core chatbot functionality and AI processing
- **Components**:
  - `chatbot_engine.py`: Main chatbot logic, prompt engineering, and response generation
  - `lightweight_vector_store.py`: Vector search and similarity matching
  - `vector_store.py`: Alternative vector store implementation

### 3. Data Processing Layer (`src/data_processing/`)
- **Purpose**: Data collection, processing, and preparation
- **Components**:
  - `website_scraper.py`: Web scraping and content extraction
  - `text_chunker.py`: Text processing and intelligent chunking
  - `rebuild_lightweight_store.py`: Vector store building and indexing
  - `nltk_setup.py`: Natural language processing initialization

### 4. Data Storage Layer (`data/`)
- **Purpose**: Persistent data storage
- **Components**:
  - `scraped_content.json`: Raw scraped website content
  - `text_chunks.json`: Processed and chunked text data
  - `vector_store.faiss`: FAISS vector index for similarity search
  - `vector_store_*.json`: Vector store metadata and configurations

### 5. Testing Layer (`tests/`)
- **Purpose**: Quality assurance and system validation
- **Components**:
  - `test_system.py`: Integration and system tests
  - `test_improved_responses.py`: Response quality validation
  - `test_4_questions.py`: Core functionality tests
  - `test_typing.py`: Performance and typing tests

### 6. Deployment Layer (`deployment/`)
- **Purpose**: Production deployment configuration
- **Components**:
  - `Procfile`: Railway/Heroku deployment configuration
  - `railway.json`: Railway-specific settings
  - `runtime.txt`: Python runtime version specification

## Data Flow

```
1. Data Collection
   Website Scraper → Raw Content (JSON)

2. Data Processing
   Raw Content → Text Chunker → Processed Chunks (JSON)
   
3. Vector Store Creation
   Processed Chunks → Vector Store Builder → FAISS Index + Metadata

4. Query Processing
   User Query → Chatbot Engine → Vector Search → Context Retrieval
   
5. Response Generation
   Context + Query → OpenAI API / Template Engine → Response

6. Web Interface
   Response → Flask API → Frontend → User Display
```

## Component Interactions

### ChatbotEngine
- **Inputs**: User queries, configuration parameters
- **Outputs**: Contextual responses with source attribution
- **Dependencies**: LightweightVectorStore, OpenAI API (optional)

### LightweightVectorStore
- **Inputs**: Text queries, vector embeddings
- **Outputs**: Ranked similarity results
- **Dependencies**: scikit-learn (TF-IDF), OpenAI embeddings (optional)

### WebInterface
- **Inputs**: HTTP requests, user messages
- **Outputs**: JSON responses, HTML pages
- **Dependencies**: ChatbotEngine, Flask framework

## Scalability Considerations

### Horizontal Scaling
- Stateless design allows multiple instance deployment
- Vector store can be shared across instances
- API-based architecture supports load balancing

### Performance Optimization
- Lightweight TF-IDF for fast local search
- Optional OpenAI embeddings for enhanced accuracy
- Efficient text chunking for optimal context retrieval
- FAISS indexing for fast similarity search

### Resource Management
- Configurable model parameters
- Optional AI features to reduce API costs
- Efficient memory usage with pickle serialization
- Minimal dependencies for lightweight deployment

## Security Features

### API Security
- Environment variable configuration for sensitive data
- Input validation and sanitization
- Error handling without information leakage

### Data Privacy
- Local vector store option (no external data sharing)
- Configurable OpenAI integration
- No persistent user conversation storage

## Monitoring and Logging

### Application Monitoring
- Flask built-in logging
- Error tracking and reporting
- Performance metrics collection

### Health Checks
- `/api/status` endpoint for system health
- Vector store validation
- Model availability checking

## Future Enhancements

### Planned Features
- User authentication and session management
- Conversation history and context persistence
- Advanced analytics and usage tracking
- Multi-language support
- Custom domain knowledge integration

### Technical Improvements
- Microservices architecture migration
- Database integration for scalable storage
- Advanced caching mechanisms
- Real-time model fine-tuning
- Enhanced security features