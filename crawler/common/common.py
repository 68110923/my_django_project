import time
from playwright.sync_api import Playwright
from playwright.sync_api import Page


class Browser:
    def start_playwright(self, _playwright: Playwright) -> Page:
        chromium = _playwright.chromium
        browser = chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        return page


class Common(Browser):
    def 假如我是一个完成的爬虫(self, page: Page, number: int):
        page.goto('https://juejin.cn/post/7159201395957039140')
        page.wait_for_timeout(1 * 1000)

        page2 = page.context.new_page()
        page2.goto('https://www.jianshu.com/u/235d8c52fe41')
        page2.close()

        page3 = page.context.browser.new_context().new_page()
        page3.goto('https://www.jianshu.com/u/235d8c52fe41')
        page3.context.close()

        print(f'我作为第{number}爬虫  我已经跑完全部我需要跑的东西了')
