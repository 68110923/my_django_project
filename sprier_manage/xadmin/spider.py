from django.contrib import admin
from django.utils.html import format_html

from sprier_manage.xmodels.spider import Spider


@admin.register(Spider)
class SpiderAdmin(admin.ModelAdmin):
    search_fields = ('platform', 'spider_name', 'spider_code', 'status')  # 配置用户需要查询的model属性
    list_filter = ('platform', 'spider_name', 'spider_code', 'status')
    list_per_page = 20
    list_display = ['platform', 'spider_name', 'spider_code', 'status',  'params_restrict', 'create_time']

    # list_editable = ('host',)   # 可编辑字段
    # actions = ()    # 操作
