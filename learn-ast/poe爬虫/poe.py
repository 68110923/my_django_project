import requests
import json
import ssl
ssl.create_default_context().load_verify_locations(cafile = '/Users/lee/anaconda3/envs/dj_celery_pro/lib/python3.10/site-packages/certifi/cacert.pem')
cookie_url = 'https://poe.com/'
headers = {
    'authority': 'poe.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}
#证书  '/Users/lee/anaconda3/envs/dj_celery_pro/lib/python3.10/site-packages/certifi/cacert.pem'
proxies = {'http': 'http://127.0.0.1:1087', 'https': 'http://127.0.0.1:1087'}
session = requests.Session()
# 设置代理IP
session.proxies= proxies
session.verify = '/Users/lee/anaconda3/envs/dj_celery_pro/lib/python3.10/site-packages/certifi/cacert.pem'
session.get(cookie_url)
session.get

# str = json.dumps(cookies)
# print('cookies:',str)