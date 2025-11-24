# Deployment Guide - Mini Memori

Guide for deploying Mini Memori in various environments.

## Table of Contents

1. [Local Deployment](#local-deployment)
2. [Server Deployment](#server-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Production Considerations](#production-considerations)

---

## Local Deployment

### For Personal Use

1. **Install the package**:
```bash
pip install -e .
```

2. **Set up environment**:
```bash
export OPENAI_API_KEY=your_key_here
```

3. **Run the chatbot**:
```bash
python -m mini_memori.chatbot
```

### For Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for complete development setup.

---

## Server Deployment

### Linux Server

#### 1. System Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.8+
sudo apt install python3.10 python3-pip python3-venv -y

# Create application directory
sudo mkdir -p /opt/mini-memori
sudo chown $USER:$USER /opt/mini-memori
cd /opt/mini-memori
```

#### 2. Application Setup

```bash
# Clone repository
git clone https://github.com/yourusername/mini-memori.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .
```

#### 3. Configuration

```bash
# Create .env file
cat > .env << EOF
OPENAI_API_KEY=your_key_here
DB_PATH=/opt/mini-memori/data/memories.db
LOG_LEVEL=INFO
EOF

# Create data directory
mkdir -p data
chmod 755 data
```

#### 4. Systemd Service (Optional)

Create `/etc/systemd/system/mini-memori.service`:

```ini
[Unit]
Description=Mini Memori Service
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/opt/mini-memori
Environment="PATH=/opt/mini-memori/venv/bin"
EnvironmentFile=/opt/mini-memori/.env
ExecStart=/opt/mini-memori/venv/bin/python -m mini_memori.chatbot
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable mini-memori
sudo systemctl start mini-memori
```

---

## Docker Deployment

### Dockerfile

Create `Dockerfile`:

```dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY mini_memori/ ./mini_memori/
COPY setup.py .
COPY README.md .

# Install package
RUN pip install -e .

# Create data directory
RUN mkdir -p /data

# Set environment variables
ENV DB_PATH=/data/memories.db

# Expose port (if building web interface)
# EXPOSE 8000

# Run chatbot
CMD ["python", "-m", "mini_memori.chatbot"]
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  mini-memori:
    build: .
    container_name: mini-memori
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DB_PATH=/data/memories.db
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/data
    restart: unless-stopped
    stdin_open: true
    tty: true
```

### Build and Run

```bash
# Build image
docker build -t mini-memori:latest .

# Run container
docker run -it \
  -e OPENAI_API_KEY=your_key \
  -v $(pwd)/data:/data \
  mini-memori:latest

# Or use docker-compose
docker-compose up -d
```

---

## Cloud Deployment

### AWS EC2

#### 1. Launch EC2 Instance

- AMI: Ubuntu 22.04 LTS
- Instance Type: t3.small or larger
- Storage: 20GB minimum
- Security Group: Allow SSH (22)

#### 2. Connect and Setup

```bash
# Connect
ssh -i your-key.pem ubuntu@your-instance-ip

# Install dependencies
sudo apt update && sudo apt install python3-pip python3-venv git -y

# Clone and setup
git clone https://github.com/yourusername/mini-memori.git
cd mini-memori
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Configure
echo "OPENAI_API_KEY=your_key" > .env

# Run
python -m mini_memori.chatbot
```

#### 3. Auto-Start (systemd)

Follow the systemd service setup from the Linux Server section.

### AWS Lambda (API Gateway)

Create `lambda_handler.py`:

```python
import json
import os
from mini_memori import MemoryEngine

# Initialize engine once (outside handler)
engine = MemoryEngine(
    db_path="/tmp/memories.db",  # Lambda tmp storage
    api_key=os.environ['OPENAI_API_KEY']
)

def lambda_handler(event, context):
    """Handle API Gateway requests."""
    try:
        body = json.loads(event['body'])
        action = body.get('action')
        
        if action == 'save':
            msg_id = engine.save_message(
                role=body['role'],
                content=body['content'],
                conversation_id=body.get('conversation_id', 'default')
            )
            return {
                'statusCode': 200,
                'body': json.dumps({'message_id': msg_id})
            }
            
        elif action == 'retrieve':
            memories = engine.retrieve_memories(
                query=body['query'],
                top_k=body.get('top_k', 5)
            )
            return {
                'statusCode': 200,
                'body': json.dumps({'memories': memories})
            }
            
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid action'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

### Heroku

Create `Procfile`:

```
web: python -m mini_memori.chatbot
```

Deploy:

```bash
# Login
heroku login

# Create app
heroku create your-app-name

# Set config
heroku config:set OPENAI_API_KEY=your_key

# Deploy
git push heroku main
```

### Google Cloud Run

#### 1. Create `Dockerfile` (see Docker section)

#### 2. Deploy

```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/your-project/mini-memori

# Deploy to Cloud Run
gcloud run deploy mini-memori \
  --image gcr.io/your-project/mini-memori \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=your_key
```

---

## Production Considerations

### 1. Security

#### Environment Variables
```bash
# Never commit .env files
echo ".env" >> .gitignore

# Use secrets management
# AWS: Secrets Manager
# GCP: Secret Manager
# Azure: Key Vault
```

#### API Key Rotation
```python
# Implement key rotation
def get_api_key():
    """Fetch API key from secure storage."""
    # AWS example:
    import boto3
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId='openai-api-key')
    return response['SecretString']
```

### 2. Performance

#### Database Optimization
```python
# Use connection pooling for high traffic
from mini_memori import MemoryEngine

# Create singleton instance
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = MemoryEngine()
    return _engine
```

#### Caching
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_retrieval(query: str, top_k: int):
    """Cache frequent queries."""
    return engine.retrieve_memories(query, top_k=top_k)
```

### 3. Monitoring

#### Logging
```python
import logging

# Configure production logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/mini-memori.log'),
        logging.StreamHandler()
    ]
)
```

#### Metrics
```python
import time

