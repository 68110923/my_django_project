import config
import time
from site_element import jquery_dic
import random
import traceback

from playwright.sync_api import Playwright, sync_playwright, expect
current_page_number = 0
site = 'us'
def run(playwright: Playwright) -> None:
    #启动浏览器 无痕 非无头 设置地区 时区 经纬度
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
            geolocation={"latitude": 34.1227, "longitude": 118.7573},
            locale="en-UA",
            permissions=["geolocation"],
            timezone_id="America/Los_Angeles")
    page = context.new_page()

    #脚本开始  设置地址
    page.goto("https://www.amazon.com/ref=nav_logo",wait_until = "domcontentloaded", timeout=50*1000)
    wait_for_selector(page,'.a-button-input') # 等待选择地址
    element_list = get_jquery_all(page,'.a-button-input')# 点击选择地址
    element_list[1].click()
    page.wait_for_timeout(500)
    wait_for_selector(page,'#GLUXZipUpdateInput') #等待输入框出现
    get_jquery(page, '#GLUXZipUpdateInput', 'filltext', sleep_time=0.3,fill_text=config.ZIP_CODE)  # 输入邮编
    get_jquery(page, '#GLUXZipUpdate span span', 'click', sleep_time=1.5)  #点击apply
    page.get_by_role("button", name="Continue").click()  # 点击continue
    page.wait_for_timeout(3000)

    #登录
    # element =  wait_for_selector(page, '#nav-link-accountList')  # 等待登录入口
    element = page.wait_for_selector('#nav-link-accountList')
    page.wait_for_timeout(1000)
    element.click()

    get_jquery(page,'//*[@id="nav-link-accountList"]','click') #点击登录入口
    # get_jquery(page, '#nav-link-accountList','click') #点击登录入口

    wait_for_selector(page,'#ap_email') #等待输入账号
    get_jquery(page,'#ap_email','filltext',fill_text=config.USER_NAME) #输入账号
    get_jquery(page,'#continue','click') #点continue
    wait_for_selector(page,'#ap_password') #等待输入密码
    get_jquery(page,'#ap_password','filltext',fill_text=config.PASSWORD) #输入密码
    get_jquery(page,'#signInSubmit','click',sleep_time=1) #点击 sign in

    #搜索
    wait_for_selector(page,'#twotabsearchtextbox') #等待搜索框
    get_jquery(page,'#twotabsearchtextbox','filltext',fill_text=config.KEYWORD) #输入关键词
    get_jquery(page,'#nav-search-submit-button','click') #点击搜索

    is_find_asin = False #是否找到指定asin
    #查找指定asin跳转详情页
    for i in range(10):
        wait_for_selector(page,'.a-section.a-spacing-small.a-spacing-top-small') #等待出结果
        if i == 0:
            list_page_down_scroll(page) #下拉全局加载
        else:
            list_page_updown_scroll(page) #上下随机加载
        content = jquery_dic['.s-main-slot.s-result-list.s-search-results.sg-row div'].get(site, '.s-main-slot.s-result-list.s-search-results.sg-row div') #商品列表
        if page.query_selector_all(content):
            for asin_obj in page.query_selector_all(content):
                if asin_obj.get_attribute("data-asin") == config.ASINID:
                    print('找到asinid')
                    #随机浏览其他页面
                    asin_obj.query_selector('.a-section.a-spacing-base').click()
                    print('点击asin跳转详情')
                    is_find_asin = True
                    detail_look(page,is_add_cart = True)
                    break
                    #随机浏览其他页面
            if is_find_asin:
                break
            else:
                #点击下一页
                wait_for_selector(page,'.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator')
                get_jquery(page,'.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator','click')

    time.sleep(50000)
    context.close()
    browser.close()

#浏览详情页
def detail_look(page,is_add_cart = False):
    wait_for_selector(page,'#productTitle') #等待标题出现
    scroll_random(page)     #随机浏览详情
    if is_add_cart:
        add_cart(page)


