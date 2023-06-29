# Python 中集成了base64 模块，可用于对二进制数据进行编码解码操作：
# https://blog.csdn.net/weixin_43276033/article/details/124886105

import base64

a = 'hello world'
a = a.encode() #  b'hello world'
# 二进制数据就是字节类型  bytes类型
# 使用 base64.b64encode 进行编码时，只能是二进制数据，如果输入是 str 文本，将报错 TypeError。
# 而使用 base64.b64decode 解码时，字符串和字节都可以作为输入。
b = base64.b64encode(a)
print(b)
b = 'aHR0cHM6Ly93d3cubm1wYS5nb3YuY24v'
c = base64.b64decode(b)
print(c)
# base64.encode(input_file , out_file)   此方法是对文件的编码和解码


import io    #将字节在内存中读取
# 写入二进制数据到 BytesIO 对象中
data = b"Hello, World!"
bio = io.BytesIO()
bio.write(data)

# 从 BytesIO 对象中读取二进制数据
bio.seek(0)
read_data = bio.read()

print(read_data)  # 输出 b'Hello, World!'



import hashlib

str = '123456'
md5 = hashlib.md5()   				# 创建md5加密对象
md5.update(str.encode('utf-8'))  	# 指定需要加密的字符串
str_md5 = md5.hexdigest()  			# 加密后的字符串

print(str_md5)						# 结果：e10adc3949ba59abbe56e057f20f883e
