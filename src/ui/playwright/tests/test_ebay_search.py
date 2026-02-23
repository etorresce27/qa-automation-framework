import pytest
from playwright.sync_api import expect

@pytest.mark.smoke
def test_ebay_search_click_second_result(page):
    
    page.goto("https://www.ebay.com", wait_until="domcontentloaded")

    # ✅ Avoid strict mode violation by specifying name
    page.get_by_role("combobox", name="Search for anything").fill("iphone")
    page.get_by_role("button", name="Search").click()

    results = page.locator("li.s-item")
    expect(results.nth(1)).to_be_visible()

    results.nth(1).locator("a").first.click()
    expect(page).to_have_title(lambda t: len(t) > 0)
