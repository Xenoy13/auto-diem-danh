import os
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
import schedule

EMAIL = "hieucyberwork@gmail.com"
CHECKIN_URL = "https://hoctot365.odoo.com/b2102454623412645095758715465195974579457497457469754674279454545454545454545454545454545642167529745794514"

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

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
            time.sleep(4)

            log("🔍 Tìm ô nhập email...")
            # Tìm theo nhiều cách khác nhau để chắc chắn hoạt động
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

            # Đợi hệ thống phản hồi (JS xử lý)
            page.wait_for_timeout(7000)
            log("🕒 Đang chờ kết quả từ máy chủ...")

            # Chụp ảnh xác nhận
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            page.screenshot(path=f"checkin_result_{timestamp}.png")
            log(f"📸 Đã chụp ảnh kết quả: checkin_result_{timestamp}.png")

            html = page.content().lower()
            if "điểm danh thành công" in html or "thành công" in html:
                log("✅ Điểm danh thành công!")
            else:
                log("⚠️ Không tìm thấy thông báo thành công, kiểm tra lại trang chụp ảnh.")

        except Exception as e:
            log(f"❌ Lỗi khi điểm danh: {e}")

        finally:
            browser.close()
            log("🧩 Đã đóng trình duyệt.\n")

if os.environ.get("RUN_ONCE", "false").lower() == "true":
    check_in()
else:
    log("🕛 Lên lịch điểm danh tự động lúc 00:00 mỗi ngày...")
    schedule.every().day.at("00:00").do(check_in)

    while True:
        schedule.run_pending()
        time.sleep(30)
