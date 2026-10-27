import os
import json
import urllib.request

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = "-1004415135551"

if not BOT_TOKEN:
    raise SystemExit("TELEGRAM_BOT_TOKEN is missing")

message_text = (
    "<b>New Content!</b>\n\n"
    "We have just pushed fresh content to our platform. "
    "Check it out."
)

keyboard = {
    "inline_keyboard": [
        [
            {"text": "🌐 Visit Website", "url": "https://steemstreamer.pages.dev"}
        ]
    ]
}

payload = {
    "chat_id": CHAT_ID,
    "text": message_text,
    "parse_mode": "HTML",
    "reply_markup": json.dumps(keyboard)
}

data = json.dumps(payload).encode("utf-8")
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

req = urllib.request.Request(
    url,
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    with urllib.request.urlopen(req) as response:
        print("Success:", response.read().decode())
except Exception as e:
    print("Error sending message:", e)
