import requests

cookies = {
    'FSSBBIl1UgzbN7N80T': '4XEO6uPZ3JP1Zi.VXMBiNW8KvCb_8iAw8Ly9x7SAfWIGRsEBV3_9Apx8V5xOJBc7_6n26O11nLU7eTkx.1MjUhdvgfWIjAAbT3rgbKbeKrHo3YjGrY5f4qTWotU2f.Yoe9QFA1FgEaKm5qIYS4wU5bWLY2Q_nsx8JLGDYTJJQ_I2ODKfPNYcTIT4WDIBmq_gZM0HYjAREV_TQuvML5iDSokOMBuw2BKnXexs1qkGgSIX86LGthewmZvR7tF.6SrSrr87jEZZiv5AkmwYP1kETERrJk9XIjatnqolMIZP1EGyFea',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'FSSBBIl1UgzbN7N80T=4XEO6uPZ3JP1Zi.VXMBiNW8KvCb_8iAw8Ly9x7SAfWIGRsEBV3_9Apx8V5xOJBc7_6n26O11nLU7eTkx.1MjUhdvgfWIjAAbT3rgbKbeKrHo3YjGrY5f4qTWotU2f.Yoe9QFA1FgEaKm5qIYS4wU5bWLY2Q_nsx8JLGDYTJJQ_I2ODKfPNYcTIT4WDIBmq_gZM0HYjAREV_TQuvML5iDSokOMBuw2BKnXexs1qkGgSIX86LGthewmZvR7tF.6SrSrr87jEZZiv5AkmwYP1kETERrJk9XIjatnqolMIZP1EGyFea',
    'Pragma': 'no-cache',
    'Referer': 'http://www.fangdi.com.cn/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}

response = requests.get('http://www.fangdi.com.cn/new_house/new_house.html', cookies=cookies, headers=headers, verify=False)
print(response.text)
with open('first.html',mode='w') as f:
    f.write(response.text)
