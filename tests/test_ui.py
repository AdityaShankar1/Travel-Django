# tests/test_ui.py
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright

class TravelAppUITest(StaticLiveServerTestCase):
    def test_admin_access(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"{self.live_server_url}/admin/")
            assert "Log in" in page.title()
            browser.close()
