from django.db import models

from sprier_manage.xmodels.platform import Platform


class Spider(models.Model):
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, verbose_name='平台')
    spider_name = models.CharField('爬虫名', max_length=64)
    spider_code = models.CharField('爬虫编码', max_length=64)
    status = models.BooleanField('可用状态', db_index=True, default=True)
    params_restrict = models.JSONField('参数约定', blank=True, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = f'爬虫'
        verbose_name_plural = verbose_name
        unique_together = (
            ('platform', 'spider_code'),
        )

    def __str__(self):
        return f'{self.platform}-{self.spider_name}'
