import os
import threading
from site_celery.main import app
from crawler.amazon.WebDriver import WebDriver
from crawler.amazon.pipeline import MySQLPipline
from sprier_manage.xmodels.task import Task

@app.task(name='detail')
def get_data():
    mysql = MySQLPipline()
    try:
        web_driver = WebDriver()
    except:
        print('启动超时，重新添加任务')
        # get_data.apply_async(args=[])
        get_data.apply_async(args=[], queue="crawl_task1")
    redis_key = 'amazon_detail'
    page  = web_driver.page
    #从数据库中取asin 及 状态
    dict = {}
    dict['status'] = 0  # 待定
    dict['spider_id'] = 5
    while Task.objects.filter(**dict).exists():
        task_obj = Task.objects.filter(**dict).first()
        task_obj.status = 1  # 启用
        task_obj.save()

        # task_obj.frequency #频率
        # 状态码  task_obj.status   task_obj.choices_status  [(0, '待定'), (1, '启用'), (10, '弃用'), (11, '暂时不可用')]
        # 爬虫类型 task_obj.spider_id     1评论  5商品详情  6商品qa
        # 爬虫名称 task_obj.spider

        if task_obj.params:
            # print(type(task_obj.params))
            asin = task_obj.params['asinId']  # asinId
            url = f'https://www.amazon.com/dp/{asin}/ref=sr_1_1_sspa'
            page.goto(url, wait_until='domcontentloaded')  # ["commit", "domcontentloaded", "load", "networkidle"]
            data = {}
            data['asin_id'] = asin
            data['image'] = get_xpath(page, "//*[contains(@class,'imgTagWrapper')]/img", 'src')  # 主图
            data['ratings'] = get_xpath(page, '//*[@id="acrCustomerReviewText"]', text=True)  # 评论数
            data['answered_questions'] = get_xpath(page, '//*[@id="askATFLink"]/span', text=True)  # qa数量
            data['brand'] = get_xpath(page, '//*[@id="bylineInfo"]', text=True)  # 商标
            data['star_avg'] = get_xpath(page,
                                         '//*[@id="reviewsMedley"]//div[@class="a-row"]/span[@class="a-size-base a-nowrap"]/span[@data-hook="rating-out-of-text"]',
                                         text=True)  # 星评
            data['comment_url'] = get_xpath(page, '//*[@id="reviews-medley-footer"]/div[2]/a', 'href')
            data['qa_url'] = f'https://www.amazon.com/ask/questions/asin/{asin}'
            # get_xpath(page,"a:text-matches('See more answered questions.*')",'href',is_text=True)  #需要全局加载才行

            print(url, f'pageid是{id(page)}当前进程id{threading.current_thread().ident},线程id是{os.getppid()}')
            result = mysql.submit_item(data, redis_key)
            if not result:
                #mysql插入数据失败 标记暂不可以用
                task_obj.status = 11
                task_obj.save()
        else:
            #没有asinId 设为暂时不可用
            task_obj.status = 11
            task_obj.save()

    #所有数据全都爬取完毕   关闭浏览器
    web_driver.context.close()
    web_driver.browser.close()
    web_driver.playwright_start.stop()



def get_xpath(page,xpath,attribute = '',text = False,is_text = False):
    '''默认是通过xpath获取属性的 text为true获取文本  is_test为True是通过文本查找selector
    :param page: 浏览器对象
    :param xpath: 定位selector的xpath
    :param attribute: 获取的属性key
    :param text: 是否获取文本
    :param is_text: 是否通过文本定位selector
    :return:
    '''
    if attribute:
        if page.query_selector(xpath):
            if page.query_selector(xpath).get_attribute(attribute):
                a = data_clean(page.query_selector(xpath).get_attribute(attribute))
                return a
    elif text:
        if page.query_selector(xpath):
            if page.query_selector(xpath).text_content():
                a = data_clean(page.query_selector(xpath).text_content())
                return a
    return ''


def data_clean(str):
    #数据清洗
    str = str.replace('\n','',).strip().replace('"',"'").replace('\\','\\\\')
    return str




