import os
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    # Test mobile
    context = browser.new_context(viewport={"width": 375, "height": 812})
    page = context.new_page()
    page.goto(f"file://{os.path.abspath('theme.xml')}")
    page.wait_for_timeout(500)

    # Verify Owner section rendered
    owners = page.query_selector_all(".sm-owner")
    print(f"Mobile Owners count: {len(owners)}")
    owner_text = page.inner_text("#owners")
    print("Owner section text preview:", owner_text[:200].replace('\n', ' '))

    # Verify Solar Diagram
    flow_nodes = page.query_selector_all(".sm-flow-node")
    print(f"Solar flow nodes count: {len(flow_nodes)}")

    # Test Filter pill click
    page.click("button[data-f='solar']")
    page.wait_for_timeout(300)
    visible_cards = page.query_selector_all(".sm-proj-card:not(.is-hidden)")
    print(f"Visible project cards for 'solar': {len(visible_cards)}")

    context.close()
    browser.close()
