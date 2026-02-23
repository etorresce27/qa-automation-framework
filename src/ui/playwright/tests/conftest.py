import os
import re
import pytest
from playwright.sync_api import sync_playwright

def _safe_name(name: str) -> str:
    # Replace anything weird with underscore for filenames
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", name)

@pytest.fixture(scope="session")
def browser():
    # One Playwright instance per test session
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-dev-shm-usage", "--no-sandbox"]
        )
        yield browser
        browser.close()

@pytest.fixture()
def page(browser, request):
    """
    Provides a Playwright Page and automatically:
    - starts tracing before each test
    - takes screenshot if test fails
    - saves trace.zip always (so artifacts/ is never empty)
    """
    os.makedirs("artifacts", exist_ok=True)

    context = browser.new_context()

    test_name = _safe_name(request.node.nodeid)

    # ✅ Start tracing (captures screenshots + DOM snapshots + sources)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()

    yield page

    # Determine whether the test failed
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    # ✅ Screenshot on failure
    if failed:
        try:
            page.screenshot(path=f"artifacts/{test_name}.png", full_page=True)
        except Exception as e:
            # Don't fail teardown if the page/browser crashed
            with open(f"artifacts/{test_name}.screenshot_error.txt", "w") as f:
                f.write(str(e))

    # ✅ Always save trace (so artifacts always has something)
        try:
            context.tracing.stop(path=f"artifacts/{test_name}.trace.zip")
        except Exception as e:
            with open(f"artifacts/{test_name}.trace_error.txt", "w") as f:
                f.write(str(e))

    context.close()

# Hook to access test outcome inside fixture
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)