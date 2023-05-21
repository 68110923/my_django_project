from celery import Celery
import os
import django

# 把celery和django进行组合，识别和加载django的配置文件
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_django_project.settings')
django.setup()

# 创建celery实例对象
app = Celery("siteCelery")

# 通过app对象加载配置
app.config_from_object("site_celery.config")
# app.config_from_object("django.conf:settings")

# 加载任务
# 参数必须必须是一个列表，里面的每一个任务都是任务的路径名称
# app.autodiscover_tasks(["任务1","任务2"])
app.autodiscover_tasks(["site_celery.crawl_task1", "site_celery.crawl_task2"])

# 启动Celery的命令
# 切换目录到mycelery根目录下启动
# celery -A mycelery.main worker --loglevel=info