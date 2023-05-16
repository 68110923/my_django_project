from django.contrib import admin
from django.utils.html import format_html

from sprier_manage.xmodels.task import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ('account', 'spider', 'name', 'frequency', 'status')  # 配置用户需要查询的model属性
    list_filter = ('account', 'spider', 'name', 'frequency', 'status')
    list_per_page = 20
    list_display = ['account', 'spider', 'name', 'frequency', 'status', 'params_text', 'params', 'create_time']

    # list_editable = ('host',)   # 可编辑字段
    # actions = ()    # 操作
