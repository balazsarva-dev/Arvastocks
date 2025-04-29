FROM python:3.9-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
COPY entrypoint.sh ./
COPY async_main.py ./
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x entrypoint.sh async_main.py

ENTRYPOINT ["./entrypoint.sh"]