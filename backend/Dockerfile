FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
COPY entrypoint.sh .
COPY async_main.py .
COPY crontab /etc/cron.d/async_data_downloader

COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    cron && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /app/entrypoint.sh  # Add execute permissions
RUN chmod +x /app/async_main.py  # Add execute permissions
RUN chmod 0644 /etc/cron.d/async_data_downloader  # Add read permissions

EXPOSE 5000

ENTRYPOINT ["/app/entrypoint.sh"]
