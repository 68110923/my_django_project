from django.db import models

from sprier_manage.xmodels.spider import Spider
from sprier_manage.xmodels.account import Account


class Task(models.Model):
    choices_status = [
        (0, '待定'),
        (1, '启用'),
        (10, '弃用'),
        (11, '暂时不可用'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='账号')
    spider = models.ForeignKey(Spider, on_delete=models.CASCADE, verbose_name='爬虫')
    name = models.CharField('任务名称', max_length=32, default='未知任务名称')
    frequency = models.CharField('频次', max_length=16, default='未知频次')
    status = models.IntegerField('启用', default=0, choices=choices_status)
    params_text = models.CharField('参数映射', max_length=128, default='daily')
    params = models.JSONField('参数', blank=True, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        # managed = False  # 默认由Ture django管理
        # db_table = 'plat_logistics_track'   # 指定表
        verbose_name = f'任务'
        verbose_name_plural = '任务'
        unique_together = (
            ('account', 'spider', 'name'),
        )

    def __str__(self):
        return self.name
