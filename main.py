import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import schedule
import time
import requests
import os

# ===== THÔNG TIN NGƯỜI DÙNG =====
EMAIL = "hieucyberwork@gmail.com"
URL = "https://hoctot365.odoo.com/b2102454623412645"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

TIME_FILE = "time.txt"

# ===== ĐỌC GIỜ LƯU TRƯỚC ĐÓ =====
def read_time():
    if os.path.exists(TIME_FILE):
        return open(TIME_FILE).read().strip()
    return "00:00"

CHECKIN_TIME = read_time()

# ===== GỬI TELE =====
def send_telegram(msg):
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")

# ===== HÀM ĐIỂM DANH =====
def check_in():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = uc.Chrome(options=chrome_options)
        driver.get(URL)

        email_input = driver.find_element(By.CSS_SELECTOR, "input[type='text'], input[type='email']")
        email_input.send_keys(EMAIL)

        submit_btn = driver.find_element(By.CSS_SELECTOR, "button, input[type='submit']")
        submit_btn.click()

        time.sleep(3)
        driver.quit()

        send_telegram("✅ Điểm danh thành công!")
    except Exception as e:
        send_telegram(f"❌ Lỗi: {e}")

# ===== NHẬN LỆNH TELEGRAM =====
def listen():
    global CHECKIN_TIME
    updates = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates").json()

    if "result" not in updates:
        return

    for update in updates["result"]:
        if "message" in update and "text" in update["message"]:
            msg = update["message"]["text"]
            if msg.startswith("/settime "):
                new_time = msg.replace("/settime ", "").strip()
                open(TIME_FILE, "w").write(new_time)
                CHECKIN_TIME = new_time
                schedule.clear()
                schedule.every().day.at(CHECKIN_TIME).do(check_in)
                send_telegram(f"⏰ Đã đổi giờ điểm danh thành **{CHECKIN_TIME}**")

# ===== KHỞI ĐỘNG =====
schedule.every().day.at(CHECKIN_TIME).do(check_in)
send_telegram(f"🤖 Bot đang chạy! Điểm danh lúc {CHECKIN_TIME}")

while True:
    listen()
    schedule.run_pending()
    time.sleep(1)
