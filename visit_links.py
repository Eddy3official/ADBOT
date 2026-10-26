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
        "name": "windows_chrome_alt",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "viewport": {"width": 1366, "height": 768},
        "device_scale_factor": 1,
        "is_mobile": False,
        "has_touch": False,
        "locale": "en-US",
        "timezone_id": "America/Chicago",
    },
    {
        "name": "linux_chrome",
        "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "viewport": {"width": 1280, "height": 800},
        "device_scale_factor": 1,
        "is_mobile": False,
        "has_touch": False,
        "locale": "en-US",
        "timezone_id": "America/Los_Angeles",
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


def random_wait(min_seconds=0.8, max_seconds=5.5):
    time.sleep(random.uniform(min_seconds, max_seconds))


def apply_anti_detection(page):
    page.add_init_script(
        """
        (() => {
            try {
                Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            } catch (e) {}

            try {
                Object.defineProperty(window, 'chrome', {
                    value: {
                        runtime: {},
                        loadTimes: () => {},
                        csi: () => {},
                    },
                    configurable: true,
                });
            } catch (e) {}

            try {
                const origQuery = navigator.permissions && navigator.permissions.query;
                if (origQuery) {
                    navigator.permissions.query = (parameters) => (
                        parameters && parameters.name === 'notifications'
                            ? Promise.resolve({ state: 'granted' })
                            : origQuery(parameters)
                    );
                }
            } catch (e) {}
        })();
        """
    )


def random_scroll(page):
    metrics = page.evaluate(
        """
        () => {
            const maxY = Math.max(
                document.body ? document.body.scrollHeight : 0,
                document.documentElement ? document.documentElement.scrollHeight : 0,
                window.innerHeight
            );
            return {
                width: window.innerWidth,
                height: window.innerHeight,
                maxY
            };
        }
        """
    )

    if not metrics or metrics["maxY"] <= metrics["height"]:
        return

    target_y = random.randint(metrics["height"] // 2, metrics["maxY"] - 120)
    page.evaluate(f"window.scrollTo(0, {target_y})")
    random_wait(0.5, 2.0)
    page.mouse.wheel(0, random.randint(150, 600))
    random_wait(0.2, 1.0)


def random_mouse_move(page):
    metrics = page.evaluate(
        """
        () => ({
            width: window.innerWidth,
            height: window.innerHeight
        })
        """
    )
    if not metrics:
        return

    x = random.randint(10, max(10, metrics["width"] - 10))
    y = random.randint(10, max(10, metrics["height"] - 10))
    page.mouse.move(x, y, steps=random.randint(12, 35))
    random_wait(0.1, 0.7)


def human_read(page):
    for _ in range(random.randint(1, 3)):
        random_scroll(page)
        random_mouse_move(page)


def pause_before_click():
    random_wait(0.6, 3.2)


def unique_links(links):
    seen = set()
    result = []
    for link in links:
        if not link:
            continue
        if link.startswith(("javascript:", "mailto:", "tel:", "#")):
            continue
        if link not in seen:
            seen.add(link)
            result.append(link)
    return result


def pick_random_device():
    return random.choice(DEVICE_PROFILES)


def get_internal_links(page, base_url):
    anchors = page.locator("a[href]").evaluate_all(
        """
        (els) => els.map(el => el.getAttribute('href'))
        """
    )

    print(f"[debug] Raw anchor hrefs before filtering: {anchors}")

    links = []
    for href in anchors:
        if not href:
            continue
        full = urljoin(base_url, href)
        if full.startswith(("http://", "https://")):
            links.append(full)

    return unique_links(links)


def click_element_human_like(page, locator):
    box = locator.bounding_box()
    if not box:
        return False

    x = random.uniform(box["x"] + 10, box["x"] + box["width"] - 10)
    y = random.uniform(box["y"] + 10, box["y"] + box["height"] - 10)

    page.mouse.move(x, y, steps=random.randint(15, 35))
    pause_before_click()
    page.mouse.down()
    page.mouse.up()
    random_wait(1.0, 3.5)
    return True


def open_page(page, url):
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    human_read(page)


def browser_args_for_profile(device):
    return [
        "--disable-dev-shm-usage",
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-blink-features=AutomationControlled",
        "--disable-features=IsolateOrigins,site-per-process",
        "--window-size={w},{h}".format(w=device["viewport"]["width"], h=device["viewport"]["height"]),
    ]


def main():
    device = pick_random_device()
    session_id = random.randint(10000, 99999)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=browser_args_for_profile(device),
        )

        context = browser.new_context(
            user_agent=device["user_agent"],
            viewport=device["viewport"],
            device_scale_factor=device["device_scale_factor"],
            is_mobile=device["is_mobile"],
            has_touch=device["has_touch"],
            locale=device["locale"],
            timezone_id=device["timezone_id"],
            ignore_https_errors=True,
            java_script_enabled=True,
        )
        context.set_default_timeout(60000)
        page = context.new_page()
        apply_anti_detection(page)

        print(f"[session {session_id}] Starting with device profile: {device['name']}")
        random_wait(1.0, 4.0)
        open_page(page, SITE_URL)

        links = get_internal_links(page, SITE_URL)
        random.shuffle(links)

        selected_links = links[: random.randint(2, 6)]
        print(f"[session {session_id}] Selected links:", selected_links)

        for i, link in enumerate(selected_links, 1):
            try:
                print(f"[session {session_id}] [{i}/{len(selected_links)}] Visiting {link}")
                open_page(page, link)

                # Randomized real-world browsing behavior: occasionally click a visible link.
                if random.random() < 0.7:
                    candidate_count = page.locator("a[href]").count()
                    if candidate_count > 0:
                        candidate_index = random.randint(0, max(0, candidate_count - 1))
                        candidate = page.locator("a[href]").nth(candidate_index)
                        click_element_human_like(page, candidate)

                # Optional random backtracking to homepage to make navigation less predictable.
                if random.random() < 0.5:
                    print(f"[session {session_id}] Returning to homepage")
                    open_page(page, SITE_URL)
                    random_wait(0.7, 2.5)

            except Exception as e:
                print(f"[session {session_id}] Failed to visit {link}: {e}")

        print(f"[session {session_id}] Finished browsing session")
        context.close()
        browser.close()


if __name__ == "__main__":
    main()
