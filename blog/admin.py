from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from makefriends.custom_site import custom_site
from .models import Post, Category, Tag
from utils.WordCloud import wordCloud


# Register your models here.
admin.site.site_header = 'August Rush\'s Blog'
admin.site.site_title = '后台管理系统'
admin.site.index_title = '欢迎使用后台管理系统'


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

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = "文章数量"


def wrapper(func):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        wordCloud.generate_word_cloud()
        return result

    return inner


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')
    search_fields = ('name',)
    list_filter = ('status',)

    @wrapper
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)

    @wrapper
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

    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True

    exclude = ('owner',)

    # fields = (  # fields配置有两个作用，一个是限定要展示的字段，另外一个就是配置展示字段的顺序
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    '''
           fieldsets用来控制布局，要求的格式是有两个元素的tuple和list,如：

           fieldsets = (
               (名称,{内容}),  #-->其中包含两个元素内容，第一个元素是当前版块的名称，第二个元素是当前版块的描述、字段和样式配置。
               (名称,{内容}),  #   也就是说，第一个元素是string，第二个元素是dict，而dict的key可以是‘fields’、‘description’、‘classes’
           )
        #  fields的配置效果和fields里一样，可以控制展示哪些元素，也可以给元素排序并组合元素的位置。
        #  classes的作用就是给要配置的版块加上一些CSS属性，Django admin默认支持的是collapse和wide。当然，你也可以写其他属性，然后自己来处理样式。
    '''
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

    # 关于编辑页的配置，还有针对多对多字段展示的配置filter_horizontal和filter_vertical
    # filter_vertical = ('tag',)    # 上下
    # filter_horizontal = ('tag',)    # 水平

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

    # 自定义静态资源引入
    # 我们可以通过自定义Media类来往页面上增加想要添加的JavaScript以及CSS资源。
    '''
    class Media:
        css = {
            'all': ("https://cdn.bootcss.com/bootstrap/4.0.0.-beta.2/css/bootstrap.min.css",),
        }
        js = ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/bootstrap.bundle.js",)
    '''
