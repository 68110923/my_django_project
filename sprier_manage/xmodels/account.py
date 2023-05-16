from django.db import models

from sprier_manage.xmodels.platform import Platform


class Account(models.Model):
    platform = models.ForeignKey(Platform, on_delete=models.RESTRICT, verbose_name='平台')
    username = models.CharField('用户名', max_length=64, blank=True, null=True)
    password = models.CharField('密码', max_length=64, blank=True, null=True)
    phone = models.CharField('手机号', max_length=16, blank=True, null=True)
    status = models.BooleanField('可用状态', default=True, blank=True, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = f'账号'
        verbose_name_plural = verbose_name
        unique_together = (
            ('platform', 'username'),
        )

    def __str__(self):
        return f'{self.platform}-{self.username}'
