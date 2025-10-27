import os
import time
import schedule
import requests
from playwright.sync_api import sync_playwright

EMAIL = "hieucyberwork@gmail.com"
URL = "https://hoctot365.odoo.com/b2102454623412645095758715465195974579457497457469754674279454545454545454545454545454545642167529745794514"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(msg):
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                 params={"chat_id": CHAT_ID, "text": msg})

def send_photo(photo_path):
    with open(photo_path, "rb") as f:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                      params={"chat_id": CHAT_ID}, files={"photo": f})

def check_in():
    send_telegram("🔄 Bắt đầu điểm danh…")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)
        time.sleep(3)
        page.fill("input[type='text'], input[type='email']", EMAIL)
        page.click("text=Xác nhận Điểm danh")
        time.sleep(3)
        screenshot = "checkin.png"
        page.screenshot(path=screenshot)
        browser.close()
    send_telegram("✅ Điểm danh thành công!")
    send_photo(screenshot)

def main():
    schedule.every().day.at("00:00").do(check_in)
    send_telegram(f"🤖 Bot đã khởi động! Điểm danh mỗi ngày lúc 00:00")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
