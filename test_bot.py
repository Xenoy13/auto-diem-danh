import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_test():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": "✅ BOT ĐÃ HOẠT ĐỘNG BÌNH THƯỜNG!"}
    r = requests.post(url, data=data)
    print("Response:", r.json())

send_test()
