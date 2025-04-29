FROM python:3.9-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x entrypoint.sh async_main.py

ENTRYPOINT ["./entrypoint.sh"]