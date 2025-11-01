import os
import asyncio
from playwright.async_api import async_playwright
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHECKIN_URL = "https://hoctot365.odoo.com/b2102454623412645095758715465195974579457497457469754674279454545454545454545454545454545642167529745794514"
EMAIL = "hieucyberwork@gmail.com"

async def checkin():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(CHECKIN_URL)

        await page.wait_for_selector("input[placeholder*='Nhập email']", timeout=20000)
        await page.fill("input[placeholder*='Nhập email']", EMAIL)
        await page.click("button:has-text('Xác nhận Điểm danh')")
        await page.wait_for_timeout(3000)

        content = await page.content()
        await browser.close()
        if "điểm danh thành công" in content.lower():
            return "✅ Điểm danh thành công!"
        else:
            return "⚠️ Không chắc điểm danh thành công, kiểm tra lại trang web."

async def run_checkin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🕐 Bắt đầu điểm danh ngay...")
    try:
        result = await checkin()
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"❌ Lỗi điểm danh: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot đã sẵn sàng! Gõ /run để điểm danh ngay hoặc đợi tự động lúc 00:00.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("run", run_checkin))
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
