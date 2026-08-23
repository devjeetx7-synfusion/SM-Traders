import os
from playwright.sync_api import sync_playwright

viewports = [
    {"name": "mobile_320", "width": 320, "height": 568},
    {"name": "mobile_375", "width": 375, "height": 812},
    {"name": "mobile_412", "width": 412, "height": 915},
    {"name": "tablet_768", "width": 768, "height": 1024},
    {"name": "desktop_1280", "width": 1280, "height": 800}
]

os.makedirs("/home/jules/verification/screenshots", exist_ok=True)
os.makedirs("/home/jules/verification/videos", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for vp in viewports:
        context = browser.new_context(viewport={"width": vp["width"], "height": vp["height"]})
        page = context.new_page()
        page.goto(f"file://{os.path.abspath('theme.xml')}")
        page.wait_for_timeout(500)

        # Check horizontal scrollbar
        scroll_width = page.evaluate("document.documentElement.scrollWidth")
        client_width = page.evaluate("document.documentElement.clientWidth")
        has_horizontal_overflow = scroll_width > client_width
        print(f"Viewport {vp['name']} ({vp['width']}px): scrollWidth={scroll_width}, clientWidth={client_width}, overflow={has_horizontal_overflow}")

        page.screenshot(path=f"/home/jules/verification/screenshots/{vp['name']}.png")
        context.close()
    browser.close()
