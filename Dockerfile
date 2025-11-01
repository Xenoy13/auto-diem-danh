FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    wget gnupg ca-certificates fonts-liberation libnss3 libxkbcommon0 libxcomposite1 \
    libxdamage1 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2 libxshmfence1 \
    libxext6 libx11-6 libatk-bridge2.0-0 libdrm2 libgtk-3-0 libglib2.0-0 libnss3-tools && \
    pip install --no-cache-dir -r requirements.txt && \
    playwright install chromium

CMD ["python", "main.py"]
