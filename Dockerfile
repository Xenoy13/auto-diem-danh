# Sử dụng image Python chính thức
FROM python:3.12-slim

# Cài các gói hệ thống cần thiết
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libx11-xcb1 \
    fonts-liberation \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Cài Playwright và trình duyệt Chromium
RUN pip install playwright && playwright install chromium

# Copy toàn bộ code vào container
WORKDIR /app
COPY . .

# Cài thêm các thư viện Python của bạn
RUN pip install -r requirements.txt

# Chạy ứng dụng
CMD ["python", "main.py"]
