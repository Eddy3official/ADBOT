import os
import random
import time

from playwright.sync_api import sync_playwright


def env_bool(name, default):
    value = os.environ.get(name, str(default)).strip().lower()
    return value in {"1", "true", "yes", "on"}


MAX_SCRIPTS = int(os.environ.get("MAX_SCRIPTS", "5"))
ENABLE_SCROLL = env_bool("ENABLE_SCROLL", True)
ENABLE_MOUSE = env_bool("ENABLE_MOUSE", True)
ENABLE_REALISTIC_PAGE = env_bool("ENABLE_REALISTIC_PAGE", True)
BROWSER_PROFILE = os.environ.get("BROWSER_PROFILE", "windows_chrome")


RAW_SCRIPT_URLS = [
    "https://biomanos.org/21/bea2f4d4a6bfbf042d6cd6466716135f",
    "https://biomanos.org/14/5c055f49f20cc8a0a34744bbf12db88c",
    "https://benchform.org/1/b84630d703a03a7e96c22c1afe8a33bb",
    "https://apiguinee.org/4/f20f41770be276f92b69f5d1add3dbdc",
    "https://biomanos.org/21/09aeda79217f4822471a07965e809a7b",
]

SCRIPT_BUNDLES = [
    {
        "name": "biomanos_1",
        "inline": """
        window.atOptions = {
            'key' : 'f7a48efa48f67dce75713a2c7522f2dc',
            'format' : 'iframe',
            'height' : 250,
            'width' : 300,
            'params' : {}
        };
        """,
        "src": "https://biomanos.org/22/f7a48efa48f67dce75713a2c7522f2dc",
    },
    {
        "name": "biomanos_2",
        "inline": """
        window.atOptions = {
            'key' : '71b5cceefcc1d515b372c2468d5bfe07',
            'format' : 'iframe',
            'height' : 300,
            'width' : 160,
            'params' : {}
        };
        """,
        "src": "https://biomanos.org/22/71b5cceefcc1d515b372c2468d5bfe07",
    },
    {
        "name": "biomanos_3",
        "inline": """
        window.atOptions = {
            'key' : '81223dbe5c198c6004a99550c163cdc1',
            'format' : 'iframe',
            'height' : 600,
            'width' : 160,
            'params' : {}
        };
        """,
        "src": "https://biomanos.org/22/81223dbe5c198c6004a99550c163cdc1",
    },
    {
        "name": "biomanos_4",
        "inline": """
        window.atOptions = {
            'key' : 'ccfbba9c4b92473595e220318fa28ff3',
            'format' : 'iframe',
            'height' : 90,
            'width' : 728,
            'params' : {}
        };
        """,
        "src": "https://biomanos.org/22/ccfbba9c4b92473595e220318fa28ff3",
    },
    {
        "name": "biomanos_5",
        "inline": """
        window.atOptions = {
            'key' : '3b3f534eb459c8de9377dabf3bb32e2e',
            'format' : 'iframe',
            'height' : 60,
            'width' : 468,
            'params' : {}
        };
        """,
        "src": "https://biomanos.org/22/3b3f534eb459c8de9377dabf3bb32e2e",
    },
    {
        "name": "biomanos_6",
        "inline": """
        window.atOptions = {
            'key' : '3fe574499fecb8fd23bc44a8fa165c0d',
            'format' : 'iframe',
            'height' : 50,
            'width' : 320,
            'params' : {}
        };
        """,
        "src": "https://biomanos.org/22/3fe574499fecb8fd23bc44a8fa165c0d",
    },
]

DEVICE_PROFILES = {
    "windows_chrome": {
        "name": "windows_chrome",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "viewport": {"width": 1440, "height": 900},
        "device_scale_factor": 1,
        "is_mobile": False,
        "has_touch": False,
        "locale": "en-US",
        "timezone_id": "America/New_York",
    },
    "android_pixel": {
        "name": "android_pixel",
        "user_agent": "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
        "viewport": {"width": 412, "height": 915},
        "device_scale_factor": 2.75,
        "is_mobile": True,
        "has_touch": True,
        "locale": "en-US",
        "timezone_id": "America/Chicago",
    },
    "ios_ipad": {
        "name": "ios_ipad",
        "user_agent": "Mozilla/5.0 (iPad; CPU OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
        "viewport": {"width": 820, "height": 1180},
        "device_scale_factor": 2,
        "is_mobile": False,
        "has_touch": True,
        "locale": "en-US",
        "timezone_id": "America/Los_Angeles",
    },
}


def random_wait(min_seconds=1.0, max_seconds=7.0):
    time.sleep(random.uniform(min_seconds, max_seconds))


def pick_random_device():
    return DEVICE_PROFILES.get(BROWSER_PROFILE, DEVICE_PROFILES["windows_chrome"])


