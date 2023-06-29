import re
import time
import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs
import requests

headers = {
    "user-agent": "yuanrenxue,project",
    "cookie": "sessionid = d1a27034cc35827cae495c8bf3dff207|1686672101000"
}
timestamp = str(int(time.time() * 1000))

def main():
    bonus = 0
    total = 0
    for page_num in range(1, 6):
        url = "https://match.yuanrenxue.com/api/match/6?page=%s" % page_num
        page = page_num
        with open('/Users/lee/PycharmProjects/my_django_project/learn-ast/code/2去除僵尸代码.js', 'r', encoding='utf-8') as f:
            m_content = f.read()
            m = execjs.compile(m_content).call('z', timestamp, page)
        q = '%d-%s|' % (page, timestamp)
        params = {
            "m": m,
            "q": q
        }
        response = requests.get(url, headers=headers, params=params)
        num_three_total = 0
        for i in range(10):
            value = response.json()['data'][i]
            num = re.findall(r"'value': (.*?)}", str(value))[0]
            num_three_total += int(num)
        total_price = num_three_total * 24
        bonus += total_price
    total += bonus
    print(total)


if __name__ == '__main__':
    main()