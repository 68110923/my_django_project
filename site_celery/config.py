from celery.schedules import crontab
import datetime
from kombu import Exchange, Queue
# 可以用此种方式配置，但对于大项目来说用配置文件
# app.conf.task_serializer = 'json'
# app.conf.update(
#     task_serializer='json',
#     accept_content=['json'],  # Ignore other content
#     result_serializer='json',
#     timezone='Europe/Oslo',
#     enable_utc=True,
# )
# 配置文件6.0以后是这样
# broker_url = 'pyamqp://'
# result_backend = 'rpc://'
#
# task_serializer = 'json'
# result_serializer = 'json'
# accept_content = ['json']
# timezone = 'Europe/Oslo'
# enable_utc = True

# celery 配置
# CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
broker_url = 'redis://106.13.1.144:6379/1'
result_backend = "django-db"
# result_backend = 'redis://106.13.1.144:6379/2'
timezone = 'Asia/Shanghai'
timezone_aware = False

worker_concurrency = 10  # 并发worker数
# CELERYD_MAX_TASKS_PER_CHILD = 100  # 每个worker最多执行万100个任务就会被销毁，可防止内存泄露
task_track_started = True   # 任务在worker执行时将其状态报告为“已启动”
task_time_limit = 60 * 60 * 20  # 单个任务的运行时间不超过此值，否则会被SIGKILL 信号杀死 默认值：无时间限制。 任务超时时间限制20小时
result_backend_transport_options = {'visibility_timeout': 60 * 60 * 24}  # 24 hours
# CELERY_TASK_ALWAYS_EAGER = True
CELERYD_FORCE_EXECV = True  # 非常重要,有些情况下可以防止死锁
# CELERY_CACHE_BACKEND = 'default'
# 支持数据库django-db和缓存django-cache存储任务状态及结果
# 建议选django-db

# celery内容等消息的格式设置，默认json
accept_content = ['application/json', ]
task_serializer = 'json'
result_serializer = 'json'
enable_utc = False
beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

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
# 注意: 使用 redis 作为 broker 时, 队列名称,Exchange名称,queue名称 必须保持一致
# 默认队列的队列名为celery  不是default,当不指定队列名时会放到celery队列中。
task_routes = {

    "crawler.amazon.amazon_detail.*": {"queue": "crawl_task1"},
    "site_celery.crawl_task2.tasks.*": {"queue": "crawl_task2"},
    "*": {"queue": "default"},
}
# 定义celery各个队列的名称     x-max-priority是优先级 数字越大越先做
task_queues = (
    Queue("crawl_task1", Exchange("crawl_task1"), routing_key="crawler.amazon.amazon_detail.*",queue_arguments={'x-max-priority': 1}),
    Queue("crawl_task2", Exchange("crawl_task2"), routing_key="site_celery.crawl_task2.tasks.*",queue_arguments={'x-max-priority': 10}),
    Queue("default", Exchange("default"), routing_key="api.task.*"),
    # Queue('tasks', Exchange('tasks'), routing_key='tasks',queue_arguments={'x-max-priority': 10}),
)

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
    celery -A site_celery.main worker -l info -n workerA.%h -P eventlet -Q crawl_task1
    celery -A site_celery.main worker -l info -n workerB.%h -P eventlet -Q crawl_task2
    celery -A site_celery.main worker -l info -n workerB.%h -P eventlet --pool=solo

    # 启动定时任务
    # 当任务没有指定queue 则任务会加入default 队列 beat(定时任务也会加入default队列)
    # celery beat -A site_celery.main -l INFO
    # celery -A site_celery.main  beat -l info  -f logging/schedule_tasks.log --detach
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