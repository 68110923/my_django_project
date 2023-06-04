import time

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://antispider3.scrape.center/detail/7916054')
    time.sleep(5)
    result_list = page.query_selector_all('.m-b-sm.name .char')
    arr = []
    for span in result_list:
        text = span.text_content().strip()
        style_pos = int(span.get_attribute('style').replace('left: ','').strip('px;'))
        dic = {'text':text,'style_pos':style_pos}   #{'text': '风', 'style_pos': 75}
        arr.append(dic)
    arr = sorted(arr,key=lambda x:x['style_pos'])   #[{'text': '清', 'style_pos': 0}, {'text': '白', 'style_pos': 25}, {'text': '家', 'style_pos': 50}, {'text': '风', 'style_pos': 75}]
    result_str = ''.join(map(lambda x:x['text'],arr))   #'清白家风'
    print(result_str)
    browser.close()