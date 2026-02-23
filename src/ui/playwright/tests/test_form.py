import pytest
import requests
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError

@pytest.mark.smoke
def test_form_result(page):
    # Go to page
    page.set_default_timeout(5000)
    page.goto("https://demoqa.com/text-box", wait_until="domcontentloaded")

    # Fill out the form
    page.locator(".userName").fill("John Doe")
    page.locator(".userEmail").fill("john.doe@example.com")
    page.locator(".urrentAddress").fill("123 Main St")
    page.locator(".permanentAddress").fill("456 Secondary St")
    page.locator(".submit").click()
    # Validate data
    output = page.locator(".output")
    expect(output).to_have_text("John Doe")

    # api request validation
    res = requests.get("https://jsonplaceholder.typicode.com/posts/1", timeout=20)
    assert res.status_code == 200
    body = res.json()
    assert "id" in body and isinstance(body["id"], int)
    assert "name" in body and isinstance(body["name"], str) and body["name"]
    assert "title" in body and isinstance(body["title"], str) and body["title"]
    assert "body" in body and isinstance(body["body"], str) and body["body"]
