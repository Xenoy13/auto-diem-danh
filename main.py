import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
import schedule
import requests

# ===============================
# CẤU HÌNH NGƯỜI DÙNG
# ===============================
EMAIL = "hieucyberwork@gmail.com"
CHECKIN_URL = "https://hoctot365.odoo.com/b2102454623412645095758715465195974579457497457469754674279454545454545454545454545454545642167529745794514"

# Lấy biến môi trường từ Railway (đã khai báo)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# ===============================
# HÀM TIỆN ÍCH
# ===============================
def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def send_telegram(msg):
    """Gửi tin nhắn Telegram (nếu token và chat ID hợp lệ)"""
    if BOT_TOKEN and CHAT_ID:
        try:
            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={"chat_id": CHAT_ID, "text": msg},
                timeout=10
            )
        except Exception as e:
            log(f"⚠️ Không gửi được Telegram: {e}")
    else:
        log("⚠️ Thiếu BOT_TOKEN hoặc CHAT_ID")

# ===============================
# HÀM CHÍNH
# ===============================
def check_in():
    log("🚀 Bắt đầu điểm danh tự động...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            log("🌐 Đang mở trang điểm danh...")
            page.goto(CHECKIN_URL, timeout=60000)
            page.wait_for_load_state("networkidle")
            time.sleep(3)

            log("🔍 Nhập email vào ô...")
            try:
                page.fill('input[placeholder*="Nhập email"]', EMAIL)
            except:
                try:
                    page.fill("input[type='email']", EMAIL)
                except:
                    raise Exception("Không tìm thấy ô nhập email!")

            log("📨 Nhấn nút 'Xác nhận điểm danh'...")
            try:
                page.click("button:has-text('Xác nhận')")
            except:
                try:
                    page.click("button:has-text('điểm danh')")
                except:
                    raise Exception("Không tìm thấy nút xác nhận điểm danh!")

            page.wait_for_timeout(7000)
            log("🕒 Đang chờ phản hồi...")

            # Lưu lại kết quả
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot = f"checkin_result_{timestamp}.png"
            page.screenshot(path=screenshot)

            html = page.content().lower()
            if "điểm danh thành công" in html or "thành công" in html:
                msg = f"✅ Điểm danh thành công cho {EMAIL} lúc {timestamp}"
                log(msg)
                send_telegram(msg)
            else:
                msg = f"⚠️ Điểm danh KHÔNG thành công (cần kiểm tra ảnh {screenshot})"
                log(msg)
                send_telegram(msg)

        except Exception as e:
            msg = f"❌ Lỗi khi điểm danh: {e}"
            log(msg)
            send_telegram(msg)

        finally:
            browser.close()
            log("🧩 Đã đóng trình duyệt.\n")

# ===============================
# LỊCH CHẠY TỰ ĐỘNG
# ===============================
if os.environ.get("RUN_ONCE", "false").lower() == "true":
    check_in()
else:
    log("🕛 Lên lịch điểm danh tự động lúc 00:00 mỗi ngày...")
    schedule.every().day.at("00:00").do(check_in)
    while True:
        schedule.run_pending()
        time.sleep(30)
