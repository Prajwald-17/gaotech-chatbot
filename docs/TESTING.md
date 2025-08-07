# Testing Guide

## Overview

This document provides comprehensive information about testing the Real Estate IoT Chatbot system, including unit tests, integration tests, and manual testing procedures.

## Test Structure

```
tests/
├── test_system.py              # System integration tests
├── test_improved_responses.py  # Response quality tests
├── test_4_questions.py         # Core functionality tests
└── test_typing.py              # Performance and typing tests
```

## Running Tests

### Prerequisites

1. **Install Test Dependencies**
   ```bash
   pip install pytest pytest-cov pytest-mock
   ```

2. **Set Up Test Environment**
   ```bash
   # Create test environment file
   echo "OPENAI_API_KEY=test_key" > .env.test
   ```

### Running All Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run with verbose output
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_system.py -v
```

### Running Individual Test Modules

```bash
# System integration tests
python tests/test_system.py

# Response quality tests
python tests/test_improved_responses.py

# Core functionality tests
python tests/test_4_questions.py

# Performance tests
python tests/test_typing.py
```

## Test Categories

### 1. Unit Tests

Test individual components in isolation.

**Example: Testing ChatbotEngine**
```python
import unittest
from unittest.mock import patch, MagicMock
from src.core.chatbot_engine import ChatbotEngine

