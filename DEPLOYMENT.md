# Docker Deployment Guide

## Quick Start

### Using Docker directly:
```bash
# Build image
docker build -t credit-scoring-model .

# Run container
docker run -d -p 8000:8000 --name credit-scoring-api credit-scoring-model

# Check status
docker ps

# View logs
docker logs -f credit-scoring-api

# Stop container
docker stop credit-scoring-api
docker rm credit-scoring-api