# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
COPY setup.py .

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Command to run the app with Gunicorn
CMD ["gunicorn", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "api.optimized_app:app", \
     "-b", "0.0.0.0:8000", \
     "--workers", "4", \
     "--timeout", "120"] 