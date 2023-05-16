from django.db import models


class Platform(models.Model):
    name = models.CharField('平台', max_length=64, unique=True)
    dir_name = models.CharField('代码文件名', max_length=64, unique=True)
    host = models.CharField('URL', max_length=512)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = f'平台'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.dir_name
