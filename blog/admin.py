from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
import logging
from makefriends.custom_site import custom_site
from .models import Post, Category, Tag
from utils.qiniu.uploadFile import qiniu_upload

# Register your models here.


logger = logging.getLogger('django')


def make_obj_delete(modeladmin, requests, queryset):
    queryset.update(status=0)
    modeladmin.message_user(requests, '修改成功')


def make_obj_normal(modeladmin, request, queryset):
    queryset.update(status=1)
    modeladmin.message_user(request, "修改成功")


make_obj_normal.short_description = "更改状态为正常"
make_obj_delete.short_description = "更改状态为删除"


class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器：只展示当前用户分类 """
    title = '分类过滤器'  # 用于展示标题
    # 查询时URL参数的名字，比如查询分类id为1的内容时，URL后面的query部分是?owner_category=1.此时就可以通过我们的过滤器拿到这个id，从而进行过滤
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):  # 返回要展示的内容和查询用的id
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):  # 根据URL Query的内容返回列表页数据。
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'owner', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')
    list_filter = ('status', 'is_nav')
    actions = (make_obj_delete, make_obj_normal)
    actions_on_top = True
    actions_on_bottom = True

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = "文章数量"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')
    search_fields = ('name',)
    list_filter = ('status',)
    actions = (make_obj_delete, make_obj_normal)
    actions_on_top = True
    actions_on_bottom = True

    @qiniu_upload
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)

    @qiniu_upload
    def delete_model(self, request, obj):
        return super(TagAdmin, self).delete_model(request, obj)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status', 'owner', 'desc',
        'created_time', 'operator'
    ]
    list_display_links = []  # 用来配置哪些字段可以作为连接，点击它们，可以进入编辑页面。

    list_filter = [CategoryOwnerFilter, 'status', 'tag']  # 配置页面过滤器，需要通过哪些字段来过滤列表页
    search_fields = ['title', 'category__name']  # 配置搜索字段。

    actions = (make_obj_delete, make_obj_normal)
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
