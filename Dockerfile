# Use Python 3.12 as base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ENVIRONMENT=production \
    PORT=8000

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements/base.txt .
COPY requirements/api.txt .
RUN pip install --no-cache-dir -r api.txt

# Install the package in development mode (for local source access)
COPY . .
RUN pip install -e .

# Create directory for database files
RUN mkdir -p /app/api/db && chmod 755 /app/api/db

# Download GeoIP databases (with redirect following)
RUN curl -L -o /app/api/db/GeoLite2-City.mmdb https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-City.mmdb \
    && curl -L -o /app/api/db/GeoLite2-ASN.mmdb https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-ASN.mmdb

# Expose port
EXPOSE ${PORT}

# Start the API
CMD uvicorn api.main:app --host 0.0.0.0 --port ${PORT}