#随机选择变体  加入购物车
def add_cart(page):
    wait_for_selector(page, '#add-to-cart-button')  #等待加购按钮出现
    if get_jquery(page,'#twister','is_exist'):  #如果存在变体
        result_list = get_jquery_all(page, '#twister li')   #获取变体列表
        var_choice = random.randint(0,len(result_list) - 1)     #随机点击除第0个以外的变体
        if var_choice != 0:
            result = result_list[var_choice]
            get_jquery(result,'.a-button-text','click')
            time.sleep(1)
    page.get_by_title("Add to Shopping Cart").click() #加购
    # get_jquery(page,'#add-to-cart-button','click')


# 查看评论，跳转评论详情
def comment_look():
    pass


# 列表页下拉随机滚动
def list_page_down_scroll(page):
    #随机次数  随机时长  随机下拉滚动长度
    count = random.randint(3, 5)
    for i in range(count):
        y = random.randint(1000, 1500)
        page.mouse.wheel(0, y)
        t = random.randint(300, 500) / 1000
        time.sleep(t)

# 列表页上下随机滚动
def list_page_updown_scroll(page):
    #随机次数  随机时长  随机下拉滚动长度
    count = random.randint(4, 6)
    for i in range(count):
        y = random.randint(-1500, 1500)
        page.mouse.wheel(0, y)
        t = random.randint(300, 500) / 1000
        time.sleep(t)

# 详情页随机滚动
def scroll_random(page):
    for i in range(config.scroll_count):
        page.mouse.wheel(0, config.scroll_y)
        time.sleep(config.detail_look_time)


# 对不同站点元素操作
def get_jquery(page,jquery,event,sleep_time = 0.0,fill_text = ''):
    '''
    封装方法  -元素  - 站点 - 操作（点击 ，填写，获取文本 获取标签列表   获取class属性  获取标签中的属性） - 延时 -填写的文本内容
    :param page: 浏览器页面
    :param jquery: 定位元素的jquery
    :param site: 亚马逊站点
    :param event: 事件  click点击 filltext填写文本 text获取文本 获取标签列表 获取class属性 获取标签中属性 is_exist是否存在返回布尔值
    :param time: 延时
    :param fill_text:文本填充内容
    :return:
    '''
    content = jquery_dic[jquery].get(site,jquery)

    if event == 'is_exist':
        if page.query_selector(content):
            return True
        else:
            return False

    if page.query_selector(content):
        print(f'element is {content}')
        element = page.query_selector(content)
        if event == 'click':
            element.click()
            print(f'click {content}')
        elif event == 'filltext':
            element.fill(fill_text)
            print(f'fill {content}')
        time.sleep(sleep_time)


# 获取不同站点元素列表
def get_jquery_all(page,jquery):
    '''
    封装方法  -元素  - 站点 - 操作（点击 ，填写，获取文本 获取标签列表   获取class属性  获取标签中的属性） - 延时 -填写的文本内容
    :param page: 浏览器页面
    :param jquery: 定位元素的jquery
    :return:
    '''
    content = jquery_dic[jquery].get(site,jquery)
    if page.query_selector_all(content):
        print(f'element list is {content}')
        element = page.query_selector_all(content)
        return element


# 元素等待
def wait_for_selector(page,jquery,state = 'visible',timeout = 20*1000,index = ''):
    '''
    等待元素
    :param page: 浏览器页面
    :param jquery: 定位元素jquery
    :param site: 站点
    :param state: attached：等待元素出现在DOM树中   detached：等待元素消失在DOM树中
        hidden：等待元素从DOM中分离出来，或者有一个空的边界框或visibility:hidden  visible：有非空的边界框和非visibility:hidden
    :param timeout:
    :param index 列表时的序号
    :return:
    '''
    content = jquery_dic[jquery].get(site, jquery)
    print(f'element is {content}')
    element = page.wait_for_selector(content, state=state, timeout=timeout)
    print(f'wait for {content}')
    return element


#启动demo
with sync_playwright() as playwright:
    try:
        run(playwright)
    except :
        # run(playwright)
        # print(f'playwright run error is {e}')
        print(traceback.format_exc())



