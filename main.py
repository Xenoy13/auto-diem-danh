import os
import time
import requests
import schedule
from playwright.sync_api import sync_playwright
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 🔹 Lấy token và chat ID từ biến môi trường trên Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 🔹 Thông tin điểm danh
EMAIL = "hieucyberwork@gmail.com"
URL = "https://hoctot365.odoo.com/b2102454623412645095758715465195974579457497457469754674279454545454545454545454545454545642167529745794514"


# Hàm gửi thông báo về Telegram
def send_message(msg):
    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
    except Exception as e:
        print(f"[Lỗi gửi tin nhắn Telegram]: {e}")


# Hàm chính để điểm danh
def diem_danh():
    try:
        send_message("🤖 Đang tiến hành điểm danh...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(URL, timeout=60000)
            page.wait_for_selector("input[placeholder*='Nhập email']", timeout=30000)
            page.fill("input[placeholder*='Nhập email']", EMAIL)
            page.click("button:has-text('Xác nhận')")
            page.wait_for_timeout(4000)
            send_message(f"✅ Điểm danh thành công cho {EMAIL}")
            browser.close()
    except Exception as e:
        send_message(f"❌ Lỗi điểm danh: {e}")


# 📅 Lên lịch điểm danh tự động mỗi ngày
schedule.every().day.at("00:00").do(diem_danh)


# 🧠 Các lệnh Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot đã sẵn sàng! Gõ /run để điểm danh ngay hoặc đợi tự động lúc 00:00.")


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🕒 Bắt đầu điểm danh ngay...")
    diem_danh()


# 🚀 Khởi chạy bot Telegram
async def scheduler():
    while True:
        schedule.run_pending()
        await asyncio.sleep(10)


if __name__ == "__main__":
    import asyncio

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Thêm các lệnh Telegram
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("run", run))  # ⬅️ Lệnh bạn cần!

    # Chạy song song scheduler và bot
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    app.run_polling()
