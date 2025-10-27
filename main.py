from playwright.sync_api import sync_playwright
import requests
import time
import os

EMAIL = "hieucyberwork@gmail.com"
URL = "https://hoctot365.odoo.com/b210245..."

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram(text):
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                 params={"chat_id": CHAT_ID, "text": text})

def send_photo(path):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                  files={"photo": open(path, "rb")},
                  params={"chat_id": CHAT_ID})

def check_in():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)

        page.fill("input[type='text'], input[type='email']", EMAIL)
        page.click("text=Xác nhận Điểm danh")

        time.sleep(3)
        page.screenshot(path="checkin.png")
        browser.close()

    send_telegram("✅ Điểm danh thành công!")
    send_photo("checkin.png")

check_in()
