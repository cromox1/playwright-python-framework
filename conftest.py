import os
import pytest
from playwright.sync_api import sync_playwright
from datetime import datetime

@pytest.fixture
def page(request):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
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
