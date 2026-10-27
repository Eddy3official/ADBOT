import json
import os
import random
import time
import urllib.request

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = "-1004415135551"
SITE_URL = "https://steemstreamer.pages.dev"
STATE_FILE = os.path.join(os.path.dirname(__file__), "bot_posts.json")
MESSAGE_TTL_SECONDS = 600

if not BOT_TOKEN:
    raise SystemExit("TELEGRAM_BOT_TOKEN is missing")


def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return []


def save_state(items):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f)


def telegram_request(method, payload):
    data = json.dumps(payload).encode("utf-8")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


def delete_old_bot_posts():
    now = int(time.time())
    tracked = load_state()
    remaining = []

    for item in tracked:
        message_id = item.get("message_id")
        timestamp = item.get("timestamp")
        if message_id is None or timestamp is None:
            continue

        if now - int(timestamp) >= MESSAGE_TTL_SECONDS:
            try:
                result = telegram_request(
                    "deleteMessage",
                    {"chat_id": CHAT_ID, "message_id": int(message_id)}
                )
                if result.get("ok"):
                    print(f"Deleted bot post {message_id}")
                else:
                    print(f"Could not delete {message_id}: {result}")
            except Exception as exc:
                print(f"Error deleting {message_id}: {exc}")
        else:
            remaining.append(item)

    save_state(remaining)


POST_LIBRARY = [
    "<b>Fresh Update 🚀</b>\n\nSomething new just dropped on our platform. Explore it now and see what’s waiting for you.",
    "<b>New Content ✨</b>\n\nWe’ve just published fresh material for our community. Take a look and discover what’s new.",
    "<b>Fresh Drop 📢</b>\n\nA new update is live and ready to explore. Check it out before the next wave rolls in.",
    "<b>Just Released 🔥</b>\n\nThe latest content is now available. See what everyone is talking about.",
    "<b>New Arrival 🆕</b>\n\nFresh content is online and waiting to be explored. Jump in and discover what’s new.",
    "<b>Live Now 🌍</b>\n\nWe’ve just activated new content for our audience. Stop by and check it out today.",
    "<b>Update Alert 🚨</b>\n\nA new batch of content has just gone live. Head over and see what’s new.",
    "<b>Fresh Material 💡</b>\n\nWe’ve uploaded something new and worth checking out. Visit the platform and explore the latest release.",
    "<b>We Added More 📚</b>\n\nFresh updates are live and ready for viewing. Take a minute to see what’s changed.",
    "<b>Latest Release 🎉</b>\n\nNew content has just been published. See what’s been added and start exploring.",
    "<b>Now Live 🌐</b>\n\nOur newest content is now available. Give it a look and enjoy the latest update.",
    "<b>Freshly Posted 📰</b>\n\nA new update just went live. Explore the latest content and see what’s trending.",
    "<b>New Wave 🌊</b>\n\nFresh content has arrived on the platform. Jump in and see the latest release.",
    "<b>Content Drop 🚀</b>\n\nWe’ve just published something brand new. Take a look and experience the newest update.",
    "<b>Freshly Updated 🧩</b>\n\nA new set of content is now live. Check it out and discover what’s been added.",
    "<b>Newly Added 🌟</b>\n\nThe platform has been refreshed with brand-new content. Visit now and see what’s waiting for you.",
    "<b>Fresh Content Alert ⚡</b>\n\nWe’ve just uploaded a new batch of material. Explore the latest features and updates today.",
    "<b>Latest Upload 📦</b>\n\nThe newest content is live and ready to view. Find out what’s new and take a look now.",
    "<b>Platform Updated 💫</b>\n\nFresh content has just gone live. Head over and discover what our latest release has to offer.",
    "<b>New Release 🎯</b>\n\nAn updated batch of content is now available. Check it out and be the first to explore it."
]


def send_new_post():
    message_text = random.choice(POST_LIBRARY)

    keyboard = {
        "inline_keyboard": [
            [{"text": "🌐 Visit Website", "url": SITE_URL}]
        ]
    }

    result = telegram_request(
        "sendMessage",
        {
            "chat_id": CHAT_ID,
            "text": message_text,
            "parse_mode": "HTML",
            "reply_markup": json.dumps(keyboard),
        }
    )

    if result.get("ok"):
        message_id = result["result"]["message_id"]
        tracked = load_state()
        tracked.append({"message_id": message_id, "timestamp": int(time.time())})
        save_state(tracked)
        print("Sent new post:", message_id)
    else:
        print("Send failed:", result)


def main():
    delete_old_bot_posts()
    send_new_post()


if __name__ == "__main__":
    main()
