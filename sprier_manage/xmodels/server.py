from django.db import models


class Server(models.Model):
    choices_system = [(i, i) for i in ['windows', 'mac', 'liunx']]

    ip = models.CharField('IP', max_length=16, unique=True)
    system = models.CharField('系统', choices=choices_system, max_length=32, db_index=True)
    server_name = models.CharField('服务器名', max_length=64, unique=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = f'服务器'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.server_name