def install_fingerprint_mask(page):
    page.add_init_script(
        """
        (() => {
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
            Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8 });
            Object.defineProperty(navigator, 'deviceMemory', { get: () => 8 });
            Object.defineProperty(window, 'chrome', { get: () => ({}) });

            try {
                Object.defineProperty(navigator, 'userAgent', {
                    get: () => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
                });
            } catch (e) {}

            const originalGetContext = HTMLCanvasElement.prototype.getContext;
            HTMLCanvasElement.prototype.getContext = function(type, ...args) {
                const context = originalGetContext.call(this, type, ...args);
                return context;
            };

            try {
                const orig = WebGLRenderingContext.prototype.getParameter;
                WebGLRenderingContext.prototype.getParameter = function(parameter) {
                    if (parameter === 37445) return 'Google Inc.';
                    if (parameter === 37446) return 'Google SwiftShader';
                    return orig.call(this, parameter);
                };
            } catch (e) {}
        })();
        """
    )


def build_realistic_article_page(page):
    if not ENABLE_REALISTIC_PAGE:
        page.goto("about:blank", wait_until="domcontentloaded", timeout=60000)
        page.evaluate(
            """
            (() => {
                window.__bot_script_log = [];
                window.__bot_script_marker = false;
            })();
            """
        )
        return

    page.set_content(
        """
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <title>Latest Stories</title>
            <style>
              html, body { margin: 0; padding: 0; background: #f3f3f3; }
              body {
                font-family: Arial, Helvetica, sans-serif;
                color: #1f1f1f;
                line-height: 1.7;
              }
              .page {
                max-width: 1200px;
                margin: 0 auto;
                padding: 28px 20px 120px;
              }
              .hero {
                background: linear-gradient(135deg, #fefefe, #ededed);
                border-radius: 18px;
                padding: 28px;
                box-shadow: 0 8px 26px rgba(0,0,0,0.06);
                border: 1px solid #e9e9e9;
              }
              h1 {
                font-size: clamp(2rem, 4vw, 3.2rem);
                margin: 0 0 20px;
              }
              .meta {
                font-size: 14px;
                letter-spacing: 0.04em;
                color: #7b7b7b;
                text-transform: uppercase;
                margin-bottom: 18px;
              }
              .content {
                background: white;
                border-radius: 16px;
                padding: 28px;
                margin-top: 22px;
                box-shadow: 0 6px 18px rgba(0,0,0,0.05);
              }
              .ad-slot {
                background: #fafafa;
                border: 1px solid #e7e7e7;
                border-radius: 12px;
                min-height: 220px;
                padding: 14px;
                margin: 26px 0;
              }
              p {
                font-size: 18px;
                margin: 18px 0;
              }
              .cta {
                display: inline-block;
                padding: 10px 18px;
                background: #2b6ff2;
                color: white;
                border-radius: 8px;
                border: none;
                cursor: pointer;
              }
            </style>
          </head>
          <body>
            <div class="page">
              <div class="hero">
                <div class="meta">Technology · Daily Brief</div>
                <h1>What the next wave of browsing behavior looks like</h1>
                <p>Consumers are increasingly interacting with high-volume article pages, scrolling through content, and searching for the next relevant signal.</p>
              </div>

              <div class="content">
                <p>Reading behavior is often shaped by predictable patterns: users scroll, pause, click on related content, and naturally continue browsing.</p>
                <p>These page structures are intentionally more realistic to better mimic a genuine user-driven experience and improve script loading realism.</p>

                <div class="ad-slot" id="slot-1"></div>

                <p>As content moves downward, page reactions change. Human-like browsing tends to involve repeated gestures, short pauses, and natural cursor movement.</p>
                <p>This layered DOM structure helps keep the browser context believable before script execution begins.</p>

                <div class="ad-slot" id="slot-2"></div>

                <p>Real users usually interact with links, buttons, and inline content wrappers. These elements improve realism and allow the script to execute in a more natural environment.</p>
                <button class="cta" id="continue-btn">Continue</button>
              </div>
            </div>
          </body>
        </html>
        """,
        wait_until="load",
    )

    page.evaluate(
        """
        (() => {
            window.__bot_script_log = [];
            window.__bot_script_marker = false;
            window.__bot_script_log.push('page-ready');

            const btn = document.getElementById('continue-btn');
            if (btn) {
                btn.addEventListener('click', () => {
                    window.__bot_script_log.push('continue-button-clicked');
                }, { passive: true });
            }

            const article = document.querySelector('.content');
            if (article) {
                article.dataset.state = 'ready';
            }
        })();
        """
    )


