import os
import time
import schedule
import threading
from datetime import datetime
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CHECKIN_URL = os.getenv("CHECKIN_URL")
GMAIL = os.getenv("GMAIL")

bot = Bot(token=TELEGRAM_TOKEN)

def send_message(msg):
    bot.send_message(chat_id=CHAT_ID, text=msg)

def send_photo(image_path):
    bot.send_photo(chat_id=CHAT_ID, photo=open(image_path, 'rb'))

def check_in():
    send_message("🔄 Đang điểm danh...")

    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1280,720")
        chrome_options.binary_location = "/usr/bin/chromium-browser"  # FIX BINARY LOCATION

        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get(CHECKIN_URL)
        time.sleep(3)

        # Nhập Gmail
        email_input = driver.find_element(By.XPATH, "//input[@type='email']")
        email_input.send_keys(GMAIL)
        time.sleep(1)

        # Bấm nút xác nhận điểm danh
        button = driver.find_element(By.XPATH, "//button")
        button.click()
        time.sleep(3)

        # Chụp ảnh xác nhận
        image_path = "/tmp/diemdanh.png"
        driver.save_screenshot(image_path)
        send_photo(image_path)

        send_message(f"✅ Điểm danh thành công lúc {datetime.now().strftime('%H:%M:%S')}")

        driver.quit()

    except Exception as e:
        send_message(f"❌ Lỗi điểm danh: {str(e)}")

def settime(update, context):
    try:
        time_str = context.args[0]
        schedule.clear()
        schedule.every().day.at(time_str).do(check_in)
        send_message(f"⏰ Đã đổi giờ điểm danh thành {time_str}")
    except:
        send_message("⚠ Dùng đúng: /settime HH:MM")

def status(update, context):
    send_message("🤖 Bot đang chạy!\n⏲ Giờ điểm danh hiện tại: tự động mỗi ngày.")

def now(update, context):
    check_in()

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    schedule.every().day.at("00:00").do(check_in)

    threading.Thread(target=run_schedule, daemon=True).start()

    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("settime", settime))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("checkin", now))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
