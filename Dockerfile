FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required for mysqlclient
# and create a non-root user in a single layer
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        default-libmysqlclient-dev \
        pkg-config \
    && addgroup --system app \
    && adduser --system --ingroup app app \
    && rm -rf /var/lib/apt/lists/*


# Install Python dependencies (better layer caching)
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files (make sure .dockerignore excludes secrets like .env)
# Copy only application code explicitly
COPY manage.py /app/
COPY core /app/core
COPY app /app/app


# Fix permissions for non-root user
RUN chown -R app:app /app

USER app

# Render provides $PORT. Use gunicorn for production.
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3"]
