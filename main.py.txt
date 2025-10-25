from selenium import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import schedule
import time
import requests

# ==== THÔNG TIN CỦA BẠN ====
EMAIL = "hieucyberwork@gmail.com"   

BOT_TOKEN = "8026649597:AAF3NKZpQTrg9GJxw451ofaXinz4tWxOTDA"
CHAT_ID = 7071306427

CHECKIN_TIME = "00:00"   # Giờ điểm danh mỗi ngày (đổi theo ý bạn)

URL = "https://hoctot365.odoo.com/b2102454623412645095758715465195974579457497457469754674279454545454545454545454545454545642167529745794514"

# ==== GỬI TIN TELEGRAM ====
def send_telegram(message):
    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}")

# ==== HÀM ĐIỂM DANH ====
def check_in():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")      
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = uc.Chrome(options=chrome_options)
        driver.get(URL)

        # nhập gmail
        email_input = driver.find_element(By.CSS_SELECTOR, "input[type='text'], input[type='email']")
        email_input.send_keys(EMAIL)

        # nhấn xác nhận
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button, input[type='submit']")
        submit_btn.click()

        time.sleep(3)
        driver.quit()

        send_telegram("✅ Điểm danh thành công!")
        print("Điểm danh xong.")
    except Exception as e:
        send_telegram(f"❌ Lỗi khi điểm danh: {e}")
        print("Lỗi:", e)

# ==== LẬP LỊCH ====
schedule.every().day.at(CHECKIN_TIME).do(check_in)

send_telegram(f"🤖 Bot đang chạy! Sẽ điểm danh lúc {CHECKIN_TIME} mỗi ngày.")

print(f"Bot đã bật — sẽ điểm danh lúc {CHECKIN_TIME} mỗi ngày.")
while True:
    schedule.run_pending()
    time.sleep(1)
