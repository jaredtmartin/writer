from django.conf.urls import patterns, url, include
from articles.views import ArticleList

urlpatterns = patterns('',
    url(r'^$', ArticleList.as_view(), name='list'),
)
