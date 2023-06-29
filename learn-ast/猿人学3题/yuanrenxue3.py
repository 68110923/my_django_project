import requests

session = requests.session()
session.headers = {
    'Content-Length': '0',
    'Accept': '*/*',
    'Referer': 'https://match.yuanrenxue.cn/match/3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'sessionid=1154smxwqjtfj3xyxm8nujqk4q4a5e98',
}

values = []
for index in range(1, 6):
    url = f"https://match.yuanrenxue.com/api/match/3?page={index}"
    session.post('https://match.yuanrenxue.cn/jssm')
    resp = session.get(url).json()['data']
    print(resp)
    for value_dic in resp:
        value = value_dic['value']
        values.append(value)
dic = {}
for value in values:
    if value in dic.keys():
        dic[value] += 1
    else:
        dic[value] = 1

result = max(dic.keys(),key = lambda x:dic[x])
print(result,dic[result])

