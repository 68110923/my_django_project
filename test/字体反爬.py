import re
import requests
download_url = 'https://www.shixiseng.com/interns/iconfonts/file?rand=0.7275526622248008'
url = 'https://www.shixiseng.com/interns?keyword=python&city=%E5%85%A8%E5%9B%BD&type=intern'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}

resp = requests.get(url,verify=False)
result_txt = resp.text
pattern = re.compile(r'<span class="day font" data-v-2d75efc8>(.*?)-(.*?)/天</span>',re.S)
result = re.findall(pattern,result_txt)     #最低价与最高价组成一个元组，多个元组组成result列表，价格内容是&#xe049&#xe04d&#xe04d
for price_tuple in result:
    min_price = price_tuple[0]
    max_price = price_tuple[1]
    min_price_list = min_price.split('&#')[1:]
    min_value = ''
    for p in min_price_list:
        key = '&#'+p
        min_value += map_dic[key]
    min_price = min_value
    max_price_list = max_price.split('&#')[1:]
    max_value = ''
    for p in max_price_list:
        key = '&#' + p
        max_value += map_dic[key]
    max_price = max_value


