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
    heat_value_total = []
    for page_num in range(1, 6):

        with open('decrypt.js', 'r', encoding='utf-8') as f:
            encrypt = f.read()
            encrypt_params = execjs.compile(encrypt).call('getCookie')

        cookies = {
            "sessionid": "jis4elbxx4lnm29w2q1vclroki27nj4u",
            "m": encrypt_params['cookie_m'],
            "RM4hZBv0dDon443M": encrypt_params['cookie_RM4']
        }

        params = {
            "m": encrypt_params['m'],
            "f": encrypt_params['f']
        }
        url = "https://match.yuanrenxue.cn/api/match/5?page=%s" % page_num

        response = requests.get(url, headers=headers, cookies=cookies, params=params)
        resp_json = response.json()
        print(resp_json)
        for i in range(10):
            value = response.json()['data'][i]
            heat_value = re.findall(r"'value': (.*?)}", str(value))[0]
            heat_value_total.append(heat_value)

    heat_value_total.sort(reverse=True)

    top_three_sum = 0
    for i in range(5):
        top_three_sum += int(heat_value_total[i])

    print(top_three_sum)


if __name__ == '__main__':
    main()