def track_operation(operation_name):
    """Decorator to track operation metrics."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start
                logging.info(f"{operation_name} completed in {duration:.2f}s")
                return result
            except Exception as e:
                logging.error(f"{operation_name} failed: {e}")
                raise
        return wrapper
    return decorator

@track_operation("memory_retrieval")
def retrieve_memories(query):
    return engine.retrieve_memories(query)
```

### 4. Backup

#### Database Backup
```bash
#!/bin/bash
# backup.sh

DB_PATH="/opt/mini-memori/data/memories.db"
BACKUP_DIR="/opt/mini-memori/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup
sqlite3 $DB_PATH ".backup '$BACKUP_DIR/memories_$DATE.db'"

# Keep only last 7 days
find $BACKUP_DIR -name "memories_*.db" -mtime +7 -delete

echo "Backup completed: memories_$DATE.db"
```

Add to crontab:
```bash
# Run daily at 2 AM
0 2 * * * /opt/mini-memori/backup.sh
```

### 5. High Availability

#### Load Balancing
```yaml
# docker-compose.yml for multiple instances
version: '3.8'

services:
  mini-memori:
    image: mini-memori:latest
    deploy:
      replicas: 3
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - shared-data:/data

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - mini-memori

volumes:
  shared-data:
```

### 6. Cost Optimization

#### OpenAI API Usage
```python
# Batch embeddings when possible
def save_messages_batch(messages):
    """Save multiple messages with batched embeddings."""
    # Save all messages first
    message_ids = []
    for role, content, conv_id in messages:
        msg_id = engine.save_message(
            role, content, conv_id, 
            generate_embedding=False
        )
        message_ids.append((msg_id, content))
    
    # Generate embeddings in batch
    contents = [content for _, content in message_ids]
    embeddings = engine.embeddings.generate_embeddings_batch(contents)
    
    # Save embeddings
    for (msg_id, _), embedding in zip(message_ids, embeddings):
        engine.db.save_embedding(msg_id, embedding, engine.embedding_model)
```

---

## Health Checks

### Basic Health Check

```python
# health_check.py
from mini_memori import MemoryEngine

def health_check():
    """Check system health."""
    try:
        engine = MemoryEngine()
        stats = engine.get_statistics()
        engine.close()
        return {
            'status': 'healthy',
            'messages': stats['total_messages'],
            'conversations': stats['total_conversations']
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e)
        }

if __name__ == '__main__':
    import json
    print(json.dumps(health_check()))
```

---

## Support

For deployment issues:
- Check logs: `journalctl -u mini-memori` (systemd)
- Docker logs: `docker logs mini-memori`
- AWS CloudWatch, GCP Stackdriver, etc.

For questions:
- GitHub Issues
- Documentation
- Community forums

---

**Production Checklist:**

- [ ] Environment variables configured
- [ ] API keys secured (not in code)
- [ ] Database backups configured
- [ ] Logging enabled
- [ ] Monitoring setup
- [ ] Error handling implemented
- [ ] Rate limiting considered
- [ ] Security hardened
- [ ] Documentation updated
- [ ] Health checks working

Good luck with your deployment! 🚀
