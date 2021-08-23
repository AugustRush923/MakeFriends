from django.conf.urls import url
from django.views.decorators.cache import cache_page

from blog import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_name>\w+)/$', views.CategoryView.as_view(), name='category-list'),
    url(r'^tag/(?P<tag_name>\w+)/$', views.TagView.as_view(), name='tag-list'),
    url(r'^post/(?P<post_id>\d+).html$', views.PostDetailView.as_view(), name='post-detail'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^archives/$', cache_page(60 * 15)(views.ArchivesView.as_view()), name='archives'),
    # url(r'^(?P<about>about)/$', views.AboutView.as_view(), name='about'),
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    url(r'^summary/(?P<summary_year>\d+)/$', views.SummaryView.as_view(), name='summary'),
]