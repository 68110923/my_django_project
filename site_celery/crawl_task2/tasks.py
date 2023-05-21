from site_celery.main import app
from celery import shared_task
import time


@app.task(name='task2')
def mul(x, y):
    time.sleep(2)
    print("The btest_mul task has been run , result is : %s !" % str(x * y))
    return x * y


# 做定时任务
@app.task(name='schedule_add')
def share_add(x, y):
    time.sleep(2)
    print("--------------------------定时任务运行---------------------------------")
    print("The share_add task has been run , result is : %s !" % str(x + y))
    return x + y