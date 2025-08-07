# Deployment Guide

## Overview

This guide covers deployment options for the Real Estate IoT Chatbot, from local development to production environments.

## Deployment Options

### 1. Local Development

**Quick Start:**
```bash
# Clone and setup
git clone https://github.com/Prajwald-17/realestate_chatbot.git
cd realestate_chatbot

# Install dependencies
pip install -r requirements.txt

# Setup environment
echo "OPENAI_API_KEY=your_key_here" > .env

# Initialize data
python setup.py

# Start application
python app.py
```

**Manual Setup:**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Setup data
python src/data_processing/website_scraper.py
python src/data_processing/text_chunker.py
python src/data_processing/rebuild_lightweight_store.py

# Start application
python app.py
```

### 2. Railway Deployment (Recommended)

Railway provides easy deployment with automatic builds and scaling.

**Automatic Deployment:**
1. Fork the repository on GitHub
2. Connect your GitHub account to Railway
3. Create a new project and select your repository
4. Railway automatically detects the Flask app
5. Set environment variables in Railway dashboard
6. Deploy with one click

**Manual Railway Deployment:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Set environment variables
railway variables set OPENAI_API_KEY=your_key_here

# Deploy
railway up
```

**Railway Configuration Files:**

`Procfile`:
```
web: gunicorn --bind 0.0.0.0:$PORT app:app
```

`railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn --bind 0.0.0.0:$PORT app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 3. Heroku Deployment

**Prerequisites:**
- Heroku account
- Heroku CLI installed

**Deployment Steps:**
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key_here

# Deploy
git push heroku main

# Scale dynos
heroku ps:scale web=1
```

**Heroku Configuration:**

`Procfile`:
```
web: gunicorn --bind 0.0.0.0:$PORT app:app
release: python setup.py
```

`runtime.txt`:
```
python-3.11.9
```

### 4. Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p data

# Setup NLTK data
RUN python src/data_processing/nltk_setup.py

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

**Docker Compose:**
```yaml
version: '3.8'

services:
  chatbot:
    build: .
    ports:
      - "5000:5000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - FLASK_ENV=production
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - chatbot
    restart: unless-stopped
```

**Build and Run:**
```bash
# Build image
docker build -t realestate-chatbot .

# Run container
docker run -p 5000:5000 -e OPENAI_API_KEY=your_key realestate-chatbot

# Using Docker Compose
docker-compose up -d
```

### 5. AWS Deployment

**AWS Elastic Beanstalk:**

1. **Prepare Application:**
   ```bash
   # Create deployment package
   zip -r chatbot-app.zip . -x "*.git*" "venv/*" "__pycache__/*"
   ```

2. **Deploy to Elastic Beanstalk:**
   - Create new application in EB console
   - Upload zip file
   - Configure environment variables
   - Deploy

**AWS Lambda + API Gateway:**

`lambda_function.py`:
```python
import json
from mangum import Mangum
from app import app

handler = Mangum(app)

def lambda_handler(event, context):
    return handler(event, context)
```

**Requirements for Lambda:**
```txt
# Add to requirements.txt
mangum>=0.17.0
```

### 6. Google Cloud Platform

**App Engine Deployment:**

`app.yaml`:
```yaml
runtime: python311

env_variables:
  OPENAI_API_KEY: "your_key_here"

automatic_scaling:
  min_instances: 1
  max_instances: 10

resources:
  cpu: 1
  memory_gb: 0.5
  disk_size_gb: 10
```

**Deploy:**
```bash
# Install Google Cloud SDK
# Configure authentication

# Deploy
gcloud app deploy
```

## Environment Configuration

### Environment Variables

**Required:**
- `OPENAI_API_KEY`: OpenAI API key (optional but recommended)

**Optional:**
- `FLASK_ENV`: Environment mode (development/production)
- `FLASK_DEBUG`: Debug mode (True/False)
- `PORT`: Server port (default: 5000)
- `USE_OPENAI_EMBEDDINGS`: Use OpenAI embeddings (True/False)
- `MODEL_NAME`: OpenAI model name (default: gpt-3.5-turbo)
- `MAX_TOKENS`: Maximum response tokens (default: 500)

### Configuration Files

**Production `.env`:**
```env
OPENAI_API_KEY=sk-your-production-key-here
FLASK_ENV=production
FLASK_DEBUG=False
PORT=5000
USE_OPENAI_EMBEDDINGS=False
MODEL_NAME=gpt-3.5-turbo
MAX_TOKENS=500
```

**Development `.env`:**
```env
OPENAI_API_KEY=sk-your-development-key-here
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
USE_OPENAI_EMBEDDINGS=False
MODEL_NAME=gpt-3.5-turbo
MAX_TOKENS=500
```

## Production Considerations

### Performance Optimization

1. **Use Production WSGI Server:**
   ```bash
   # Gunicorn (recommended)
   gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
   
   # uWSGI
   uwsgi --http :5000 --wsgi-file app.py --callable app
   ```

