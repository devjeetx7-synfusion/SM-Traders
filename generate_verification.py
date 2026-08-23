import os
from playwright.sync_api import sync_playwright

os.makedirs("/home/jules/verification/screenshots", exist_ok=True)
os.makedirs("/home/jules/verification/videos", exist_ok=True)

theme_path = f"file://{os.path.abspath('theme.xml')}"

def run_cuj(page):
    page.goto(theme_path)
    page.wait_for_timeout(600)

    # Scroll to Hero
    page.wait_for_timeout(500)

    # Scroll to Services
    page.locator("#services").scroll_into_view_if_needed()
    page.wait_for_timeout(600)

    # Scroll to Solar & Diagram
    page.locator("#solar").scroll_into_view_if_needed()
    page.wait_for_timeout(600)

    # Scroll to Portfolio & interact with filter
    page.locator("#work").scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    page.get_by_role("button", name="SOLAR", exact=True).click()
    page.wait_for_timeout(600)

    # Scroll to Owners section
    page.locator("#owners").scroll_into_view_if_needed()
    page.wait_for_timeout(800)

    # Take screenshot at Owner section
    page.screenshot(path="/home/jules/verification/screenshots/verification.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mobile context for video recording
        context = browser.new_context(
            viewport={"width": 390, "height": 844},
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()
