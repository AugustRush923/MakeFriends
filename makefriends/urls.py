"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.views.generic import TemplateView, RedirectView

from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from blog import views
from config.views import LinksView
from model.views import ModelView

urlpatterns = [
    url(r'^backstage/', admin.site.urls, name='admin'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_name>\w+)/$', views.CategoryView.as_view(), name='category-list'),
    url(r'^tag/(?P<tag_name>\w+)/$', views.TagView.as_view(), name='tag-list'),
    url(r'^post/(?P<post_id>\d+).html$', views.PostDetailView.as_view(), name='post-detail'),
    url(r'^links/$', cache_page(60 * 15)(LinksView.as_view()), name='links'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^archives/$', cache_page(60 * 15)(views.ArchivesView.as_view()), name='archives'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^summary/(?P<summary_year>\d+)/$', views.SummaryView.as_view(), name='summary'),
    # url(r'^atom\.xml/$', cache_page(60 * 15)(LatestPostFeed()), name="rss"),
    url(r'^atom\.xml/$', LatestPostFeed(), name="rss"),
    url(r'^sitemap\.xml/$', cache_page(60 * 15)(sitemap_views.sitemap), {'sitemaps': {'posts': PostSitemap}},
        name="sitemap"),
    url(r'^robots\.txt/$', cache_page(60 * 60 * 24)(
        TemplateView.as_view(template_name='robots.txt', content_type='text/plain')), name="robots"
        ),
    url(r'^favicon.ico/', cache_page(60 * 60 * 24)(
        RedirectView.as_view(url=r'/static/img/favicon.ico')), name="favicon"
        ),
    url(r'mdeditor/', include('mdeditor.urls')),
    url(r'^emoji/', include('emoji.urls')),
    # url(r'^models/$', cache_page(60 * 15)(ModelView.as_view()), name='models'),
    url(r'^models/$', ModelView.as_view(), name='models'),
]

admin.site.site_header = 'August Rush\'s Blog System'
admin.site.site_title = f'{admin.site.site_header}后台管理系统'
admin.site.index_title = f"欢迎使用{admin.site.site_header}后台管理系统"

handler404 = views.HandleError.page_not_found
handler500 = views.HandleError.internal_server_error


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
