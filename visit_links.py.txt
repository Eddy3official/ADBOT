import json
import os
import time
import urllib.request
from datetime import datetime, timezone

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "-1004415135551")
SITE_URL = "https://shorturl.at/zNI0m"
STATE_FILE = os.path.join(os.path.dirname(__file__), "bot_posts.json")
LAST_REPORT_FILE = os.path.join(os.path.dirname(__file__), "last_report.json")
MESSAGE_TTL_SECONDS = 1800  # 30 minutes
REPORT_COOLDOWN_SECONDS = 300  # 5 minutes

if not BOT_TOKEN:
    raise SystemExit("TELEGRAM_BOT_TOKEN is missing")


def utc_timestamp():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if data is not None else default
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path, payload):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)


def load_state():
    data = load_json(STATE_FILE, [])
    if isinstance(data, list):
        return data
    return []


def save_state(items):
    save_json(STATE_FILE, items)


def load_last_report():
    return load_json(LAST_REPORT_FILE, {})


def save_last_report(data):
    save_json(LAST_REPORT_FILE, data)


def telegram_request(method, payload):
    data = json.dumps(payload).encode("utf-8")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=20) as response:
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


def format_price(value):
    return f"${value:,.2f}"


def format_change(value):
    return f"{value:+.2f}%"


def trend_label(change_value):
    if change_value > 2.0:
        return "Strong Bullish"
    if change_value > 0.0:
        return "Bullish"
    if change_value < -2.0:
        return "Strong Bearish"
    if change_value < 0.0:
        return "Bearish"
    return "Neutral"


def fetch_market_data():
    ids = "bitcoin,xaut,tether-gold"
    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        f"?ids={ids}&vs_currencies=usd&include_24hr_change=true"
    )

    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise RuntimeError(f"Market API request failed: {exc}") from exc

    btc_data = payload.get("bitcoin")
    xaut_data = payload.get("xaut") or payload.get("tether-gold")

    if btc_data is None or xaut_data is None:
        raise RuntimeError(f"Market data unavailable: {payload}")

    btc_price = float(btc_data.get("usd", 0.0))
    btc_change = float(btc_data.get("usd_24h_change", 0.0))

    xaut_price = float(xaut_data.get("usd", 0.0))
    xaut_change = float(xaut_data.get("usd_24h_change", 0.0))

    return {
        "btc": {
            "price": btc_price,
            "change": btc_change,
        },
        "xaut": {
            "price": xaut_price,
            "change": xaut_change,
        },
    }


def build_message(payload, template_index):
    btc = payload["btc"]
    xaut = payload["xaut"]

    btc_price = format_price(btc["price"])
    btc_change = format_change(btc["change"])
    btc_trend = trend_label(btc["change"])

    xaut_price = format_price(xaut["price"])
    xaut_change = format_change(xaut["change"])
    xaut_trend = trend_label(xaut["change"])

    templates = [
        (
            "XAUT / BTC market update\n"
            f"Updated: {utc_timestamp()}\n\n"
            f"XAUT is trading at {xaut_price}, {xaut_change} over the last 24 hours.\n"
            f"BTC is trading at {btc_price}, {btc_change} over the last 24 hours.\n\n"
            f"XAUT trend: {xaut_trend}\n"
            f"BTC trend: {btc_trend}\n\n"
            "The market tone remains constructive, with momentum continuing to hold across both assets.\n"
            f"Trade link: {SITE_URL}"
        ),
        (
            "Market report: XAUT and BTC\n"
            f"Updated: {utc_timestamp()}\n\n"
            f"XAUT: {xaut_price} | {xaut_change} | {xaut_trend}\n"
            f"BTC: {btc_price} | {btc_change} | {btc_trend}\n\n"
            "Momentum remains active, with BTC leading the pace and XAUT holding a steady range.\n"
            f"Trade link: {SITE_URL}"
        ),
        (
            "XAUT and BTC update\n"
            f"Updated: {utc_timestamp()}\n\n"
            f"XAUT is priced at {xaut_price} and is {xaut_change} in the last 24 hours.\n"
            f"BTC is priced at {btc_price} and is {btc_change} in the last 24 hours.\n\n"
            "The current setup remains supportive, with continued participation across both markets.\n"
            f"Trade link: {SITE_URL}"
        ),
        (
            "Session check: XAUT and BTC\n"
            f"Updated: {utc_timestamp()}\n\n"
            f"XAUT: {xaut_price} | {xaut_change} | {xaut_trend}\n"
            f"BTC: {btc_price} | {btc_change} | {btc_trend}\n\n"
            "Price action remains steady and the broader tone continues to favor active trading.\n"
            f"Trade link: {SITE_URL}"
        ),
        (
            "Market snapshot\n"
            f"Updated: {utc_timestamp()}\n\n"
            f"XAUT: {xaut_price}\n"
            f"24h change: {xaut_change}\n"
            f"Trend: {xaut_trend}\n\n"
            f"BTC: {btc_price}\n"
            f"24h change: {btc_change}\n"
            f"Trend: {btc_trend}\n\n"
            "The market remains in a constructive phase with both assets holding positive momentum.\n"
            f"Trade link: {SITE_URL}"
        ),
        (
            "XAUT / BTC brief\n"
            f"Updated: {utc_timestamp()}\n\n"
            f"XAUT is trading at {xaut_price}, up {xaut_change} over the last 24 hours.\n"
            f"BTC is trading at {btc_price}, up {btc_change} over the last 24 hours.\n\n"
            "The trend remains supportive, with strength continuing to show in the broader crypto and metals-linked space.\n"
            f"Trade link: {SITE_URL}"
        ),
    ]

    return templates[template_index % len(templates)]


def should_send_new_report(data):
    last_report = load_last_report()
    if not last_report:
        return True

    try:
        last_sent = float(last_report.get("timestamp", 0))
    except (TypeError, ValueError):
        return True

    return (time.time() - last_sent) >= REPORT_COOLDOWN_SECONDS


def send_new_report():
    if not should_send_new_report({}):
        print("Skipping duplicate market report within cooldown window.")
        return

    market_data = fetch_market_data()
    template_index = int(time.time() // 600)  # rotates on a 10-minute cycle
    message_text = build_message(market_data, template_index)

    keyboard = {
        "inline_keyboard": [
            [{"text": "Trade Now", "url": SITE_URL}]
        ]
    }

    result = telegram_request(
        "sendMessage",
        {
            "chat_id": CHAT_ID,
            "text": message_text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
            "reply_markup": json.dumps(keyboard),
        },
    )

    if result.get("ok"):
        message_id = result["result"]["message_id"]
        state = load_state()
        state.append({"message_id": message_id, "timestamp": int(time.time())})
        save_state(state)

        save_last_report({"timestamp": time.time(), "message_id": message_id})
        print(f"Sent market report {message_id}")
    else:
        print("Failed to send market report:", result)


def main():
    delete_old_bot_posts()
    send_new_report()


if __name__ == "__main__":
    main()
