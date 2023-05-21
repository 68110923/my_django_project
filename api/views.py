from django.shortcuts import render
from site_celery.crawl_task1.tasks import add
from site_celery.crawl_task2.tasks import mul
from django.http import HttpResponse


def test_celery(request):
    result_crawl_task1 = add.apply_async(args=[3, 5], queue="crawl_task1")
    result_crawl_task2 = mul.apply_async(args=[3, 5], queue="crawl_task2")
    print(result_crawl_task1.id)
    print(result_crawl_task2.id)
    print(result_crawl_task1.status)
    print(result_crawl_task2.status)
    # return HttpResponse("Celery works")
    return HttpResponse(result_crawl_task1.task_id + ":" + result_crawl_task1.status)
