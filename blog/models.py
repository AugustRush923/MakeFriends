import markdown
from django.db import models
from django.core.cache import cache
from django.db.models import Count, Case, When
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.functional import cached_property
import mistune

# Create your models here.
from mdeditor.fields import MDTextField


class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name='分类')
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL,
        choices=STATUS_ITEMS,
        verbose_name='状态')
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    owner = models.ForeignKey(User, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = "分类"

    def __str__(self):
        return self.name

    @classmethod
    def get_navs(cls):
        # categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        # nav_categories = []
        # normal_categories = []
        # for cate in categories:
        #     if cate.is_nav:
        #         nav_categories.append(cate)
        #     else:
        #         normal_categories.append(cate)
        navs = cache.get('navs')
        if not navs:
            navs = cls.objects.filter(Q(is_nav=True) & Q(status=cls.STATUS_NORMAL)).annotate(
                num_posts=Count(Case(When(post__status__exact=1, then=1))))
        cache.set('navs', navs)
        return {
            # Category.objects.annotate(Count(Case(When(post__status__exact=1, then=1))))
            # 'navs': cls.objects.filter(is_nav=True).annotate(num_posts=Count('post')),
            'navs': navs,
            # Django 2.0+
            # 'navs': cls.objects.filter(is_nav=True).annotate(num_posts=Count('post', filter=Q(post__status=1)),
            # 'categories': normal_categories,
        }


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=10, verbose_name='名称')
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL,
        choices=STATUS_ITEMS,
        verbose_name='状态')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.name

    @classmethod
    def get_tags(cls):
        # tag_list = cls.objects.annotate(num_posts=Count('post')).filter(status__exact=cls.STATUS_NORMAL)
        tag_list = cache.get('tag_list')
        if not tag_list:
            tag_list = cls.objects.filter(status=cls.STATUS_NORMAL).annotate(
                num_posts=Count(Case(When(post__status__exact=1, then=1))))
        cache.set('tag_list', tag_list)
        return tag_list


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    title = models.CharField(max_length=255, verbose_name='标题')
    desc = models.CharField(max_length=1024, blank=True, verbose_name='摘要')
    # content = models.TextField(verbose_name='正文', help_text='正文必须为MarkDown格式')
    content = MDTextField()
    content_markdown = models.TextField(blank=True, editable=False)
    # content = RichTextField(default='', verbose_name='正文', help_text="正文必须为MarkDown格式")
    content_html = models.TextField(verbose_name='正文html代码', blank=True, editable=False)
    status = models.PositiveIntegerField(
        default=STATUS_NORMAL,
        choices=STATUS_ITEMS,
        verbose_name='状态')
    category = models.ForeignKey(Category, verbose_name='分类')
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.content_html = mistune.markdown(self.content)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.tables',
            'markdown.extensions.sane_lists',
            'markdown.extensions.fenced_code',
        ])
        self.content_markdown = md.convert(self.content)
        super(Post, self).save(*args, **kwargs)

    @classmethod
    def latest_posts(cls):
        latest_posts = cache.get('latest_posts')
        if not latest_posts:
            latest_posts = cls.objects.filter(status=cls.STATUS_NORMAL)
        cache.set('latest_post', latest_posts)
        return latest_posts

    @classmethod
    def hot_posts(cls):
        hot_posts = cache.get('hot_posts')
        if not hot_posts:
            hot_posts = cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')[:12]
        cache.set('hot_posts', hot_posts)
        return hot_posts

    @classmethod
    def archives(cls):
        dates = cls.objects.datetimes('created_time', 'month', order='DESC')
        return dates

    @classmethod
    def about_me(cls):
        queryset = cls.objects.filter(title__exact='关于帅气的August Rush')
        return queryset

    @classmethod
    def summary(cls):
        queryset = cls.objects.filter(title__contains='年终总结')
        return queryset

    @cached_property
    def tags(self):
        return ','.join(self.tag.values_list('name', flat=True))
