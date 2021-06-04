from django.core.cache import cache
from django.db import models
from django.utils.html import format_html


# Create your models here.


class Model(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    name = models.CharField(max_length=50, verbose_name='模型名称')
    sale_date = models.DateField(verbose_name='发售日')
    brand = models.CharField(max_length=50, verbose_name='模型品牌')
    series = models.CharField(max_length=50, verbose_name='系列')
    size = models.CharField(max_length=50, verbose_name='比例')
    character = models.CharField(max_length=50, verbose_name='角色', null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='购入价格')
    works = models.CharField(max_length=50, verbose_name='作品', null=True)
    img = models.ImageField(verbose_name='图片', null=True, upload_to="static/img")
    album = models.URLField(verbose_name='链接', null=True, blank=True)

    status = models.PositiveIntegerField(
        default=STATUS_NORMAL,
        choices=STATUS_ITEMS,
        verbose_name='状态'
    )
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '模型'

    def __str__(self):
        return self.name

    @classmethod
    def get_models(cls):
        models = cache.get('models')
        if not models:
            models = cls.objects.filter(status=1).order_by('created_time')
        return models

    def img_field(self):
        if self.img:
            return format_html(
                f'<img src="{self.img.url}" style="width:400px; height:450px; box-sizing: border-box;margin: auto;padding: 3px;" data-action="zoom"/>')
        return format_html("<strong>暂无上传照片。</strong>")

    img_field.allow_tags = True
    img_field.short_description = "照片"