class TestChatbotEngine(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.engine = ChatbotEngine(openai_api_key=None)
    
    def test_initialization_without_openai(self):
        """Test chatbot initialization without OpenAI key."""
        self.assertFalse(self.engine.use_openai)
        self.assertEqual(self.engine.model_name, "free")
    
    def test_retrieve_context(self):
        """Test context retrieval functionality."""
        query = "What is IoT?"
        results = self.engine.retrieve_context(query, top_k=3)
        self.assertIsInstance(results, list)
        self.assertLessEqual(len(results), 3)
```

### 2. Integration Tests

Test component interactions and end-to-end functionality.

**Example: Testing Web API**
```python
import unittest
import json
from src.web.web_interface import app

class TestWebInterface(unittest.TestCase):
    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_chat_api_endpoint(self):
        """Test chat API endpoint."""
        response = self.app.post('/api/chat',
                               data=json.dumps({'message': 'Hello'}),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('response', data)
    
    def test_status_endpoint(self):
        """Test status endpoint."""
        response = self.app.get('/api/status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)
```

### 3. Performance Tests

Test system performance and response times.

**Example: Response Time Testing**
```python
import time
import unittest
from src.core.chatbot_engine import ChatbotEngine

class TestPerformance(unittest.TestCase):
    def setUp(self):
        self.engine = ChatbotEngine()
    
    def test_response_time(self):
        """Test that responses are generated within acceptable time."""
        query = "What services do you offer?"
        
        start_time = time.time()
        response = self.engine.chat(query)
        end_time = time.time()
        
        response_time = end_time - start_time
        self.assertLess(response_time, 5.0)  # Should respond within 5 seconds
```

### 4. Data Quality Tests

Test data processing and vector store functionality.

**Example: Vector Store Testing**
```python
import unittest
from src.core.lightweight_vector_store import LightweightVectorStore

class TestVectorStore(unittest.TestCase):
    def setUp(self):
        self.vector_store = LightweightVectorStore()
    
    def test_search_functionality(self):
        """Test vector search returns relevant results."""
        query = "smart building technology"
        results = self.vector_store.search(query, top_k=5)
        
        self.assertIsInstance(results, list)
        self.assertLessEqual(len(results), 5)
        
        # Check result structure
        if results:
            result = results[0]
            self.assertIn('content', result)
            self.assertIn('score', result)
```

## Test Data

### Mock Data Setup

Create test data for consistent testing:

```python
# tests/test_data.py
SAMPLE_QUERIES = [
    "What is Real Estate IoT?",
    "What services do you offer?",
    "How can I contact you?",
    "What are smart building solutions?"
]

EXPECTED_RESPONSES = {
    "iot_query": "Real Estate IoT refers to",
    "services_query": "We offer",
    "contact_query": "You can contact",
    "smart_building_query": "Smart building solutions"
}

SAMPLE_CHUNKS = [
    {
        "content": "Real Estate IoT provides smart building solutions...",
        "metadata": {"source": "test_source", "title": "Test Title"}
    },
    {
        "content": "Our services include IoT implementation...",
        "metadata": {"source": "test_source_2", "title": "Test Title 2"}
    }
]
```

### Environment Setup for Tests

```python
# tests/conftest.py
import pytest
import os
import tempfile
from src.core.chatbot_engine import ChatbotEngine

@pytest.fixture
def temp_data_dir():
    """Create temporary directory for test data."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

@pytest.fixture
def mock_chatbot():
    """Create chatbot instance for testing."""
    return ChatbotEngine(openai_api_key=None)

@pytest.fixture
def test_client():
    """Create Flask test client."""
    from src.web.web_interface import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
```

## Manual Testing

### 1. Functional Testing

**Chat Functionality:**
1. Open the web interface
2. Test basic queries:
   - "What is Real Estate IoT?"
   - "What services do you offer?"
   - "How can I contact you?"
3. Verify responses are relevant and well-formatted
4. Check that sources are provided when available

**API Testing:**
```bash
# Test chat endpoint
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is IoT?"}'

# Test status endpoint
curl -X GET http://localhost:5000/api/status

# Test starters endpoint
curl -X GET http://localhost:5000/api/starters
```

### 2. User Interface Testing

**Responsive Design:**
1. Test on different screen sizes
2. Verify mobile compatibility
3. Check chat bubble formatting
4. Test conversation starter buttons

**User Experience:**
1. Test typing indicators
2. Verify smooth scrolling
3. Check message history display
4. Test error handling display

### 3. Performance Testing

**Load Testing:**
```python
import concurrent.futures
import requests
import time

def send_request():
    response = requests.post('http://localhost:5000/api/chat',
                           json={'message': 'Test query'})
    return response.status_code

# Test concurrent requests
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(send_request) for _ in range(50)]
    results = [future.result() for future in futures]

print(f"Success rate: {results.count(200)/len(results)*100}%")
```

### 4. Error Handling Testing

**Invalid Inputs:**
- Empty messages
- Very long messages (>10000 characters)
- Special characters and emojis
- SQL injection attempts
- XSS attempts

**System Errors:**
- Missing vector store files
- Invalid OpenAI API key
- Network connectivity issues
- Memory limitations

## Continuous Integration

### GitHub Actions Example

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

## Test Coverage

### Measuring Coverage

```bash
# Generate coverage report
pytest tests/ --cov=src --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html
```

### Coverage Goals

- **Overall Coverage**: >80%
- **Core Components**: >90%
- **Critical Paths**: 100%

### Coverage Exclusions

```python
# .coveragerc
[run]
source = src
omit = 
    */tests/*
    */venv/*
    */migrations/*
    */settings/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

## Debugging Tests

### Common Issues

1. **Import Errors**
   ```python
   # Add to test files if needed
   import sys
   import os
   sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
   ```

2. **Missing Test Data**
   ```bash
   # Ensure test data exists
   python src/data_processing/website_scraper.py
   python src/data_processing/text_chunker.py
   ```

3. **Environment Variables**
   ```python
   # Set test environment variables
   os.environ['OPENAI_API_KEY'] = 'test_key'
   ```

### Debug Mode

```bash
# Run tests with debug output
pytest tests/ -v -s --tb=long

# Run specific test with debugging
pytest tests/test_system.py::TestChatbot::test_basic_chat -v -s
```

## Best Practices

### Writing Tests

1. **Use Descriptive Names**: Test names should clearly describe what is being tested
2. **Test One Thing**: Each test should focus on a single functionality
3. **Use Fixtures**: Reuse common setup code with pytest fixtures
4. **Mock External Dependencies**: Use mocks for API calls and file operations
5. **Test Edge Cases**: Include tests for boundary conditions and error cases

### Test Organization

1. **Group Related Tests**: Use test classes to group related functionality
2. **Use Setup/Teardown**: Clean up resources after tests
3. **Document Test Purpose**: Add docstrings to explain complex tests
4. **Keep Tests Fast**: Avoid slow operations in unit tests

### Maintenance

1. **Update Tests with Code Changes**: Keep tests synchronized with code
2. **Review Test Coverage**: Regularly check and improve coverage
3. **Refactor Tests**: Keep test code clean and maintainable
4. **Monitor Test Performance**: Ensure tests run quickly