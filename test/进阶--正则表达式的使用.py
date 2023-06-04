import re
pattern = r"([\w\.]+@[A-Za-z0-9]+)(\.[A-Za-z0-9]+){1,2}"    #适用于文本中匹配邮箱
a = re.findall(pattern,'dasdsa:adsa@139.com dsa')       #findall  返回所有结果到一个列表
print(type(a),a)                                        #<class 'list'> [('adsa@139', '.com')]   整个正则匹配的结果是adsa@139.com    返回的是两个()内的结果
a = re.finditer(pattern,'dasdsa:adsa@139.com dsa')      #finditer 返回所有结果到一个迭代器，迭代器里面是match对象，用group()查看
print(type(a),list(a)[0].group())                       #<class 'callable_iterator'>    adsa@139.com
a = re.search(pattern,'dasdsa:adsa@139.com dsa')        #search 任意位置开始匹配，匹配到一个结果就停止，有结果返回match对象，没有返回None,查看结果需用group()函数
print(type(a),a)                                        #<class 're.Match'> <re.Match object; span=(7, 19), match='adsa@139.com'>
a = re.match(pattern,'dasdsaadsa@139.com dsa')         #match 只能从头开始匹配，匹配到一个结果就停止，有结果返回match对象，没有返回None,查看结果需用group()函数
print(type(a),'\n'+a.group()+'\n'+a.group(1)+'\n'+a.group(2)+'\n'+a.group(0))
'''  
<class 're.Match'> 
dasdsaadsa@139.com
dasdsaadsa@139
.com
dasdsaadsa@139.com
可以看出group() 等价于 group(0)     group(1)是正则里的第一个()内的内容    group(2)是正则里的第二个()内的内容
'''
'''所以实际应用中，想要在文本中查找所有邮箱可以这样'''
pattern = r"([\w\.]+@[A-Za-z0-9]+(\.[A-Za-z0-9]+){1,2})"    #包含了   a.dsa@qq.com     和   3211s@qq.vip.com   这两种少见的情况
a = re.findall(pattern,'dasdsa:adsa@139.com dsadhaishi \n dgasdsas:dsa@qq.vip.com dsayu')    #这里面有效的邮箱是adsa@139.com和dsa@qq.vip.com
print(a)        #[('adsa@139.com', '.com'), ('dsa@qq.vip.com', '.com')]
# 从这里也可看出()有两种含义：1.写正则的时候，将表达式分组，便于对整组的数量的定义    2.想要专门输出结果的时候，可以给该内容设置()


#预加载正则表达式，可以反复使用此正则
# obj = re.compile(pattern)
# obj.match('要查找的字符串')
#
# #实际应用
# obj = re.compile(r'''br /><br /> href="(?P<url>.*?)">(?P<name>.*?)<strong>''',re.S)
# for result_iter in obj.finditer('要查找的字符串'):
#     result_dic = result_iter.groupdict()
#     print(result_dic['name'],result_dic['url'])