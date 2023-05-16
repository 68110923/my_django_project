from django.contrib import admin
from django.utils.html import format_html

from sprier_manage.xmodels.account import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    search_fields = ('platform', 'username', 'password', 'phone', 'status')  # 配置用户需要查询的model属性
    list_filter = ('platform', 'username', 'password', 'phone', 'status')
    list_per_page = 20
    list_display = ['platform', 'username', 'password', 'phone', 'status', 'create_time']

    # list_editable = ('host',)   # 可编辑字段
    # actions = ()    # 操作
