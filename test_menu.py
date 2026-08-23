import os
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 375, "height": 812})
    page = context.new_page()
    page.goto(f"file://{os.path.abspath('theme.xml')}")
    page.wait_for_timeout(500)

    # Click mobile menu burger
    page.click("#smBurger")
    page.wait_for_timeout(300)
    is_open = page.is_visible("#smMobile.open")
    print("Mobile menu is open:", is_open)

    # Click close
    page.click("#smClose")
    page.wait_for_timeout(300)
    is_open = page.is_visible("#smMobile.open")
    print("Mobile menu after close:", is_open)

    context.close()
    browser.close()
