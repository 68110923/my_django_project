from celery.schedules import crontab
import datetime
from kombu import Exchange, Queue

# celery 配置
# CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
BROKER_URL = 'redis://106.13.1.144:6379/1'
CELERY_TIMEZONE = 'Asia/Shanghai'
DJANGO_CELERY_BEAT_TZ_AWARE = False

CELERYD_CONCURRENCY = 20  # 并发worker数
CELERYD_MAX_TASKS_PER_CHILD = 100  # 每个worker最多执行万100个任务就会被销毁，可防止内存泄露
CELERYD_TASK_TIME_LIMIT = 60  # 单个任务的运行时间不超过此值，否则会被SIGKILL 信号杀死
# CELERY_TASK_ALWAYS_EAGER = True
CELERYD_FORCE_EXECV = True  # 非常重要,有些情况下可以防止死锁
# CELERY_CACHE_BACKEND = 'default'
# 支持数据库django-db和缓存django-cache存储任务状态及结果
# 建议选django-db
CELERY_RESULT_BACKEND = "django-db"
# celery内容等消息的格式设置，默认json
CELERY_ACCEPT_CONTENT = ['application/json', ]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
ENABLE_UTC = False
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# 定时任务配置如下

# CELERY_BEAT_SCHEDULER = {
#     'beat_task1': {
#         'task': 'schedule_add',
#         'schedule': datetime.timedelta(seconds=10),
#         'args': (2, 8)
#     },
#     # 'beat_task2': {
#     #     'task': 'mots_add',
#     #     'schedule': crontab(hour=4, minute=25),
#     #     'args': [4, 5]
#     # }
# }

# 定义celery各个队列的名称
CELERY_QUEUES = (
    Queue("default", Exchange("default"), routing_key="default"),
    Queue("crawl_task1", Exchange("crawl_task1"), routing_key="task_mots"),
    Queue("crawl_task2", Exchange("crawl_task2"), routing_key="task_btest")
)

# 注意: 使用 redis 作为 broker 时, 队列名称,Exchange名称,queue名称 必须保持一致
CELERY_ROUTES = {
    "*": {"queue": "default", "routing_key": "default"},
    "task*": {"queue": "crawl_task1", "routing_key": "task_mots"},
    "task2": {"queue": "crawl_task2", "routing_key": "task_btest"},
}

# 注意: 使用 redis 作为 broker 时, 队列名称,Exchenge名称,queue名称 必须保持一致

"""
这里只定义了两个队列
    crawl_task1: 用来存放需要优先执行的重要任务, 如果队列仍然存在堵塞的情况, 可以根据更小颗粒度划分出更多的队列
    crawl_task2: 用来存放执行级别较低的任务, 该类型的任务可以允许存在较长时间的延迟

进入manage.py 文件所在目录下, 执行以下命令, 开启worker, 因为我使用了django-celery模块,
所以可以使用manage.py 入口文件进行启动:    -Q  queue_name   指定队列名称

如果需要后台运行, 可在命令的最后加上 "&", 如果使用supervisor进行进程管理, 则不可以加上 "&", docker部署请自行参考docker 官方文档对 dockerfile 使用方式的说明.

注意: 这里添加了一个使用 celery 队列的worker, 因为在进行任务发送时, 如果没有指明队列, 将默认发送至队列名称为celery的队列中.

# -A 表示 应用目录  这里是celery_tasks.main

# -B 表示 定时任务

# -l 表示日志级别 这是英文小写l不是数字1

# -n woker名 自定义

# -Q 队列名

# .%h 对应不同主机ip  如果默认localhost，所以可以省略.%h

启动命令
    Celery -A site_celery.main worker -l info -n workerA.%h -P eventlet -Q crawl_task1
    Celery -A site_celery.main worker -l info -n workerB.%h -P eventlet -Q crawl_task2
    Celery -A site_celery.main worker -l info -n workerB.%h -P eventlet --pool=solo

    # 启动定时任务
    # 当任务没有指定queue 则任务会加入default 队列 beat(定时任务也会加入default队列)
    # celery beat -A site_celery.main -l INFO
    # Celery -A site_celery.main  beat -l info  -f logging/schedule_tasks.log --detach
    # --detach: 后台运行
    # -f logging/schedule_tasks.log : 后台输出路径pip
    # --scheduler : 指定获取定时任务的方式，这里是从后台数据库中获取
    # Celery -A site_celery.main  beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler -f logging/schedule_tasks.log --detach

"""

"""
from .tasks import send_emailMes_task

send_emailMes_task.apply_async((params_1, params_2), {"params_3_key": params_3_value}, queue="import_task")


需要注意的是:

使用异步任务对象下的apply_async(), 而不是delay(), 后者无法指定队列名称

参数:  (params_1, params_2),  使用这样的方式传递实参, 需要使用*agrs接收

参数:  {"active_token":token},  使用这样的方式传递命名参数, 需要使用**kwagrs接收

参数:  queue,  指定将任务发送至那个队列

五.完成以上操作以后就可以进行程序的执行了.
"""