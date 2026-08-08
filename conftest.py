import os
import pytest
from playwright.sync_api import sync_playwright
from datetime import datetime


@pytest.fixture
def api_request():
    with sync_playwright() as p:
        request_context = p.request.new_context()
        yield request_context
        request_context.dispose()


@pytest.fixture
def page(request):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="videos"
        )
        context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True
        )
        # page = browser.new_page()
        page = context.new_page()
        yield page
        # Save the trace
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        trace_name = f"traces/{request.node.name}_{timestamp}.zip"
        context.tracing.stop(path=trace_name)
        # Then close context
        context.close()
        # Finally close browser
        browser.close()


@pytest.fixture
def monitor_page(page):
    js_errors = []
    console_errors = []
    http_errors = []

    page.on("pageerror",
            lambda e: js_errors.append(str(e)))

    page.on("console",
            lambda m: console_errors.append(m.text)
            if m.type == "error" else None)

    page.on("response",
            lambda r: http_errors.append(
                f"{r.status} {r.url}"
            ) if r.status >= 400 else None)

    yield page

    assert not js_errors, \
        f"JavaScript errors:\n{js_errors}"

    # assert not console_errors, \
    #     f"Console errors:\n{console_errors}"

    assert not http_errors, \
        f"HTTP errors:\n{http_errors}"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            os.makedirs("screenshots", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshots/{item.name}_{timestamp}.png"
            page.screenshot(
                path=filename,
                full_page=True
            )
            print(f"\nScreenshot saved: {filename}")
            html = page.content()
            filename_html = f"screenshots/{item.name}_{timestamp}.html"
            with open(filename_html, "w", encoding="utf8") as f:
                f.write(html)
            print(f"\nScreenshot html saved: {filename_html}")
