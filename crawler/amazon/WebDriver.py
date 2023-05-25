from playwright.sync_api import Playwright, sync_playwright, expect
import time




class WebDriver():

    def __init__(self):
        self.playwright = sync_playwright()
        self.playwright_start = self.playwright.start()
        self.browser = self.playwright_start.chromium.launch(headless=False)
        self.context = self.browser.new_context(geolocation={"latitude": 34.1227, "longitude": 118.7573},
                                                locale="en-UA",
                                                permissions=["geolocation"], timezone_id="America/Los_Angeles")
        self.page = self.context.new_page()
        self.temp(self.page)

    def temp(self, page):
        page.goto("https://www.amazon.com/",wait_until = "load")
        page.get_by_role("button", name="Submit").nth(1).click()
        page.get_by_role("textbox", name="or enter a US zip code").click()
        page.get_by_role("textbox", name="or enter a US zip code").fill("91301")
        time.sleep(0.3)
        page.locator("#GLUXZipUpdate").get_by_role("button", name="Apply").click(no_wait_after = True)
        page.get_by_role("button", name="Continue").click()
        time.sleep(2)

    def __del__(self):
        print('走了del函数')
        self.context.close()
        self.browser.close()
        self.playwright_start.stop()

    def run(self,playwright: Playwright):
        pass


