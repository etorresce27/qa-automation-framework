import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.mark.smoke
def test_ebay_search_click_second_result():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.ebay.com", wait_until="domcontentloaded")

        # Search for iphone
        page.get_by_role("combobox").fill("iphone")
        page.get_by_role("button", name="Search").click()

        # Select the 2nd result
        results = page.locator("li.s-item")
        expect(results.nth(1)).to_be_visible()

        # Handle case where result opens in a new tab
        with context.expect_page() as new_page_info:
            results.nth(1).locator("a").first.click()

        new_page = new_page_info.value
        new_page.wait_for_load_state("domcontentloaded")

        # Minimal validation
        expect(new_page).to_have_title(lambda t: len(t) > 0)

        browser.close()
