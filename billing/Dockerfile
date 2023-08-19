# Используем официальный образ Python 3.11
FROM python:3.11.3-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python-dev \
    cron && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/artefacts

RUN chown -R 1000:1000 /app/artefacts

ENTRYPOINT ["python", "main.py"]
