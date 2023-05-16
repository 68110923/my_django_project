from django.contrib import admin
from django.utils.html import format_html

from sprier_manage.xmodels.platform import Platform


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    search_fields = ('name', 'dir_name')  # 配置用户需要查询的model属性
    list_filter = ('name', 'dir_name')
    list_per_page = 20
    list_display = ['name', 'dir_name', 'official_website', 'create_time']

    # list_editable = ('host',)   # 可编辑字段
    # actions = ()    # 操作

    def official_website(self, obj):
        return format_html(f'<a target="_blank" href="{obj.host}">官方网站</a>')

    official_website.allow_tags = True
    official_website.short_description = 'URL'
