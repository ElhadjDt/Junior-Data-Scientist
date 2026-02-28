# CARMS Data Platform API — containerized FastAPI backend.
# Build from carms-data-platform-demo directory: docker build -t carms-api .
# Override DATABASE_URL and FAISS_PATH at runtime for AWS/stack deployment.
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY src ./src
COPY .env.example .env.example

# Default env (override with docker-compose or ECS task def)
ENV PYTHONPATH=/app
ENV DATA_DIR=/data
ENV FAISS_PATH=/data/embeddings/faiss_index

EXPOSE 8000

# Run FastAPI with uvicorn
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
