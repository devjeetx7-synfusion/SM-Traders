import os
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 390, "height": 844})
    page = context.new_page()
    page.goto(f"file://{os.path.abspath('theme.xml')}")
    page.wait_for_timeout(500)
    bg = page.evaluate("window.getComputedStyle(document.body).backgroundColor")
    print("Computed body bg:", bg)
    context.close()
    browser.close()
