from django.contrib import admin
from django.utils.html import format_html

from sprier_manage.xmodels.server import Server


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    search_fields = ('ip', 'system', 'server_name', 'create_time')  # 配置用户需要查询的model属性
    list_filter = ('ip', 'system', 'server_name', 'create_time')
    list_per_page = 20
    list_display = ['ip', 'system', 'server_name', 'create_time']

    # list_editable = ('host',)   # 可编辑字段
    # actions = ()    # 操作