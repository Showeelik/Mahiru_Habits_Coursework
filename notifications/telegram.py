import requests
from django.conf import settings

TOKEN = settings.TELEGRAM_BOT_TOKEN
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send_telegram_message(chat_id, message):
    data = {"chat_id": chat_id, "text": message}
    requests.post(URL, data=data)
