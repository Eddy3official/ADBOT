import json
import os
import random
import time
import urllib.request

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = "-1004415135551"
SITE_URL = "https://steemstreamer.pages.dev"
STATE_FILE = os.path.join(os.path.dirname(__file__), "bot_posts.json")
MESSAGE_TTL_SECONDS = 60  # 1 minute

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
    state = load_state()
    remaining = []

    for item in state:
        message_id = item.get("message_id")
        timestamp = item.get("timestamp")

        if message_id is None or timestamp is None:
            continue

        if now - int(timestamp) >= MESSAGE_TTL_SECONDS:
            try:
                result = telegram_request(
                    "deleteMessage",
                    {"chat_id": CHAT_ID, "message_id": int(message_id)},
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
    "Ava added a new photo.",
    "Leo uploaded a video.",
    "Mia posted a new image.",
    "Noah shared a video clip.",
    "Emma added another photo.",
    "Lucas uploaded a fresh video.",
    "Sofia posted a new picture.",
    "Mason shared a short video.",
    "Harper added a new image.",
    "James uploaded a photo.",
    "Ella posted a new video.",
    "Benjamin shared a fresh picture.",
    "Amelia added a new video.",
    "Henry uploaded a photo.",
    "Grace posted a new image.",
    "Alexander shared a video.",
    "Charlotte added another photo.",
    "Daniel uploaded a new video.",
    "Scarlett posted a picture.",
    "Jack shared a short video.",
    "Luna added a new photo.",
    "Owen uploaded a fresh video.",
    "Chloe posted a new image.",
    "Gabriel shared a video clip.",
    "Aria added a new picture.",
    "Wyatt uploaded a photo.",
    "Nora posted a new video.",
    "Julian shared a fresh photo.",
    "Zoe added a new image.",
    "Nathan uploaded a video.",
    "Layla posted a new picture.",
    "Isaac shared a fresh video.",
    "Madison added a new photo.",
    "Hudson uploaded a video clip.",
    "Penelope posted a new image.",
    "Eli shared a video.",
    "Stella added a picture.",
    "Leo uploaded another video.",
    "Aurora posted a new photo.",
    "Ryan shared a fresh image.",
    "Hazel added a new video.",
    "David uploaded a picture.",
    "Violet posted a new clip.",
    "Samuel shared a video.",
    "Ruby added a photo.",
    "Joseph uploaded a new video.",
    "Claire posted a fresh image.",
    "Carter shared a video.",
    "Natalie added a new picture.",
    "Julian uploaded a photo.",
    "Bella posted a new video.",
    "Adrian shared a fresh image.",
    "Lily added a new video.",
    "Ethan uploaded a picture.",
    "Mila posted a new clip.",
    "Leo shared a video.",
    "Eva added a new photo.",
    "Miles uploaded a fresh video.",
    "Naomi posted a new image.",
    "Theo shared a video clip.",
    "Samantha added a new photo.",
    "Isaiah uploaded a video.",
    "Hannah posted a new picture.",
    "Oliver shared a fresh image.",
    "Aubrey added a new video.",
    "Caleb uploaded a photo.",
    "Sadie posted a new clip.",
    "Aaron shared a video.",
    "Paisley added a new picture.",
    "Elijah uploaded a fresh video.",
    "Piper posted a new image.",
    "Jonathan shared a short video.",
    "Lucy added a new photo.",
    "Christian uploaded a video.",
    "Addison posted a new picture.",
    "Anthony shared a fresh clip.",
    "Brooklyn added a new image.",
    "Dylan uploaded a video.",
    "Savannah posted a new photo.",
    "Joshua shared a fresh video.",
    "Aria added another image.",
    "Sebastian uploaded a new video.",
    "Genesis posted a picture.",
    "Nicholas shared a fresh photo.",
    "Aurora added a new clip.",
    "Wyatt uploaded a photo.",
    "Stella posted a new video.",
    "Kai shared a fresh picture.",
    "Delilah added a new image.",
    "Mateo uploaded a video.",
    "Valentina posted a new photo.",
    "Colton shared a fresh video.",
    "Riley added a new picture.",
    "Asher uploaded a video clip.",
    "Ivy posted a new image.",
    "Julian shared a fresh photo.",
    "Freya added a new video.",
    "Henry uploaded a picture.",
    "Cora posted a new clip.",
    "Nathaniel shared a video.",
    "Lila added a new photo.",
    "Leo uploaded a fresh video.",
    "Maya posted a new image.",
    "Roman shared a video clip.",
    "Elena added a new photo.",
    "Victor uploaded a picture.",
    "Sophie posted a new video.",
    "Evan shared a fresh image.",
    "Ava added a new photo.",
    "Liam uploaded a video.",
    "Ella posted a new image.",
    "Mason shared a clip.",
    "Hannah added a new photo.",
    "Noah uploaded a video.",
    "Avery posted a new image.",
    "Jack shared a fresh video.",
    "Mila added a photo.",
    "Leo uploaded another video.",
    "Riley posted a new picture.",
    "Luca shared a video clip.",
    "Ariana added a new image.",
    "Daniel uploaded a photo.",
    "Chloe posted a new video.",
    "Nathan shared a fresh picture.",
    "Harper added a new clip.",
]


def send_new_post():
    message_text = random.choice(POST_LIBRARY)

    keyboard = {
        "inline_keyboard": [
            [{"text": "Visit Website", "url": SITE_URL}]
        ]
    }

    result = telegram_request(
        "sendMessage",
        {
            "chat_id": CHAT_ID,
            "text": message_text,
            "parse_mode": "HTML",
            "reply_markup": json.dumps(keyboard),
        },
    )

    if result.get("ok"):
        message_id = result["result"]["message_id"]
        state = load_state()
        state.append({"message_id": message_id, "timestamp": int(time.time())})
        save_state(state)
        print(f"Sent new post {message_id}")
    else:
        print("Failed to send post:", result)


def main():
    delete_old_bot_posts()
    send_new_post()


if __name__ == "__main__":
    main()