def random_scroll(page):
    if not ENABLE_SCROLL:
        return

    metrics = page.evaluate(
        """
        () => {
            const maxY = Math.max(
                document.body ? document.body.scrollHeight : 0,
                document.documentElement ? document.documentElement.scrollHeight : 0,
                window.innerHeight
            );
            return { width: window.innerWidth, height: window.innerHeight, maxY };
        }
        """
    )
    if not metrics or metrics["maxY"] <= metrics["height"]:
        return

    scroll_target = random.randint(metrics["height"] // 2, metrics["maxY"] - 120)
    page.evaluate(f"window.scrollTo(0, {scroll_target})")
    random_wait(0.4, 1.3)
    page.mouse.wheel(0, random.randint(180, 550))
    random_wait(0.2, 0.8)


def random_mouse_move(page):
    if not ENABLE_MOUSE:
        return

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

    x = random.randint(15, max(15, metrics["width"] - 15))
    y = random.randint(15, max(15, metrics["height"] - 15))
    page.mouse.move(x, y, steps=random.randint(12, 28))
    random_wait(0.12, 0.7)


def simulate_user_behavior(page):
    for _ in range(random.randint(1, 3)):
        random_scroll(page)
        random_mouse_move(page)

    button = page.locator("#continue-btn")
    if button.count() > 0:
        box = button.bounding_box()
        if box:
            x = random.uniform(box["x"] + 10, box["x"] + box["width"] - 10)
            y = random.uniform(box["y"] + 10, box["y"] + box["height"] - 10)
            page.mouse.move(x, y, steps=random.randint(15, 30))
            random_wait(0.3, 0.8)
            page.mouse.down()
            page.mouse.up()
            random_wait(0.6, 1.6)


def execute_bundle(page, bundle):
    page.evaluate(bundle["inline"])
    page.evaluate(
        """
        (() => {
            window.__bot_script_log.push('inline-config-added');
            window.__bot_script_marker = true;
        })();
        """
    )
    random_wait(0.7, 1.8)

    page.add_script_tag(url=bundle["src"])
    page.evaluate(
        """
        (() => {
            window.__bot_script_log.push('external-script-loaded');
            window.__bot_script_marker = true;
        })();
        """
    )
    random_wait(1.2, 3.0)


def execute_raw_script(page, url):
    page.add_script_tag(url=url)
    page.evaluate(
        """
        (() => {
            window.__bot_script_log.push('raw-script-loaded');
            window.__bot_script_marker = true;
        })();
        """
    )
    random_wait(1.0, 3.0)


def script_pass_fail_summary(page, bundle_name, entry_type):
    result = page.evaluate(
        """
        () => {
            const log = window.__bot_script_log || [];
            const marker = !!window.__bot_script_marker;
            return {
                marker,
                log_count: log.length,
                log: log.slice(-10),
                passed: marker && log.length > 0
            };
        }
        """
    )
    return {
        "name": bundle_name,
        "type": entry_type,
        "status": "PASS" if result.get("passed") else "FAIL",
        "marker": result.get("marker", False),
        "log_count": result.get("log_count", 0),
        "log": result.get("log", []),
    }


def collect_script_entries():
    entries = []
    for url in RAW_SCRIPT_URLS:
        entries.append({"type": "raw", "url": url})
    for bundle in SCRIPT_BUNDLES:
        entries.append({"type": "bundle", "bundle": bundle})
    random.shuffle(entries)
    return entries[: min(MAX_SCRIPTS, len(entries))]


def main():
    device = pick_random_device()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-features=AudioServiceOutOfProcess",
                "--no-sandbox",
            ],
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
            accept_downloads=False,
        )
        context.set_default_timeout(60000)

        page = context.new_page()
        install_fingerprint_mask(page)
        build_realistic_article_page(page)

        random_wait(1.0, 2.2)
        simulate_user_behavior(page)

        selected_entries = collect_script_entries()
        results = []

        for i, entry in enumerate(selected_entries, 1):
            print(f"\n[{i}/{len(selected_entries)}] Starting script execution...")

            simulate_user_behavior(page)

            if entry["type"] == "raw":
                name = entry["url"]
                try:
                    execute_raw_script(page, entry["url"])
                    item = script_pass_fail_summary(page, name, "raw")
                    results.append(item)
                    print(f"RAW SCRIPT: {name} -> {item['status']}")
                    print("DETAILS:", item)
                except Exception as exc:
                    results.append({
                        "name": name,
                        "type": "raw",
                        "status": "FAIL",
                        "marker": False,
                        "log_count": 0,
                        "log": [str(exc)],
                    })
                    print(f"RAW SCRIPT FAILED: {name}: {exc}")

            else:
                bundle = entry["bundle"]
                try:
                    execute_bundle(page, bundle)
                    item = script_pass_fail_summary(page, bundle["name"], "bundle")
                    results.append(item)
                    print(f"BUNDLE: {bundle['name']} -> {item['status']}")
                    print("DETAILS:", item)
                except Exception as exc:
                    results.append({
                        "name": bundle["name"],
                        "type": "bundle",
                        "status": "FAIL",
                        "marker": False,
                        "log_count": 0,
                        "log": [str(exc)],
                    })
                    print(f"BUNDLE FAILED: {bundle['name']}: {exc}")

            simulate_user_behavior(page)
            random_wait(1.0, 2.5)

        passed = sum(1 for item in results if item["status"] == "PASS")
        failed = len(results) - passed

        print("\n=== FINAL PASS/FAIL SUMMARY ===")
        for item in results:
            print(f"{item['name']} | {item['type']} | {item['status']} | marker={item['marker']} | logs={item['log_count']}")
        print(f"TOTAL: {len(results)} | PASS: {passed} | FAIL: {failed}")

        context.close()
        browser.close()


if __name__ == "__main__":
    main()
