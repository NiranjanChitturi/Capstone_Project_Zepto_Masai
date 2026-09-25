# ---------------------------------------------------------------------------
# Module 3 - Zepto Support Assistant
# FastAPI Docker image
# ---------------------------------------------------------------------------

FROM python:3.12-slim

# Prevent Python from creating .pyc files and buffer output.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Application working directory.
WORKDIR /app

# Copy only the Docker-specific dependency file.
COPY support_assistant/docker-requirements.txt /app/docker-requirements.txt

# Install Python dependencies.
#
# The requirements file points PyTorch to the CPU-only package repository.
# This avoids downloading the unnecessary CUDA dependency stack.
RUN pip install --no-cache-dir -r /app/docker-requirements.txt

# Copy the complete Module 3 application.
COPY support_assistant /app/support_assistant

# Build the local ChromaDB knowledge base inside the image.
#
# This loads the eight required policy documents and creates embeddings
# using all-MiniLM-L6-v2.
RUN python support_assistant/src/ingest.py

# FastAPI listens on port 8000.
EXPOSE 8000

# Start the FastAPI application.
CMD ["uvicorn", "support_assistant.src.api:app", "--host", "0.0.0.0", "--port", "8000"]