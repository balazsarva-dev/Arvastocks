FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY requirements.txt .
COPY entrypoint.sh .
COPY async_main.py .
COPY crontab /etc/cron.d/async_data_downloader
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set permissions for scripts
RUN chmod +x entrypoint.sh async_main.py

ENTRYPOINT ["./entrypoint.sh"]