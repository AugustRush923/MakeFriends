from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed

from .models import Post


# class ExtendedRSSFeed(Rss201rev2Feed):
#     def add_item_elements(self, handler, item):
#         super(ExtendedRSSFeed, self).add_item_elements(handler, item)
#         handler.addQuickElement('content:html', item['content_html'])


class LatestPostFeed(Feed):
    # feed_type = ExtendedRSSFeed
    # 显示在聚合阅读器上的标题
    title = "AugustRush923's Blog"
    # 通过聚合阅读器跳转到网站的地址
    link = r"/atom.xml/"
    # 显示在聚合阅读器上的描述信息
    description = "AugustRush923 is a blog power by django"

    # 需要显示的内容条目
    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL).order_by("-id")[:8]

    # 聚合器中显示的内容条目的标题
    def item_title(self, item):
        return item.title

    # 聚合器中显示的内容条目的描述
    def item_description(self, item):
        return item.content_markdown

    def item_link(self, item):
        return reverse('post-detail', args=[item.pk])

    # def item_extra_kwargs(self, item):
    #     return {'content_html': self.item_content_html(item)}
    #
    # def item_content_html(self, item):
    #     return item.content_markdown
