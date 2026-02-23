import pytest
import requests
from playwright.sync_api import expect

@pytest.mark.smoke
def test_form_result(page):
    page.set_default_timeout(5000)
    page.goto("https://demoqa.com/text-box", wait_until="domcontentloaded")

    # Fill out the form
    page.get_by_role("textbox", name="Full Name").fill("John Doe")
    page.get_by_role("textbox", name="name@example.com").fill("john.doe@example.com")
    page.get_by_role("textbox", name="Current Address").fill("123 Main St")
    page.locator("#permanentAddress").fill("456 Secondary St")
    page.get_by_role("button", name="Submit").click()

    # Validate UI output
    output = page.locator("#output")
    expect(output).to_contain_text("John Doe")
    expect(output).to_contain_text("john.doe@example.com")

    # API request validation
    res = requests.get("https://jsonplaceholder.typicode.com/posts/1", timeout=20)
    assert res.status_code == 200

    body = res.json()
    assert isinstance(body["id"], int)
    assert body["id"] == 1, f"Expected id to be 1 but got {body['id']}"
    assert isinstance(body["title"], str) and body["title"]
    assert isinstance(body["body"], str) and body["body"]
