import os
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

API = f"https://api.telegram.org/bot{TOKEN}"


def send_message(chat_id, text):
    requests.post(
        f"{API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        },
        timeout=20
    )


@app.route("/", methods=["GET"])
def home():
    return "Hasibi Telegram Bot is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json(silent=True) or {}

    message = update.get("message", {})
    chat = message.get("chat", {})
    text = message.get("text", "")

    if not chat:
        return "OK"

    chat_id = chat.get("id")

    if text == "/start":
        send_message(
            chat_id,
            "سلام 👋\n\n"
            "به ربات تلگرام حسیبی خوش آمدی.\n\n"
            "دستورها:\n"
            "/help - راهنما\n"
            "/video - پردازش ویدیو\n"
            "/audio - تمیز کردن صدا\n"
            "/subtitle - ساخت زیرنویس"
        )

    elif text == "/help":
        send_message(
            chat_id,
            "راهنمای ربات:\n\n"
            "/video - پردازش ویدیو\n"
            "/audio - تمیز کردن صدا\n"
            "/subtitle - ساخت زیرنویس"
        )

    elif text == "/video":
        send_message(
            chat_id,
            "🎬 بخش پردازش ویدیو به‌زودی فعال می‌شود."
        )

    elif text == "/audio":
        send_message(
            chat_id,
            "🎙 بخش تمیز کردن صدا به‌زودی فعال می‌شود."
        )

    elif text == "/subtitle":
        send_message(
            chat_id,
            "📝 بخش ساخت زیرنویس به‌زودی فعال می‌شود."
        )

    else:
        send_message(
            chat_id,
            "پیامت دریافت شد ✅\nبرای راهنما /help را بفرست."
        )

    return "OK"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    if TOKEN and WEBHOOK_URL:
        try:
            requests.post(
                f"{API}/setWebhook",
                json={"url": WEBHOOK_URL + "/webhook"},
                timeout=20
            )
        except Exception:
            pass

    app.run(host="0.0.0.0", port=port)
