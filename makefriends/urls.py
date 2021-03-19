"""makefriends URL Configuration

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

from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from blog import views
from config.views import LinksView
from comment.views import post_comment

urlpatterns = [
    url(r'^backstage/', admin.site.urls, name='admin'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_name>\w+)/$', views.CategoryView.as_view(), name='category-list'),
    url(r'^tag/(?P<tag_name>\w+)/$', views.TagView.as_view(), name='tag-list'),
    url(r'^post/(?P<post_id>\d+).html$', cache_page(60*15)(views.PostDetailView.as_view()), name='post-detail'),
    url(r'^links/$', LinksView.as_view(), name='links'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^archives/$', views.ArchivesView.as_view(), name='archives'),
    url(r'^about/$', cache_page(60*15)(views.AboutView.as_view()), name='about'),
    url(r'^summary/(?P<summary_year>\d+)/$', cache_page(60*15)(views.SummaryView.as_view()), name='summary'),
    url(r'^atom\.xml/$', LatestPostFeed(), name="rss"),
    url(r'^sitemap\.xml/$', sitemap_views.sitemap, {'sitemaps': {'posts': PostSitemap}}),
    url(r'mdeditor/', include('mdeditor.urls')),
    url(r'^emoji/', include('emoji.urls')),
    url(r'^comment/post/(?P<post_id>[0-9]+)/$', post_comment, name='post_comment'),

]

admin.site.site_header = 'August Rush\'s Blog System'
admin.site.site_title = f'{admin.site.site_header}后台管理系统'
admin.site.index_title = f"欢迎使用{admin.site.site_header}后台管理系统"
admin.site.disable_action('delete_selected')

handler404 = views.HandleError.page_not_found
handler500 = views.HandleError.internal_server_error
