#!/usr/bin/python
# -*- coding: utf-8 -*-
from playwright.sync_api import Playwright, sync_playwright, expect
import time,json,requests


''' 
使用：
    run(playwright) 是将cookies采集到文本形成cookie池
    test_cookie()   是调用cookie池获取数据

'''
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.zhihu.com/signin?next=%2F")
    page.goto("https://www.zhihu.com/")
    time.sleep(15)  # 此处手动扫码登录，然后到个人信息页再获取cookie
    cookies = context.cookies()
    str = json.dumps(cookies)
    # print('cookies:',str)
    with open('cookies.txt',mode="a") as f:
        f.write(f'{str}\n')
    browser.close()

# 此处是采集cookies的启动方法
with sync_playwright() as playwright:
    run(playwright)

def test_cookie():
    url = 'https://www.zhihu.com/'
    headers = {
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding' : 'gzip, deflate',
        'Accept-Language' : 'zh-CN,zh;q=0.9',
        'Referer' : 'https://www.baidu.com/link?url=zJczq6tBP109CP8eHoINOIQPioJzdiZDwIuvtckIHdS&wd=&eqid=f5ab89440001e253000000066479aa27',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }   #某乎的Accept-Encoding中含有br,拿到数据时会乱码，需要去掉才行
    with open('cookies.txt',mode='r') as f:
        cookie_list = f.readlines()
    for cookies in cookie_list:
        session = requests.session()
        session.headers = headers
        cookies = cookies.rstrip()   #去除结尾的换行
        cookies = json.loads(cookies)   #将cookies字符串转化为列表
        # print(type(cookies),cookies)
        for cookie in cookies:
            # print(cookie)
            session.cookies.set(cookie['name'],cookie['value'])
        resp = session.get(url)
        print('============================='+resp.text)

#此处调用cookie池获取数据
test_cookie()














