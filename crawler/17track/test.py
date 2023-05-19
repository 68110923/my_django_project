import time

from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
from crawler.common.common import Common


# 以下内容为调用程序
c = Common()
with sync_playwright() as _playwright:
    page = c.start_playwright(_playwright)
    for i in range(3):
        c.假如我是一个完成的爬虫(page, i)

    print(1)
