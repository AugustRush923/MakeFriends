from datetime import date
from django.core.cache import cache
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Post, Tag, Category
from celery_tasks.count.tasks import increase_PV, increase_UV, increase_both
# Create your views here.


# 公共资源类
class CommonViewMixin:
    # 获取上下文方法
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'tag_list': Tag.get_tags(),  # 获取tag标签
            'category': Category.get_navs(),  # 获取分类
            'hot_post': Post.hot_posts(),  # 获取热门文章
        })
        return context


# 首页基类
class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 7
    context_object_name = 'post_list'
    template_name = 'blog/list.html'
    ordering = '-created_time'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context

    @staticmethod
    def pagination_data(paginator, page, is_paginated):
        if not is_paginated:
            return {}
        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }
        return data


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        category_name = self.kwargs.get('category_name')
        try:
            category = Category.objects.filter(name=category_name)
        except Category.DoesNotExist:
            raise Http404("Does not exist.")
        context.update({
            'cate': category,
        })

        return context

    def get_queryset(self):
        queryset = super(CategoryView, self).get_queryset()
        category_name = self.kwargs.get('category_name')
        return queryset.filter(category__name=category_name)


class ArchivesView(IndexView):
    template_name = 'blog/archives.html'
    paginate_by = False

    def get_context_data(self, **kwargs):
        context = super(ArchivesView, self).get_context_data()
        context.update({
            'dates': Post.archives()
        })
        return context


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        tag_name = self.kwargs.get('tag_name')
        try:
            tag = Tag.objects.filter(name=tag_name)
        except Tag.DoesNotExist:
            raise Http404("Does not exist.")
        context.update({
            'tag': tag
        })
        return context

    def get_queryset(self):
        queryset = super(TagView, self).get_queryset()
        tag_name = self.kwargs.get('tag_name')
        return queryset.filter(tag__name=tag_name)


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        context.update({
            # 'pre_post': Post.objects.filter(status=1).filter(created_time__gt=post.created_time).last(),
            'pre_post': Post.objects.filter(Q(status=1) & Q(created_time__lt=post.created_time)).first(),
            # 'next_post': Post.objects.filter(status=1).filter(created_time__lt=post.created_time).first(),
            'next_post': Post.objects.filter(Q(status=1) & Q(created_time__gt=post.created_time)).last(),
        })
        return context

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        post_id = self.object.id
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1 * 60)
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24 * 60 * 60)
        if increase_uv and increase_pv:
            increase_both.delay(post_id)
        elif increase_pv:
            increase_PV.delay(post_id)
        elif increase_uv:
            increase_UV.delay(post_id)


class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        queryset = super(SearchView, self).get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        result = queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))
        if not result:
            raise Http404
        return result


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super(AuthorView, self).get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)


class AboutView(PostDetailView):
    # queryset = None
    template_name = 'blog/about.html'
    context_object_name = 'about_post'
    pk_url_kwarg = 'about'

    def get_queryset(self):
        return Post.objects\
            .filter(title__exact='关于帅气的August Rush')\
            .only('id', 'title', 'content_markdown', 'owner', 'created_time', 'pv')

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404()
        return obj

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        return context


class SummaryView(PostDetailView):
    # queryset = Post.summary()
    template_name = 'blog/summary.html'
    context_object_name = 'summary'
    pk_url_kwarg = 'summary_year'

    def get_queryset(self):
        return Post.objects.filter(title__contains='年终总结')

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        queryset = queryset.filter(title=f'{pk}年终总结')\
            .only('id', 'title', 'content_markdown', 'owner', 'created_time', 'pv')
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404()
        return obj

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        return context


class HandleError:
    def page_not_found(request):
        return render(request, 'blog/404.html')

    def internal_server_error(request):
        return render(request, 'blog/500.html')
