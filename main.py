from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import schedule
import time
import requests
import os

# ==== CẤU HÌNH NGƯỜI DÙNG ====
EMAIL = "hieucyberwork@gmail.com"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

CHECKIN_TIME = "00:00"  # Giờ điểm danh mỗi ngày

URL = "https://hoctot365.odoo.com/b2102454623412645095758715465195974579457497457469754674279454545454545454545454545454545642167529745794514"


def send_telegram(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ Không có BOT_TOKEN hoặc CHAT_ID → Bỏ qua gửi Telegram.")
        return

    try:
        requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": message},
            timeout=10
        )
    except:
        print("⚠️ Không gửi được Telegram.")


def check_in():
    try:
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        driver = Chrome(options=chrome_options)
        driver.get(URL)

        wait = WebDriverWait(driver, 15)
        email_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email'], input[type='text']"))
        )

        email_input.clear()
        email_input.send_keys(EMAIL)

        try:
            submit = driver.find_element(By.CSS_SELECTOR, "button, input[type='submit']")
            submit.click()
        except:
            email_input.send_keys(Keys.ENTER)

        time.sleep(3)
        driver.quit()

        send_telegram("✅ Điểm danh thành công!")
        print("✅ Điểm danh thành công!")

    except Exception as e:
        send_telegram(f"❌ Lỗi khi điểm danh: {e}")
        print("❌ Lỗi:", e)


# Lập lịch chạy tự động
schedule.every().day.at(CHECKIN_TIME).do(check_in)

send_telegram(f"🤖 Bot đang chạy! Sẽ tự động điểm danh lúc {CHECKIN_TIME} mỗi ngày.")
print(f"🤖 Bot đang chạy! Chờ đến {CHECKIN_TIME} để điểm danh...")

while True:
    schedule.run_pending()
    time.sleep(1)
