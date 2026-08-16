# Build Stage
FROM python:3.11-slim as builder

# Install uv
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml pyproject.toml
COPY README.md README.md
COPY src/ src/

# Create virtual environment and install dependencies using uv
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN uv pip install -e .

# Runtime Stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set environment variables
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Copy project files
COPY --from=builder /app/src /app/src
COPY --from=builder /app/pyproject.toml /app/pyproject.toml
COPY --from=builder /app/README.md /app/README.md

# Create necessary directories
RUN mkdir -p /app/data /app/logs

# Copy .env.example as template (optional)
COPY .env.example .env.example 2>/dev/null || true

# Expose ports
# Streamlit default port
EXPOSE 8501
# Optional: for API/other services
EXPOSE 8000

# Health check for Streamlit
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8501')" || exit 1

# Default command - runs Streamlit web interface
CMD ["uv", "run", "streamlit", "run", "src/ai_etl_agent/app.py", "--server.port=8501", "--server.address=0.0.0.0"]