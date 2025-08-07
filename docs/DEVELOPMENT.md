# Development Guide

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git (optional, for cloning)
- Text editor or IDE (VS Code recommended)
- OpenAI API key (optional, for enhanced features)

### Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Prajwald-17/realestate_chatbot.git
   cd realestate_chatbot
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   FLASK_ENV=development
   FLASK_DEBUG=True
   PORT=5000
   ```

5. **Initialize Data**
   ```bash
   python src/data_processing/website_scraper.py
   python src/data_processing/text_chunker.py
   python src/data_processing/rebuild_lightweight_store.py
   ```

6. **Run the Application**
   ```bash
   python app.py
   ```

## Project Structure Explained

### Source Code Organization

```
src/
├── core/                    # Core business logic
│   ├── __init__.py         # Package initialization
│   ├── chatbot_engine.py   # Main chatbot logic
│   ├── lightweight_vector_store.py  # Vector search
│   └── vector_store.py     # Alternative vector implementation
├── data_processing/        # Data pipeline
│   ├── __init__.py        # Package initialization
│   ├── website_scraper.py # Web scraping
│   ├── text_chunker.py    # Text processing
│   ├── rebuild_lightweight_store.py  # Vector store building
│   └── nltk_setup.py      # NLP setup
└── web/                   # Web interface
    ├── __init__.py        # Package initialization
    ├── web_interface.py   # Flask application
    └── templates/         # HTML templates
        └── index.html     # Main chat interface
```

### Key Components

#### ChatbotEngine (`src/core/chatbot_engine.py`)
- **Purpose**: Main chatbot logic and response generation
- **Key Methods**:
  - `chat()`: Process user queries and generate responses
  - `retrieve_context()`: Find relevant information from vector store
  - `build_prompt()`: Construct prompts for AI models
  - `get_conversation_starter()`: Generate conversation starters

#### LightweightVectorStore (`src/core/lightweight_vector_store.py`)
- **Purpose**: Efficient similarity search and context retrieval
- **Key Methods**:
  - `search()`: Find similar text chunks
  - `load_index()`: Load pre-built vector index
  - `build_index()`: Create new vector index from text chunks

#### WebInterface (`src/web/web_interface.py`)
- **Purpose**: Flask web application and API endpoints
- **Key Endpoints**:
  - `GET /`: Main chat interface
  - `POST /api/chat`: Chat API for message processing
  - `GET /api/starters`: Get conversation starters
  - `GET /api/status`: System health check

## Development Workflow

### Adding New Features

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/new-feature-name
   ```

2. **Implement Changes**
   - Add new functionality in appropriate module
   - Follow existing code patterns and conventions
   - Add docstrings and comments

3. **Write Tests**
   - Add unit tests in `tests/` directory
   - Test both success and failure scenarios
   - Ensure good test coverage

4. **Test Locally**
   ```bash
   python -m pytest tests/
   python app.py  # Manual testing
   ```

5. **Update Documentation**
   - Update relevant documentation files
   - Add inline code comments
   - Update README if needed

### Code Style Guidelines

#### Python Code Style
- Follow PEP 8 conventions
- Use meaningful variable and function names
- Add type hints where appropriate
- Include docstrings for all functions and classes

#### Example Function Structure
```python
def process_user_query(query: str, context_limit: int = 5) -> Dict[str, Any]:
    """
    Process a user query and return a structured response.
    
    Args:
        query: The user's input query
        context_limit: Maximum number of context chunks to retrieve
        
    Returns:
        Dictionary containing response and metadata
        
    Raises:
        ValueError: If query is empty or invalid
    """
    # Implementation here
    pass
```

### Testing Guidelines

#### Unit Tests
- Test individual functions and methods
- Mock external dependencies (OpenAI API, file system)
- Use descriptive test names

#### Integration Tests
- Test component interactions
- Verify end-to-end functionality
- Test with real data when possible

#### Example Test Structure
```python
import unittest
from unittest.mock import patch, MagicMock
from src.core.chatbot_engine import ChatbotEngine

class TestChatbotEngine(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.engine = ChatbotEngine(openai_api_key=None)
    
    def test_chat_with_valid_query(self):
        """Test chat method with valid user query."""
        # Test implementation
        pass
    
    @patch('src.core.chatbot_engine.openai')
    def test_chat_with_openai_integration(self, mock_openai):
        """Test chat method with OpenAI API integration."""
        # Test implementation with mocked OpenAI
        pass
```

### Debugging Tips

#### Common Issues
1. **Import Errors**: Check Python path and module structure
2. **Vector Store Not Found**: Run data initialization scripts
3. **OpenAI API Errors**: Verify API key and rate limits
4. **Flask Template Errors**: Check template file paths

#### Debugging Tools
- Use Python debugger: `import pdb; pdb.set_trace()`
- Flask debug mode: Set `FLASK_DEBUG=True`
- Logging: Add print statements or use Python logging module

### Performance Optimization

#### Vector Search Optimization
- Use appropriate chunk sizes (500-1000 characters)
- Optimize TF-IDF parameters
- Consider caching frequent queries

#### Memory Management
- Monitor memory usage with large datasets
- Use generators for processing large files
- Clean up temporary objects

#### API Response Time
- Implement response caching
- Optimize database queries
- Use async processing for long operations

## Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set environment variables for production
2. Use production WSGI server (Gunicorn)
3. Configure proper logging
4. Set up monitoring and health checks

### Railway Deployment
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy to Railway
railway login
railway init
railway up
```

## Contributing

### Pull Request Process
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

### Code Review Guidelines
- Review for functionality and correctness
- Check code style and conventions
- Verify test coverage
- Ensure documentation is updated

## Troubleshooting

### Common Development Issues

#### Module Import Errors
```python
# Add to Python path if needed
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
```

#### Vector Store Issues
```bash
# Rebuild vector store
python src/data_processing/rebuild_lightweight_store.py
```

#### Flask Template Issues
```python
# Ensure templates directory is correctly configured
app = Flask(__name__, template_folder='templates')
```

### Getting Help
- Check existing issues on GitHub
- Review documentation in `docs/` directory
- Contact maintainers through GitHub issues