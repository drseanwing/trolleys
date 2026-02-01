# Multi-stage build for Django application
FROM python:3.12-slim AS base

# Security: run as non-root
RUN groupadd -r app && useradd -r -g app -d /app -s /sbin/nologin app

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application and entrypoint
COPY backend/ .
COPY seed_data/ /app/seed_data/
COPY docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set ownership
RUN chown -R app:app /app

USER app

EXPOSE 11000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:11000", "--workers", "4", "--timeout", "120", "redi.wsgi:application"]
