from django.shortcuts import render
from site_celery.crawl_task1.tasks import add
from site_celery.crawl_task2.tasks import mul
from django.http import HttpResponse
from sprier_manage.xmodels.task import Task

from crawler.amazon.amazon_detail import get_data

def test_celery(request):
    # 从数据库中获取任务列表的数据然后将任务添加到celery中执行
    result_crawl_task1 = add.apply_async(args=[3, 5])
    result_crawl_task2 = mul.apply_async(args=[3, 5], queue="crawl_task2")
    print(result_crawl_task1.id)
    print(result_crawl_task2.id)
    print(result_crawl_task1.status)
    print(result_crawl_task2.status)
    # return HttpResponse("Celery works")
    return HttpResponse(result_crawl_task1.task_id + ":" + result_crawl_task1.status)





def add_task(request):

    result_task_detail = get_data.apply_async(args=[], queue="crawl_task1")
    # print(result_task_detail.id)
    # print(result_task_detail.status)
    str = f'detail --------- {result_task_detail.id}:{result_task_detail.status}\n'
    return HttpResponse(str)


