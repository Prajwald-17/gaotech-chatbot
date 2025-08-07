# API Documentation

## Overview

The Real Estate IoT Chatbot provides a RESTful API for interacting with the chatbot system. All endpoints return JSON responses and follow standard HTTP status codes.

## Base URL

- **Local Development**: `http://localhost:5000`
- **Production**: `https://realestatechatbot-production-160a.up.railway.app`

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

## Endpoints

### 1. Main Chat Interface

#### `GET /`

Returns the main chat interface HTML page.

**Response:**
- **Content-Type**: `text/html`
- **Status**: `200 OK`

**Example:**
```bash
curl -X GET http://localhost:5000/
```

---

### 2. Chat API

#### `POST /api/chat`

Process a user message and return a chatbot response.

**Request Body:**
```json
{
  "message": "What is Real Estate IoT?"
}
```

**Parameters:**
- `message` (string, required): The user's input message

**Response:**
```json
{
  "response": "Real Estate IoT refers to the integration of Internet of Things (IoT) technologies...",
  "sources": [
    {
      "content": "Relevant content snippet...",
      "metadata": {
        "source": "https://example.com/page",
        "title": "Page Title"
      }
    }
  ],
  "status": "success",
  "model_used": "gpt-3.5-turbo",
  "response_time": 1.23
}
```

**Status Codes:**
- `200 OK`: Successful response
- `400 Bad Request`: Empty or invalid message
- `500 Internal Server Error`: Server error

**Example:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What services do you offer?"}'
```

---

### 3. Conversation Starters

#### `GET /api/starters`

Get suggested conversation starter questions.

**Response:**
```json
{
  "starters": [
    "What is Real Estate IoT and what do you do?",
    "What IoT solutions do you offer for buildings?",
    "What career opportunities are available?",
    "How can I contact Real Estate IoT?"
  ]
}
```

**Status Codes:**
- `200 OK`: Successful response
- `500 Internal Server Error`: Server error

**Example:**
```bash
curl -X GET http://localhost:5000/api/starters
```

---

### 4. System Status

#### `GET /api/status`

Get the current system status and health information.

**Response:**
```json
{
  "status": "ready",
  "model": "gpt-3.5-turbo",
  "vector_store_loaded": true,
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

**Status Codes:**
- `200 OK`: System is operational
- `500 Internal Server Error`: System error

**Example:**
```bash
curl -X GET http://localhost:5000/api/status
```

## Response Format

### Success Response

All successful API responses follow this general structure:

```json
{
  "status": "success",
  "data": {
    // Endpoint-specific data
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Error Response

Error responses follow this structure:

```json
{
  "status": "error",
  "error": "Error description",
  "code": "ERROR_CODE",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Error Codes

| Code | Description |
|------|-------------|
| `EMPTY_MESSAGE` | The message parameter is empty or missing |
| `INVALID_REQUEST` | The request format is invalid |
| `CHATBOT_ERROR` | Error in chatbot processing |
| `VECTOR_STORE_ERROR` | Error accessing vector store |
| `OPENAI_ERROR` | Error with OpenAI API |
| `INTERNAL_ERROR` | General server error |

## Rate Limiting

Currently, there are no rate limits implemented. However, for production use, consider implementing rate limiting to prevent abuse.

## CORS

Cross-Origin Resource Sharing (CORS) is enabled for all origins in development mode. In production, configure CORS appropriately for your domain.

## Examples

### JavaScript/Fetch API

```javascript
// Send a chat message
async function sendMessage(message) {
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: message })
    });
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
  }
}

// Get conversation starters
async function getStarters() {
  try {
    const response = await fetch('/api/starters');
    const data = await response.json();
    return data.starters;
  } catch (error) {
    console.error('Error:', error);
  }
}
```

### Python/Requests

```python
import requests

# Send a chat message
def send_message(message, base_url="http://localhost:5000"):
    url = f"{base_url}/api/chat"
    payload = {"message": message}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Get system status
def get_status(base_url="http://localhost:5000"):
    url = f"{base_url}/api/status"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
```

### cURL Examples

```bash
# Send a chat message
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about smart building solutions"}'

# Get conversation starters
curl -X GET http://localhost:5000/api/starters

# Check system status
curl -X GET http://localhost:5000/api/status

# Get main interface
curl -X GET http://localhost:5000/
```

## WebSocket Support

Currently, the API uses HTTP requests. For real-time features, consider implementing WebSocket support for:
- Real-time typing indicators
- Live conversation updates
- Push notifications

## Future Enhancements

### Planned API Features
- User authentication and session management
- Conversation history endpoints
- File upload for document processing
- Webhook support for integrations
- GraphQL API option
- API versioning

### Security Enhancements
- API key authentication
- Rate limiting
- Request validation
- HTTPS enforcement
- Input sanitization

## Support

For API support and questions:
- **GitHub Issues**: [Open an issue](https://github.com/Prajwald-17/realestate_chatbot/issues)
- **Documentation**: Check the `/docs` directory
- **Examples**: See the `/examples` directory (if available)