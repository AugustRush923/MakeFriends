from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django_redis import get_redis_connection
from django.core.cache import cache

from .models import Post, Category, Tag
from blog.actions import make_status_normal, make_status_delete, save_all
from blog.filters import CategoryOwnerFilter

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ('name', 'status', 'owner', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')
    list_filter = ('status', 'is_nav')
    actions = (make_status_normal, make_status_delete, 'make_is_nav_true', 'make_is_nav_false')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user

        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = "文章数量"

    def make_is_nav_true(self, requests, queryset):
        queryset.update(is_nav=True)
        self.message_user(requests, "修改成功！")

    make_is_nav_true.short_description = "设置所选分类名为导航"

    def make_is_nav_false(self, requests, queryset):
        queryset.update(is_nav=False)
        self.message_user(requests, "修改成功！")

    make_is_nav_false.short_description = "取消所选分类名为导航"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')
    search_fields = ('name',)
    list_filter = ('status',)
    actions = (make_status_normal, make_status_delete)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        return super(TagAdmin, self).delete_model(request, obj)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_per_page = 20

    list_display = [
        'title', 'category', 'status', 'owner', 'desc',
        'created_time', 'operator'
    ]
    list_display_links = []  # 用来配置哪些字段可以作为连接，点击它们，可以进入编辑页面。

    list_filter = [CategoryOwnerFilter, 'status', 'tag']  # 配置页面过滤器，需要通过哪些字段来过滤列表页
    search_fields = ['title', 'category__name']  # 配置搜索字段。

    actions = (make_status_normal, make_status_delete, save_all)
    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True

    exclude = ('owner',)

    fieldsets = (  # fieldsets用来控制页面布局
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',),
        }),
    )

    def operator(self, obj):  # 自定义函数的参数是固定的，就是当前行的对象
        return format_html(  # 自定义函数可以返回HTML，但是需要通过format_html函数处理，reverse是根据名称解析出URL地址
            '<a href="{}">编辑</a>',
            # reverse('admin:blog_post_change', args=(obj.id,))
            reverse('admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'  # 指定表头的展示文案

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
