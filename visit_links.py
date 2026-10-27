import os
import json
import urllib.request

# Fetch credentials from GitHub environment variables
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
# For channels use '@channelusername', for groups use the negative chat ID (e.g., -100xxxxxx)
CHAT_ID = "@your_channel_username" 

# Define your post content
message_text = (
    "<b>🚀 New Update Available!</b>\n\n"
    "We have just pushed a fresh update to our platform. "
    "Check out the latest features and changes right now."
)

# Define the stylish inline button layout
keyboard = {
    "inline_keyboard": [
        [
            {"text": "🌐 Visit Website", "url": "https://yourwebsite.com"}
        ]
    ]
}

# Construct the API request payload
payload = {
    "chat_id": CHAT_ID,
    "text": message_text,
    "parse_mode": "HTML", # Allows <b>, <i>, and <a> tags in text
    "reply_markup": json.dumps(keyboard)
}

# Convert payload to bytes
data = json.dumps(payload).encode('utf-8')

# Send the request using standard library (no external pip dependencies needed)
url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
req = urllib.request.Request(
    url, 
    data=data, 
    headers={'Content-Type': 'application/json'}
)

try:
    with urllib.request.urlopen(req) as response:
        print("Success:", response.read().decode())
except Exception as e:
    print("Error sending message:", e)
