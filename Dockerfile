FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for mysqlclient
RUN apt-get update \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
