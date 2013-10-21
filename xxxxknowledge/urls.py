from django.conf.urls.defaults import patterns, url
from knowledge.views import *

urlpatterns = patterns('knowledge.views',
    url(r'^$', 'knowledge_index', name='knowledge_index'),
    url(r'^articles/$', 'knowledge_list', name='knowledge_list'),
    url(r'^articles/(?P<category_slug>[a-z0-9-_]+)/$', 'knowledge_list', name='knowledge_list_category'),
    url(r'^articles/(?P<article_id>\d+)/$', 'knowledge_thread', name='knowledge_thread_no_slug'),
    url(r'^articles/(?P<article_id>\d+)/(?P<slug>[a-z0-9-_]+)/$', 'knowledge_thread', name='knowledge_thread'),
    url(r'^moderate/(?P<model>[a-z]+)/(?P<lookup_id>\d+)/(?P<mod>[a-zA-Z0-9_]+)/$', 'knowledge_moderate', name='knowledge_moderate'),
    url(r'^ask/$', 'knowledge_ask', name='knowledge_ask'),

    url(r'question/add/$', QuestionCreate.as_view(), name='question_add'),   
    #url(r'^question/(?P<question_id>\d+)/screenshot$', 'question_screenshot', name='question_screenshot'),
)
