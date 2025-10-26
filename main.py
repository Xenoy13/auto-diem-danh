import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import schedule
import time
import requests
import os

# ==== THÔNG TIN CỦA BẠN ====
EMAIL = "hieucyberwork@gmail.com"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Đổi giờ điểm danh tùy ý: "HH:MM" (24h)
CHECKIN_TIME = "00:00"

URL = "https://hoctot365.odoo.com/b2102454623412645095758715465195974579457497457469754674279454545454545454545454545454545642167529745794514"

# ==== GỬI THÔNG BÁO TELEGRAM ====
def send_telegram(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ Chưa cấu hình BOT_TOKEN hoặc CHAT_ID → Bỏ qua gửi Telegram")
        return
    try:
        requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": message},
            timeout=10
        )
    except Exception as e:
        print("Không thể gửi Telegram:", e)


# ==== HÀM ĐIỂM DANH ====
def check_in():
    try:
 chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--window-size=1920,1080")
driver = uc.Chrome(options=chrome_options)
        driver.get(URL)

        wait = WebDriverWait(driver, 15)

        # nhập email
        email_input = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[type='email'], input[type='text']")
            )
        )
        email_input.clear()
        email_input.send_keys(EMAIL)

        # nhấn xác nhận
        try:
            submit_btn = driver.find_element(By.CSS_SELECTOR, "button, input[type='submit']")
            submit_btn.click()
        except:
            from selenium.webdriver.common.keys import Keys
            email_input.send_keys(Keys.ENTER)

        time.sleep(3)
        driver.quit()

        send_telegram("✅ Điểm danh thành công!")
        print("✅ Điểm danh xong.")

    except Exception as e:
        send_telegram(f"❌ Lỗi khi điểm danh: {e}")
        print("❌ Lỗi:", e)


# ==== LẬP LỊCH ====
schedule.every().day.at(CHECKIN_TIME).do(check_in)

send_telegram(f"🤖 Bot đang chạy! Sẽ tự động điểm danh mỗi ngày lúc {CHECKIN_TIME}.")
print(f"Bot đã bật — sẽ điểm danh lúc {CHECKIN_TIME} mỗi ngày.")

while True:
    schedule.run_pending()
    time.sleep(1)
