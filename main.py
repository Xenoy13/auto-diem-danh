import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import schedule
import time
import requests
import os
import threading

# ===== THÔNG TIN NGƯỜI DÙNG =====
EMAIL = "hieucyberwork@gmail.com"
URL = "https://hoctot365.odoo.com/b2102454623412645"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

TIME_FILE = "time.txt"
LAST_UPDATE_FILE = "last_update.txt"

# ===== ĐỌC GIỜ LƯU TRƯỚC ĐÓ =====
def read_time():
    if os.path.exists(TIME_FILE):
        return open(TIME_FILE).read().strip()
    return "00:00"

CHECKIN_TIME = read_time()

# ===== GỬI TELE =====
def send_telegram(msg):
    try:
        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                     params={"chat_id": CHAT_ID, "text": msg})
    except:
        pass

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
        open("last_checkin.txt", "w").write(time.strftime("%Y-%m-%d %H:%M:%S"))
    except Exception as e:
        send_telegram(f"❌ Lỗi: {e}")

# ===== NHẬN LỆNH TELEGRAM (LONG POLLING) =====
def listen():
    global CHECKIN_TIME

    last_update_id = 0
    if os.path.exists(LAST_UPDATE_FILE):
        last_update_id = int(open(LAST_UPDATE_FILE).read())

    params = {"offset": last_update_id + 1, "timeout": 20}
    updates = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates", params=params).json()

    if "result" not in updates:
        return

    for update in updates["result"]:
        last_update_id = update["update_id"]
        open(LAST_UPDATE_FILE, "w").write(str(last_update_id))

        if "message" in update and "text" in update["message"]:
            msg = update["message"]["text"]
            if msg.startswith("/settime "):
                elif msg == "/status":
    if os.path.exists("last_checkin.txt"):
        last = open("last_checkin.txt").read().strip()
        send_telegram(f"🟢 Lần điểm danh gần nhất: {last}")
    else:
        send_telegram("⚠️ Chưa có lần điểm danh nào được ghi lại.")
                new_time = msg.replace("/settime ", "").strip()
                open(TIME_FILE, "w").write(new_time)
                CHECKIN_TIME = new_time
                schedule.clear()
                schedule.every().day.at(CHECKIN_TIME).do(check_in)
                send_telegram(f"⏰ Đã đổi giờ điểm danh thành {CHECKIN_TIME}")

# ===== TÁCH THREAD CHO SCHEDULE =====
def schedule_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)

# ===== KHỞI ĐỘNG =====
schedule.every().day.at(CHECKIN_TIME).do(check_in)
send_telegram(f"🤖 Bot đang chạy! Điểm danh lúc {CHECKIN_TIME}")

threading.Thread(target=schedule_thread, daemon=True).start()

while True:
    listen()

