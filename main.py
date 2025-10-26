import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import schedule
import time
import requests
import os

# ===== CẤU HÌNH NGƯỜI DÙNG =====
EMAIL = "hieucyberwork@gmail.com"
URL = "https://hoctot365.odoo.com/b2102454623412645095758715465195974579457497457469754674279454545454545454545454545454545642167529745794514"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

TIME_FILE = "time.txt"
LAST_FILE = "last_checkin.txt"

# ===== ĐỌC GIỜ LƯU TRƯỚC =====
def read_time():
    if os.path.exists(TIME_FILE):
        return open(TIME_FILE).read().strip()
    return "00:00"

CHECKIN_TIME = read_time()

# ===== GỬI TIN NHẮN TELEGRAM =====
def send_telegram(msg):
    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": msg}
    )

# ===== GỬI ẢNH =====
def send_photo(photo_path):
    try:
        files = {"photo": open(photo_path, "rb")}
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto?chat_id={CHAT_ID}", files=files)
    except:
        send_telegram("⚠ Gửi ảnh thất bại nhưng điểm danh đã xong")

# ===== HÀM ĐIỂM DANH =====
def check_in():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        driver = uc.Chrome(options=chrome_options)
        driver.get(URL)
        time.sleep(2)

        email_input = driver.find_element(By.CSS_SELECTOR, "input[type='text'], input[type='email']")
        email_input.clear()
        email_input.send_keys(EMAIL)

        confirm_btn = driver.find_element(By.XPATH, "//button[contains(., 'Xác nhận')]")
        confirm_btn.click()

        time.sleep(3)

        screenshot_path = "checkin.png"
        driver.save_screenshot(screenshot_path)
        driver.quit()

        with open(LAST_FILE, "w") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S"))

        send_telegram("✅ Điểm danh thành công!")
        send_photo(screenshot_path)

    except Exception as e:
        send_telegram(f"❌ Lỗi điểm danh: {e}")

# ===== LISTEN TELEGRAM COMMANDS =====
last_update_id = 0

def listen():
    global CHECKIN_TIME, last_update_id

    updates = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates").json()
    if "result" not in updates:
        return

    for update in updates["result"]:
        if update["update_id"] <= last_update_id:
            continue
        last_update_id = update["update_id"]

        if "message" in update and "text" in update["message"]:
            msg = update["message"]["text"]

            # THAY ĐỔI GIỜ
            if msg.startswith("/settime "):
                new_time = msg.replace("/settime ", "").strip()
                open(TIME_FILE, "w").write(new_time)
                CHECKIN_TIME = new_time
                schedule.clear()
                schedule.every().day.at(CHECKIN_TIME).do(check_in)
                send_telegram(f"⏰ Đã đổi giờ điểm danh thành {CHECKIN_TIME}")

            # KIỂM TRA TRẠNG THÁI
            elif msg == "/status":
                if os.path.exists(LAST_FILE):
                    last = open(LAST_FILE).read()
                else:
                    last = "Chưa điểm danh lần nào."
                send_telegram(f"📌 Lần điểm danh gần nhất: {last}")

            # ⭐ ĐIỂM DANH NGAY
            elif msg == "/checkin":
                send_telegram("🔄 Đang điểm danh ngay...")
                check_in()

# ===== KHỞI ĐỘNG =====
schedule.every().day.at(CHECKIN_TIME).do(check_in)
send_telegram(f"🤖 Bot đang chạy! Điểm danh lúc {CHECKIN_TIME}")

while True:
    listen()
    schedule.run_pending()
    time.sleep(2)
