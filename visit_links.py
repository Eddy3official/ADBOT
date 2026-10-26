import os
import time
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright

SITE_URL = os.environ.get("SITE_URL", "https://steemstreamer.pages.dev")

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

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print(f"Opening {SITE_URL}")
        page.goto(SITE_URL, wait_until="networkidle", timeout=60000)

        time.sleep(2)

        # Get all internal links on the page
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

        browser.close()

if __name__ == "__main__":
    main()