2. **Enable Caching:**
   ```python
   # Add to app.py
   from flask_caching import Cache
   
   cache = Cache(app, config={'CACHE_TYPE': 'simple'})
   
   @cache.memoize(timeout=300)
   def cached_vector_search(query):
       return vector_store.search(query)
   ```

3. **Database Optimization:**
   - Use persistent storage for vector store
   - Implement connection pooling
   - Add database indexing

### Security

1. **HTTPS Configuration:**
   ```nginx
   # nginx.conf
   server {
       listen 443 ssl;
       server_name your-domain.com;
       
       ssl_certificate /path/to/certificate.crt;
       ssl_certificate_key /path/to/private.key;
       
       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

2. **Environment Security:**
   - Use secure environment variable management
   - Implement API rate limiting
   - Add input validation and sanitization
   - Enable CORS properly

3. **Secrets Management:**
   ```bash
   # Use cloud provider secret managers
   # AWS Secrets Manager
   aws secretsmanager get-secret-value --secret-id openai-api-key
   
   # Google Secret Manager
   gcloud secrets versions access latest --secret="openai-api-key"
   ```

### Monitoring and Logging

1. **Application Monitoring:**
   ```python
   # Add to app.py
   import logging
   from logging.handlers import RotatingFileHandler
   
   if not app.debug:
       file_handler = RotatingFileHandler('logs/chatbot.log', maxBytes=10240, backupCount=10)
       file_handler.setFormatter(logging.Formatter(
           '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
       ))
       file_handler.setLevel(logging.INFO)
       app.logger.addHandler(file_handler)
   ```

2. **Health Checks:**
   ```python
   @app.route('/health')
   def health_check():
       return jsonify({
           'status': 'healthy',
           'timestamp': datetime.utcnow().isoformat(),
           'version': '1.0.0'
       })
   ```

3. **Metrics Collection:**
   ```python
   # Add Prometheus metrics
   from prometheus_flask_exporter import PrometheusMetrics
   
   metrics = PrometheusMetrics(app)
   metrics.info('app_info', 'Application info', version='1.0.0')
   ```

### Scaling

1. **Horizontal Scaling:**
   - Use load balancers
   - Implement session management
   - Share vector store across instances

2. **Vertical Scaling:**
   - Optimize memory usage
   - Use efficient data structures
   - Implement lazy loading

3. **Auto-scaling Configuration:**
   ```yaml
   # Kubernetes HPA
   apiVersion: autoscaling/v2
   kind: HorizontalPodAutoscaler
   metadata:
     name: chatbot-hpa
   spec:
     scaleTargetRef:
       apiVersion: apps/v1
       kind: Deployment
       name: chatbot-deployment
     minReplicas: 2
     maxReplicas: 10
     metrics:
     - type: Resource
       resource:
         name: cpu
         target:
           type: Utilization
           averageUtilization: 70
   ```

## Troubleshooting

### Common Deployment Issues

1. **Module Import Errors:**
   ```bash
   # Check Python path
   export PYTHONPATH="${PYTHONPATH}:/app/src"
   ```

2. **Missing Dependencies:**
   ```bash
   # Verify all dependencies are installed
   pip freeze > current_requirements.txt
   diff requirements.txt current_requirements.txt
   ```

3. **Port Binding Issues:**
   ```python
   # Use environment port
   port = int(os.environ.get('PORT', 5000))
   app.run(host='0.0.0.0', port=port)
   ```

4. **Vector Store Not Found:**
   ```bash
   # Rebuild vector store
   python src/data_processing/rebuild_lightweight_store.py
   ```

### Debugging Production Issues

1. **Enable Debug Logging:**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Check System Resources:**
   ```bash
   # Monitor memory and CPU
   htop
   free -h
   df -h
   ```

3. **Application Logs:**
   ```bash
   # View application logs
   tail -f logs/chatbot.log
   
   # Railway logs
   railway logs
   
   # Heroku logs
   heroku logs --tail
   ```

## Maintenance

### Regular Updates

1. **Dependency Updates:**
   ```bash
   # Check for outdated packages
   pip list --outdated
   
   # Update packages
   pip install --upgrade package_name
   ```

2. **Security Updates:**
   ```bash
   # Check for security vulnerabilities
   pip audit
   
   # Update security patches
   pip install --upgrade package_name
   ```

3. **Data Updates:**
   ```bash
   # Refresh scraped content
   python src/data_processing/website_scraper.py
   python src/data_processing/rebuild_lightweight_store.py
   ```

### Backup and Recovery

1. **Data Backup:**
   ```bash
   # Backup data directory
   tar -czf backup_$(date +%Y%m%d).tar.gz data/
   ```

2. **Configuration Backup:**
   ```bash
   # Backup configuration
   cp .env .env.backup
   cp deployment/railway.json deployment/railway.json.backup
   ```

3. **Recovery Procedures:**
   ```bash
   # Restore from backup
   tar -xzf backup_20240115.tar.gz
   cp .env.backup .env
   ```