from django.conf.urls import patterns, url, include
from articles.views import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^articles/$', ArticleList.as_view(), name='article_list'),
    url(r'^article/add/$', ArticleCreate.as_view(), name='article_add'),
    url(r'^project/add/$', ProjectCreate.as_view(), name='new_project'),
    url(r'^article/(?P<pk>\d+)/tag/$', TagArticle.as_view(), name='tag_article'),
    url(r'^projects/$', ProjectList.as_view(), name='project_list'),
    url(r'^project/(?P<pk>\d+)/delete/$', ProjectDelete.as_view(), name='project_delete'),
    url(r'^article/(?P<pk>\d+)/$', ArticleUpdate.as_view(), name='article_update'),
    url(r'^article/(?P<pk>\d+)/delete/$', ArticleDelete.as_view(), name='article_delete'),
    url(r'^keyword/new/$', AjaxKeywordInlineForm.as_view(), name='new_keyword'),
    url(r'^article/(?P<pk>\d+)/submit/$', ArticleSubmit.as_view(), name='article_submit'),
    url(r'^article/(?P<pk>\d+)/release/$', ArticleRelease.as_view(), name='article_release'),
    url(r'^article/(?P<pk>\d+)/approve/$', ArticleApprove.as_view(), name='article_approve'),
    url(r'^article/(?P<pk>\d+)/claim/$', ArticleClaim.as_view(), name='article_claim'),
    url(r'^article/(?P<pk>\d+)/assign/$', AssignArticle.as_view(), name='article_assign'),
    url(r'^article/(?P<pk>\d+)/reject/$', RejectArticle.as_view(), name='article_reject'),
    
    url(r'^various/assign/$', AssignVariousArticles.as_view(), name='assign_various_articles'),
    url(r'^various/reject/$', RejectVariousArticles.as_view(), name='reject_various_articles'),
    url(r'^various/approve/$', ApproveVariousArticles.as_view(), name='approve_various_articles'),
    url(r'^various/tag/$', TagVariousArticles.as_view(), name='tag_various_articles'),
    
    url(r'^requester/add/$', AddRequester.as_view(), name='requester_add'),
    url(r'^writer/add/$', AddWriter.as_view(), name='writer_add'),
    url(r'^writers/$', WriterList.as_view(), name='writer_list'),
    url(r'^requesters/$', RequesterList.as_view(), name='requester_list'),
    url(r'^relationship/(?P<pk>\d+)/delete/$', DeleteRelationship.as_view(), name='relationship_delete'),
    url(r'^relationship/(?P<pk>\d+)/confirm/$', ConfirmRelationship.as_view(), name='relationship_confirm'),

    url(r'^dashboard/$', direct_to_template, {'template': 'dashboard.html'}, name='dashboard'),
    

)
