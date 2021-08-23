from django.contrib import admin
from blog.models import Category


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
