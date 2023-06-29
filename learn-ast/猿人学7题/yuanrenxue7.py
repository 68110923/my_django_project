from fontTools.ttLib import TTFont
import requests
import base64
from io import BytesIO
from bs4 import BeautifulSoup
headers = {
    "user-agent": "yuanrenxue,project",
    "cookie": "sessionid = d1a27034cc35827cae495c8bf3dff207|1686672101000"
}

PIXELS = {
    '111': '',
    '10100100100101010010010010': '0',
    '1001101111': '1',
    '100110101001010101011110101000': '2',
    '10101100101000111100010101011010100101010100': '3',
    '111111111111111': '4',
    '1110101001001010110101010100101011111': '5',
    '10101010100001010111010101101010010101000': '6',
    '1111111': '7',
    '101010101101010001010101101010101010010010010101001000010': '8',
    '10010101001110101011010101010101000100100': '9'
}
name_list = [ '爷灬霸气傀儡', '梦战苍穹', '傲世哥', 'мaη肆風聲', '一刀メ隔世', '横刀メ绝杀', 'Q不死你R死你', '魔帝殤邪', '封刀不再战', '倾城孤狼', '戎马江湖',
            '狂得像风', '影之哀伤', '謸氕づ独尊', '傲视狂杀', '追风之梦', '枭雄在世', '傲视之巅', '黑夜刺客', '占你心为王', '爷来取你狗命', '御风踏血', '凫矢暮城', '孤影メ残刀',
            '野区霸王', '噬血啸月', '风逝无迹', '帅的睡不着', '血色杀戮者', '冷视天下', '帅出新高度', '風狆瑬蒗', '灵魂禁锢', 'ヤ地狱篮枫ゞ', '溅血メ破天', '剑尊メ杀戮',
            '塞外う飛龍', '哥‘K纯帅', '逆風祈雨', '恣意踏江山', '望断、天涯路', '地獄惡灵', '疯狂メ孽杀', '寂月灭影', '骚年霸称帝王', '狂杀メ无赦', '死灵的哀伤', '撩妹界扛把子',
            '霸刀☆藐视天下', '潇洒又能打', '狂卩龙灬巅丷峰', '羁旅天涯.', '南宫沐风', '风恋绝尘', '剑下孤魂', '一蓑烟雨', '领域★倾战', '威龙丶断魂神狙', '辉煌战绩', '屎来运赚',
            '伱、Bu够档次', '九音引魂箫', '骨子里的傲气', '霸海断长空', '没枪也很狂', '死魂★之灵']
rank_list = []
for page in range(1,6):
    url = f'https://match.yuanrenxue.cn/api/match/7?page={page}'
    resp = requests.get(url).json()

    c = base64.b64decode(resp['woff'].encode())
    # 将字节保存到文件
    with open('fontfile.ttf', mode='wb') as f:
        f.write(c)
    ttf = TTFont('fontfile.ttf')
    # 将下载后文件保存为ttf文件，方便在High-Logic FontCreator中打开
    ttf.saveXML('fontfile.ttx')
    ids = BeautifulSoup(open('fontfile.ttx', mode='r').read(), 'xml').find('glyf').find_all(
        'TTGlyph')  # .find('GlyphOrder').find_all('GlyphID')

    # 使用内存保存字体
    # font_bytes = BytesIO(base64.b64decode(resp['woff'].encode()))
    # font = TTFont(font_bytes)
    # font_bytes.close()
    # font_bytes = BytesIO()
    # font.saveXML(font_bytes)
    # ids = BeautifulSoup(font_bytes.getvalue(), 'xml').find('glyf').find_all(
    #     'TTGlyph')  # .find('GlyphOrder').find_all('GlyphID')
    # font_bytes.close()

    # gid = {}
    # for g in ids:
    #     gid[g['name']] = PIXELS[''.join(b['on'] for b in g.find_all('pt'))]


    gid = {}
    for g in ids:
        l = g.find_all('pt')
        gid[g['name']] = PIXELS[''.join([i['on'] for i in l])]


    for value_dic in resp['data']:
        index = resp['data'].index(value_dic)
        value = value_dic['value'] #  &#xc234 &#xb732 &#xb732 &#xb784
        value_list =  value.strip().split(' ')
        true_value_list = [gid[i.replace('&#x','uni')] for i in value_list] # unic234,unib732,unib732,unib784
        current_index = (page - 1) * 10 + index
        name = name_list[current_index]
        rank_dic = {}
        rank_dic['name'] = name
        rank_dic['rank'] = ''.join(true_value_list)
        rank_list.append(rank_dic)

result = max(rank_list,key=lambda x:int(x['rank']))
print(rank_list)
print(result['name'],result['rank'])