import execjs
import requests
import re
headers = {
    "user-agent": "yuanrenxue,project",
'Accept' : 'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding' : 'gzip, deflate, br',
'Accept-Language' : 'zh-CN,zh;q=0.9',
}


def main():
    value_total = []
    for page_num in range(1, 6):

        with open('decrypt.js', 'r', encoding='utf-8') as f:
            encrypt = f.read()
            m = execjs.compile(encrypt).call('getParams')

        cookies = {
            "sessionid": "pitg6xljib9czsxhznw3p02fnr4oib2b",
            "m": '7eabc39c5ee32fc5cfa9530957169f5e',
        }

        params = {
            # m: cfd08f558f0fab340cdeb2f2da1d0748丨1686999563
            "m": m,
            'page' : page_num,
        }
        url = "https://match.yuanrenxue.cn/api/match/1"

        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        resp_json = response.json()
        print(resp_json)

        for i in resp_json['data']:
            value_total.append(i['value'])

    avg = sum(value_total)/len(value_total)
    print(avg)



if __name__ == '__main__':
    main()