import json
import os
import random
import urllib.request

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = "-1004415135551"
SITE_URL = "https://steemstreamer.pages.dev"

if not BOT_TOKEN:
    raise SystemExit("TELEGRAM_BOT_TOKEN is missing")

POST_LIBRARY = [
    (
        "<b>Fresh Update 🚀</b>\n\n"
        "Something new just dropped on our platform. "
        "Explore it now and see what’s waiting for you."
    ),
    (
        "<b>New Content ✨</b>\n\n"
        "We’ve just published fresh material for our community. "
        "Take a look and discover what’s new."
    ),
    (
        "<b>Fresh Drop 📢</b>\n\n"
        "A new update is live and ready to explore. "
        "Check it out before the next wave rolls in."
    ),
    (
        "<b>Just Released 🔥</b>\n\n"
        "The latest content is now available. "
        "See what everyone is talking about."
    ),
    (
        "<b>New Arrival 🆕</b>\n\n"
        "Fresh content is online and waiting to be explored. "
        "Jump in and discover what’s new."
    ),
    (
        "<b>Live Now 🌍</b>\n\n"
        "We’ve just activated new content for our audience. "
        "Stop by and check it out today."
    ),
    (
        "<b>Update Alert 🚨</b>\n\n"
        "A new batch of content has just gone live. "
        "Head over and see what’s new."
    ),
    (
        "<b>Fresh Material 💡</b>\n\n"
        "We’ve uploaded something new and worth checking out. "
        "Visit the platform and explore the latest release."
    ),
    (
        "<b>We Added More 📚</b>\n\n"
        "Fresh updates are live and ready for viewing. "
        "Take a minute to see what’s changed."
    ),
    (
        "<b>Latest Release 🎉</b>\n\n"
        "New content has just been published. "
        "See what’s been added and start exploring."
    ),
    (
        "<b>Now Live 🌐</b>\n\n"
        "Our newest content is now available. "
        "Give it a look and enjoy the latest update."
    ),
    (
        "<b>Freshly Posted 📰</b>\n\n"
        "A new update just went live. "
        "Explore the latest content and see what’s trending."
    ),
    (
        "<b>New Wave 🌊</b>\n\n"
        "Fresh content has arrived on the platform. "
        "Jump in and see the latest release."
    ),
    (
        "<b>Content Drop 🚀</b>\n\n"
        "We’ve just published something brand new. "
        "Take a look and experience the newest update."
    ),
    (
        "<b>Freshly Updated 🧩</b>\n\n"
        "A new set of content is now live. "
        "Check it out and discover what’s been added."
    ),
    (
        "<b>Newly Added 🌟</b>\n\n"
        "The platform has been refreshed with brand-new content. "
        "Visit now and see what’s waiting for you."
    ),
    (
        "<b>Fresh Content Alert ⚡</b>\n\n"
        "We’ve just uploaded a new batch of material. "
        "Explore the latest features and updates today."
    ),
    (
        "<b>Latest Upload 📦</b>\n\n"
        "The newest content is live and ready to view. "
        "Find out what’s new and take a look now."
    ),
    (
        "<b>Platform Updated 💫</b>\n\n"
        "Fresh content has just gone live. "
        "Head over and discover what our latest release has to offer."
    ),
    (
        "<b>New Release 🎯</b>\n\n"
        "An updated batch of content is now available. "
        "Check it out and be the first to explore it."
    ),
]

message_text = random.choice(POST_LIBRARY)

keyboard = {
    "inline_keyboard": [
        [
            {"text": "🌐 Visit Website", "url": SITE_URL}
        ]
    ]
}

payload = {
    "chat_id": CHAT_ID,
    "text": message_text,
    "parse_mode": "HTML",
    "reply_markup": json.dumps(keyboard),
}

data = json.dumps(payload).encode("utf-8")
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

req = urllib.request.Request(
    url,
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST",
)

try:
    with urllib.request.urlopen(req) as response:
        print("Success:", response.read().decode())
except Exception as e:
    print("Error sending message:", e)
