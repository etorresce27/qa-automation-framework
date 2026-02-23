import pytest
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError

@pytest.mark.smoke
def test_ebay_search_click_second_result(page):
    page.goto("https://www.ebay.com", wait_until="domcontentloaded")

    # Unique search input (strict-safe)
    page.get_by_role("combobox", name="Search for anything").fill("iphone")

    # ✅ Strict-safe search button
    page.locator("#gh-search-btn").click()

    # Filter results to real items with links
    results = page.locator("li.s-item").filter(has=page.locator("a.s-item__link"))
    expect(results.first).to_be_visible()

    second = results.nth(1)
    expect(second).to_be_visible()

    link = second.locator("a.s-item__link").first
    start_url = page.url

    # Dual-path: new tab OR same tab
    new_page = None
    try:
        with page.context.expect_page(timeout=3000) as new_page_info:
            link.click()
        new_page = new_page_info.value
    except PlaywrightTimeoutError:
        link.click()

    target = new_page if new_page else page
    target.wait_for_load_state("domcontentloaded")

    # Validate title is non-empty
    expect(target).to_have_title(lambda t: len(t.strip()) > 0)

    # If same tab, confirm URL changed
    if not new_page:
        expect(page).not_to_have_url(start_url)
