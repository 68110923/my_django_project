import random

STATIC_IP = ''
USER_NAME = '1973844456@qq.com'
PASSWORD = 'a00000000'
KEYWORD = 'Smart Video Doorbell'
PLUGIN = 'aaa'
# ASINID = 'B0BV6LJ1X5' #第一页
ASINID = 'B0BZZ24PYJ'   #第三页
# ASINID = 'B0BZ3CB5NG'   #第六页
ZIP_CODE = '91301'


#浏览器启动参数
# chrome_param = [
#     '--disable-popup-blocking', #禁止弹窗
#     '--disable-blink-features=AutomationControlled',
#     '--disable-bundled-ppapi-flash',#禁用捆绑的PPAPI版本的Flash。
#     '--ignore-ssl-errors', #忽略ssl证书错误
#     '--ignore-certificate-errors',#忽略与证书相关的错误。
#     '--disable-gpu',#禁用GPU硬件加速。如果软件渲染器不到位，则GPU进程将无法启动。
#     '--disable-webrtc-encryption', #禁用WebRTC的RTP媒体加密。当Chrome嵌入内容时，它会在其稳定和测试版渠道上忽略此切换。
#     '--disable_non_proxied_udp',
#     'lang=en-us'
# ]
scroll_y = random.randint(500,1000)  #随机滚动距离在 像素之间
scroll_count = random.randint(1,3) #随机滚动次数 1- 3次之间
detail_look_time = random.randint(500,1000)/1000 #详情页浏览时间0.5-1秒之间，实际需要拉长






# https://www.amazon.co.uk/
# https://www.amazon.com/
# https://www.amazon.cn/
# LATITUDE = 34.1227 #经度
# LONGITUDE = 118.7573 #纬度
# LOCAL = "en-UA" #地区
# TIMEZONE = 'America/Los_Angeles' #时区

