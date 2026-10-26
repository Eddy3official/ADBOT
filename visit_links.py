import os
import random
import time
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright

SITE_URL = os.environ.get("SITE_URL", "https://steemstreamer.pages.dev")

DEVICE_PROFILES = [
    {
        "name": "windows_chrome",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "viewport": {"width": 1440, "height": 900},
        "device_scale_factor": 1,
        "is_mobile": False,
        "has_touch": False,
        "locale": "en-US",
        "timezone_id": "America/New_York",
    },
    {
        "name": "android_pixel",
        "user_agent": "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "viewport": {"width": 412, "height": 915},
        "device_scale_factor": 2.75,
        "is_mobile": True,
        "has_touch": True,
        "locale": "en-US",
        "timezone_id": "America/Chicago",
    },
    {
        "name": "ios_ipad",
        "user_agent": "Mozilla/5.0 (iPad; CPU OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
        "viewport": {"width": 820, "height": 1180},
        "device_scale_factor": 2,
        "is_mobile": False,
        "has_touch": True,
        "locale": "en-US",
        "timezone_id": "America/Los_Angeles",
    },
]


def unique_links(links):
    seen = set()
    result = []
    for link in links:
        if not link:
            continue
        if link.startswith("javascript:"):
            continue
        if link.startswith("#"):
            continue
        if link.startswith("mailto:"):
            continue
        if link not in seen:
            seen.add(link)
            result.append(link)
    return result


def pick_random_device():
    return random.choice(DEVICE_PROFILES)


def main():
    device = pick_random_device()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=device["user_agent"],
            viewport=device["viewport"],
            device_scale_factor=device["device_scale_factor"],
            is_mobile=device["is_mobile"],
            has_touch=device["has_touch"],
            locale=device["locale"],
            timezone_id=device["timezone_id"],
            ignore_https_errors=True,
        )
        page = context.new_page()

        print(f"Opening {SITE_URL} with device profile: {device['name']}")
        page.goto(SITE_URL, wait_until="networkidle", timeout=60000)

        time.sleep(2)

        anchors = page.locator("a[href]").evaluate_all("""
            (els) => els.map(el => el.getAttribute('href'))
        """)

        links = []
        for href in anchors:
            full = urljoin(SITE_URL, href)
            if full.startswith("https://steemstreamer.pages.dev"):
                links.append(full)

        links = unique_links(links)[:20]

        print("Found links:", links)

        for i, link in enumerate(links, 1):
            try:
                print(f"[{i}/{len(links)}] Visiting {link}")
                page.goto(link, wait_until="networkidle", timeout=60000)
                time.sleep(2)
            except Exception as e:
                print(f"Failed to visit {link}: {e}")

        context.close()
        browser.close()


if __name__ == "__main__":
    main()
