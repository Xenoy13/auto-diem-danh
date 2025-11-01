# ===== DÙNG DEBIAN CHO CHẮC CHẮN =====
FROM mcr.microsoft.com/playwright/python:v1.49.0-jammy

# ===== CÀI CÁC GÓI BỔ TRỢ =====
RUN apt-get update && apt-get install -y \
    fonts-noto-color-emoji \
    fonts-noto-cjk \
    libglib2.0-0 libnss3 libatk1.0-0 libcups2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libasound2 libpangocairo-1.0-0 libcairo2 \
    && rm -rf /var/lib/apt/lists/*

# ===== SAO CHÉP TOÀN BỘ CODE =====
WORKDIR /app
COPY . .

# ===== CÀI DEPENDENCIES PYTHON =====
RUN pip install --no-cache-dir -r requirements.txt

# ===== CÀI BROWSER =====
RUN playwright install chromium

# ===== CHẠY BOT =====
CMD ["python", "main.py"]
