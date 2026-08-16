# Docker Setup Guide for AI ETL Agent

This guide explains how to run the AI ETL Agent using Docker and Docker Compose.

## 📋 Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)

## 🚀 Quick Start

### Using Docker Compose (Recommended)

1. **Setup Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   nano .env  # or use your preferred editor
   ```

2. **Start the Application**
   ```bash
   docker-compose up -d
   ```

3. **Access the Web UI**
   Open your browser to: `http://localhost:8501`

4. **View Logs**
   ```bash
   docker-compose logs -f ai-etl-agent
   ```

5. **Stop the Application**
   ```bash
   docker-compose down
   ```

---

## 🐳 Using Docker Directly

### Build the Image

```bash
docker build -t ai-etl-agent:latest .
```

### Run the Container

#### Streamlit Web UI (Default)
```bash
docker run -p 8501:8501 \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  ai-etl-agent:latest
```

#### CLI Mode
```bash
docker run -it \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  ai-etl-agent:latest \
  uv run python src/ai_etl_agent/main.py
```

### Run with Custom Configuration
```bash
docker run -p 8501:8501 \
  -e GROQ_API_KEY=your_key \
  -e SNOWFLAKE_ACCOUNT=your_account \
  -v $(pwd)/data:/app/data \
  ai-etl-agent:latest
```

---

## 📁 Docker Files Overview

### Dockerfile
**Multi-stage build** for optimized image size:
- **Builder Stage**: Installs `uv` and dependencies
- **Runtime Stage**: Minimal runtime with only necessary files

**Key Features:**
- Uses Python 3.11 slim base image
- Installs dependencies via `uv` (faster than pip)
- Exposes ports 8501 (Streamlit) and 8000 (Optional API)
- Includes health check
- Runs Streamlit by default

### docker-compose.yml
**Complete development setup** with:
- Volume mounting for live code updates
- Environment variable management
- Resource limits
- Health checks
- Restart policies
- Optional ChromaDB service (commented out)

### .dockerignore
**Optimizes build context** by excluding:
- Virtual environments
- Git files
- Python cache
- Test files
- Development files

---

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

**Required:**
- `GROQ_API_KEY` - Your Groq API key

**Optional (depending on usage):**
- `SNOWFLAKE_*` - For Snowflake integration
- `DATABRICKS_*` - For Databricks integration
- `SQLITE_DB_PATH` - For SQLite configuration

### Port Mapping

```
8501  → Streamlit Web UI
8000  → Optional API endpoint
```

Modify in `docker-compose.yml` if needed:
```yaml
ports:
  - "8501:8501"  # Change first number for external port
  - "8000:8000"
```

---

## 📝 Common Commands

### Start Development Environment
```bash
docker-compose up -d
```

### Rebuild Image (after code/dependency changes)
```bash
docker-compose up -d --build
```

### Stop All Containers
```bash
docker-compose down
```

### Stop and Remove Volumes
```bash
docker-compose down -v
```

### View Container Logs
```bash
docker-compose logs -f ai-etl-agent
```

### Execute Command in Running Container
```bash
docker-compose exec ai-etl-agent uv run python src/ai_etl_agent/main.py
```

### View Container Resource Usage
```bash
docker stats
```

### Shell Access to Container
```bash
docker-compose exec ai-etl-agent /bin/bash
```

---

## 🔍 Troubleshooting

### Container Won't Start

**Check logs:**
```bash
docker-compose logs ai-etl-agent
```

**Common Issues:**
- Missing `.env` file → `cp .env.example .env`
- Invalid credentials → Check API keys in `.env`
- Port already in use → Change port in `docker-compose.yml`

### Build Fails

**Clear cache and rebuild:**
```bash
docker-compose down
docker system prune -a
docker-compose up -d --build
```

### Slow Build

**Use BuildKit for faster builds:**
```bash
DOCKER_BUILDKIT=1 docker build -t ai-etl-agent:latest .
```

### Out of Memory

**Increase Docker memory:**
- Docker Desktop: Preferences → Resources → Memory
- Or modify limits in `docker-compose.yml`:
  ```yaml
  deploy:
    resources:
      limits:
        memory: 8G  # Increase as needed
  ```

### Connection Issues

**Verify networking:**
```bash
docker-compose exec ai-etl-agent curl http://localhost:8501
```

---

## 🚢 Production Deployment

### Build for Production
```bash
docker build -t ai-etl-agent:prod --build-arg BUILDKIT_INLINE_CACHE=1 .
```

### Push to Registry
```bash
docker tag ai-etl-agent:prod yourusername/ai-etl-agent:latest
docker push yourusername/ai-etl-agent:latest
```

### Use Environment File for Secrets
```bash
# Create secure .env file
echo "GROQ_API_KEY=your_production_key" > .env.prod
docker run --env-file .env.prod ai-etl-agent:prod
```

### Run with Limited Resources
```yaml
# In docker-compose.yml
deploy:
  resources:
    limits:
      cpus: '1'
      memory: 2G
```

---

## 🐳 Docker Hub / Registry

### Save Image as Tarball
```bash
docker save ai-etl-agent:latest > ai-etl-agent.tar
```

### Load Image from Tarball
```bash
docker load < ai-etl-agent.tar
```

---

## 📊 Monitoring

### Container Stats
```bash
docker stats ai-etl-agent
```

### View Health Status
```bash
docker ps  # Check STATUS column
```

### Continuous Monitoring
```bash
watch -n 2 'docker stats --no-stream'
```

---

## 🧹 Cleanup

### Remove All Containers
```bash
docker-compose down
```

### Remove Unused Images
```bash
docker image prune -a
```

### Remove All Dangling Volumes
```bash
docker volume prune
```

### Full System Cleanup
```bash
docker system prune -a --volumes
```

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best Practices for Python Docker Images](https://docs.docker.com/language/python/build-images/)
- [uv Documentation](https://docs.astral.sh/uv/)

---

## 🤝 Tips

1. **Use `.dockerignore`** to exclude unnecessary files → faster builds
2. **Use multi-stage builds** → smaller final images
3. **Use `docker-compose`** → easier local development
4. **Pin dependency versions** → reproducible builds
5. **Use health checks** → automatic container management
6. **Mount volumes** → live code updates during development
7. **Use BuildKit** → faster parallel builds

---

**Last Updated**: 2026-08-16
