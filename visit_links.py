import json
import os
import random
import time
import urllib.request

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = "-1004415135551"
SITE_URL = "https://steemstreamer.pages.dev"
OFFSET_FILE = os.path.join(os.path.dirname(__file__), "telegram_offset.json")
MESSAGE_TTL_SECONDS = 600

if not BOT_TOKEN:
    raise SystemExit("TELEGRAM_BOT_TOKEN is missing")


def read_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if data is not None else default
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


def telegram_request(endpoint, payload):
    data = json.dumps(payload).encode("utf-8")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{endpoint}"
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as response:
        response_body = response.read().decode("utf-8")
        return json.loads(response_body) if response_body else {}


def purge_old_group_messages():
    now = int(time.time())
    offset = read_json(OFFSET_FILE, 0)
    result = telegram_request(
        "getUpdates",
        {
            "offset": int(offset),
            "limit": 100,
            "timeout": 5,
            "allowed_updates": ["message"],
        },
    )

    updates = result.get("result", [])
    if not updates:
        return

    max_offset = int(offset)
    for update in updates:
        update_id = update.get("update_id")
        if update_id is not None:
            max_offset = max(max_offset, int(update_id) + 1)

        message = update.get("message")
        if not message:
            continue

        chat = message.get("chat") or {}
        if str(chat.get("id")) != str(CHAT_ID):
            continue

        message_id = message.get("message_id")
        message_date = message.get("date")
        if message_id is None or message_date is None:
            continue

        if now - int(message_date) <= MESSAGE_TTL_SECONDS:
            continue

        try:
            telegram_request(
                "deleteMessage",
                {"chat_id": CHAT_ID, "message_id": int(message_id)},
            )
            print(f"Deleted message {message_id} from chat {CHAT_ID}")
        except Exception as exc:
            print(f"Failed deleting message {message_id}: {exc}")

    write_json(OFFSET_FILE, max_offset)


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


def main():
    purge_old_group_messages()

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

    result = telegram_request("sendMessage", payload)
    if result.get("ok"):
        print("Message sent successfully")
    else:
        print("Telegram send failed:", result)


if __name__ == "__main__":
    main()
