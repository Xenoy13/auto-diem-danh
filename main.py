import asyncio
import os
import datetime
from playwright.async_api import async_playwright
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import schedule
import time
import threading

# === CẤU HÌNH CƠ BẢN ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
EMAIL = os.getenv("EMAIL", "hieucyberwork@gmail.com")
URL = "https://hoctot365.odoo.com/b2102454623412645095758715465195974579457497457469754674279454545454545454545454545454545642167529745794514"

# === HÀM ĐIỂM DANH CHÍNH ===
async def perform_checkin():
    print(f"[INFO] {datetime.datetime.now()} | Đang mở trang điểm danh...")

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(URL, wait_until="networkidle")

            # Điền email
            await page.fill('input[placeholder*="Nhập email"]', EMAIL)
            await page.click('button:has-text("Xác nhận Điểm danh")')
            await page.wait_for_timeout(5000)

            # Chụp ảnh kết quả
            await page.screenshot(path="checkin_result.png")

            print("✅ Điểm danh thành công!")
            await browser.close()
            return True

    except Exception as e:
        print(f"❌ Lỗi khi điểm danh: {e}")
        return False


# === GỬI KẾT QUẢ CHO TELEGRAM ===
async def send_message(app, text, image_path=None):
    if image_path and os.path.exists(image_path):
        await app.bot.send_photo(chat_id=CHAT_ID, photo=InputFile(image_path), caption=text)
    else:
        await app.bot.send_message(chat_id=CHAT_ID, text=text)


# === LỆNH /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot đã sẵn sàng! Gõ /run để điểm danh ngay hoặc đợi tự động lúc 00:00.")


# === LỆNH /run: Điểm danh thủ công ===
async def run(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🕒 Bắt đầu điểm danh ngay...")
    success = await perform_checkin()
    if success:
        await update.message.reply_text("✅ Điểm danh thành công! Ảnh kết quả đang được gửi...")
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("checkin_result.png", "rb"))
    else:
        await update.message.reply_text("❌ Lỗi khi điểm danh. Vui lòng kiểm tra lại!")


# === LỆNH /status: Kiểm tra trạng thái bot ===
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📌 Bot vẫn đang hoạt động bình thường và chờ tới 00:00 để điểm danh.")


# === HÀM ĐIỂM DANH TỰ ĐỘNG MỖI NGÀY ===
def schedule_checkin(app):
    async def task():
        await send_message(app, "🕛 Tự động điểm danh lúc 00:00...")
        result = await perform_checkin()
        if result:
            await send_message(app, "✅ Tự động điểm danh thành công!", "checkin_result.png")
        else:
            await send_message(app, "❌ Lỗi khi tự động điểm danh!")

    schedule.every().day.at("00:00").do(lambda: asyncio.run(task()))

    while True:
        schedule.run_pending()
        time.sleep(30)


# === KHỞI CHẠY BOT TELEGRAM ===
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("run", run))
    app.add_handler(CommandHandler("status", status))

    threading.Thread(target=schedule_checkin, args=(app,), daemon=True).start()

    print("🤖 Bot Telegram đã khởi động!")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
