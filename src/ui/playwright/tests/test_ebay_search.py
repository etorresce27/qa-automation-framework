import pytest
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError

@pytest.mark.smoke
def test_ebay_search_click_second_result(page):
    # Give the site more time in CI
    page.set_default_timeout(5000)

    page.goto("https://www.ebay.com", wait_until="domcontentloaded")

    # (Optional) handle consent banner if it appears
    # This is safe: try it, but don't fail if it's not there
    try:
        consent = page.get_by_role("button", name="Accept all")
        if consent.is_visible():
            consent.click()
    except Exception:
        pass

    # Search
    page.get_by_role("combobox", name="Search for anything").fill("iphone")
    page.locator("#gh-search-btn").click()

    # ✅ Wait until we're clearly on a results page
    # eBay usually loads results under #srp-river-results OR ul.srp-results
    results_container = page.locator("ul.srp-results")
    expect(results_container).to_be_visible(timeout=5000)

    items = page.locator("li.s-card")

    expect(items.first).to_be_visible(timeout=5000)
    second = items.nth(3).locator("a.s-card__link")

    # ---- capture the card title BEFORE clicking ----
    card_title = second.nth(1).locator("div.s-card__title").inner_text().strip()

    start_url = page.url

    # Dual-path: new tab OR same tab
    new_page = None
    try:
        with page.context.expect_page(timeout=3000) as new_page_info:
            second.first.click()
        new_page = new_page_info.value
    except PlaywrightTimeoutError:
        second.first.click()

    target = new_page if new_page else page
    target.wait_for_load_state("domcontentloaded")

    # If same tab, confirm URL changed
    if not new_page:
        expect(page).not_to_have_url(start_url)
    new_page = None

    # ---- ASSERT: new page title contains card title ----
    actual_title = target.title()

    assert actual_title[:10].lower() == card_title[:10].lower()


