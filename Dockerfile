FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

ENV CHROMIUM_PATH=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

ENV PORT=8080

CMD gunicorn --bind 0.0.0.0:$PORT app:app

