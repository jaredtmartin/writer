from django.conf.urls import patterns, url, include
from articles.views import ArticleList, ArticleCreate, ArticleUpdate, ArticleDelete

urlpatterns = patterns('',
    url(r'^$', ArticleList.as_view(), name='article_list'),
    url(r'add/$', ArticleCreate.as_view(), name='article_add'),
    url(r'(?P<pk>\d+)/$', ArticleUpdate.as_view(), name='article_update'),
    url(r'(?P<pk>\d+)/delete/$', ArticleDelete.as_view(), name='article_delete'),
)
