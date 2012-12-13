from django.conf.urls import patterns, url, include
from articles.views import ArticleList, ArticleCreate, ArticleUpdate, ArticleDelete, AjaxKeywordInlineForm, ProjectCreate

urlpatterns = patterns('',
    url(r'^list/$', ArticleList.as_view(), name='article_list'),
    url(r'^article/add/$', ArticleCreate.as_view(), name='article_add'),
    url(r'^project/add/$', ProjectCreate.as_view(), name='new_project'),
    url(r'^article/(?P<pk>\d+)/$', ArticleUpdate.as_view(), name='article_update'),
    url(r'^article/(?P<pk>\d+)/delete/$', ArticleDelete.as_view(), name='article_delete'),
    url(r'^keyword/new/$', AjaxKeywordInlineForm.as_view(), name='new_keyword'),
)
