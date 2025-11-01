import os
import time
import asyncio
from playwright.async_api import async_playwright
from telegram import Bot

# Biến môi trường
EMAIL = os.getenv("EMAIL", "hieucyberwork@gmail.com")
CHECKIN_URL = "https://hoctot365.odoo.com/b2102454623412645095758715465195974579457497457469754674279454545454545454545454545454545642167529745794514"
CHAT_ID = os.getenv("CHAT_ID")  # ID Telegram Chat của bạn
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Token bot Telegram

async def check_in():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = await browser.new_page()
        print("[INFO] Đang mở trang điểm danh...")

        await page.goto(CHECKIN_URL, timeout=60000)
        await asyncio.sleep(3)

        # Điền Gmail
        await page.fill('input[placeholder*="Nhập email"]', EMAIL)
        await page.click('button:has-text("Xác nhận Điểm danh")')

        # Chờ phản hồi hiển thị (text thành công hoặc alert)
        await asyncio.sleep(5)

        # Chụp ảnh kết quả
        await page.screenshot(path="checkin_result.png", full_page=True)
        print("[INFO] Đã chụp ảnh kết quả.")

        await browser.close()

async def send_to_telegram():
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text="✅ Điểm danh hoàn tất!")
    with open("checkin_result.png", "rb") as img:
        await bot.send_photo(chat_id=CHAT_ID, photo=img)

async def main():
    try:
        await check_in()
        await send_to_telegram()
    except Exception as e:
        print(f"[ERROR] Lỗi khi điểm danh: {e}")

if __name__ == "__main__":
    asyncio.run(main())
