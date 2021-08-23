from django.contrib import admin

from model.models import Model
from blog.actions import make_status_normal, make_status_delete


# Register your models here.


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'series', 'size', 'character', 'status')

    search_fields = ('name', 'brand', 'series')
    list_filter = ('brand', 'series', 'size')

    actions = (make_status_normal, make_status_delete)
    actions_on_bottom = True

    ordering = ('created_time',)
    list_per_page = 10

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.fieldsets = (
            ('状态：', {
                'fields': (
                    'status',
                )
            }),
            ('基础信息：', {
                'fields': (
                    ("name", "character", "sale_date"),
                    ("brand", "series"), "works",
                    ("size", "price"),
                    "img",
                    "img_field",
                    "album",
                )
            }),
        )
        self.readonly_fields = ("img_field",)  # 务必将该字段设置为仅限可读, 否则抛出异常
        return super(ModelAdmin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    class Media:
        css = {'all': ("css/zoom.css",)}
        js = ("https://cdn.staticfile.org/jquery/1.11.1-rc2/jquery.min.js",
              "js/zoom.js",)
