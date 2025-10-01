FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Create non-root user
RUN useradd -m appuser

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt 

COPY . .
RUN mkdir -p /home/appuser/.streamlit && \
    cp .streamlit/config.toml /home/appuser/.streamlit/config.toml && \
    chown -R appuser:appuser /app /home/appuser/.streamlit

USER appuser
EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
 