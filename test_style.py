import os
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 390, "height": 844})
    page = context.new_page()
    page.goto(f"file://{os.path.abspath('theme.xml')}")
    page.wait_for_timeout(500)

    style_count = page.evaluate("document.querySelectorAll('style').length")
    print("Style tags count:", style_count)
    if style_count > 0:
        first_style = page.evaluate("document.querySelectorAll('style')[0].textContent.substring(0, 100)")
        print("First style snippet:", first_style)

    context.close()
    browser.close()
