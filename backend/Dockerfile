# Use slim Python image
FROM python:3.13-slim

# Prevent prompts from tzdata etc.
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies for OCR and PDF processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-fra \
    tesseract-ocr-deu \
    tesseract-ocr-hun \
    poppler-utils \
    ghostscript \
    fonts-dejavu-core \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY . .

# Expose port (Heroku dynamically sets PORT env)
EXPOSE 10000

# Set environment defaults
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

# Launch FastAPI app
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]

