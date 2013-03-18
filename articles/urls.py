from django.conf.urls import patterns, url, include
from articles.views import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^articles/$',                         ArticleList.as_view(),          name='article_list'),
    url(r'^article/add/$',                      ArticleCreate.as_view(),        name='article_add'),
    url(r'^article/(?P<pk>\d+)/tag/$',          TagArticle.as_view(),           name='tag_article'),
    url(r'^article/(?P<pk>\d+)/$',              ArticleUpdate.as_view(),        name='article_update'),
    url(r'^keyword/new/$',                      AjaxKeywordInlineForm.as_view(),name='new_keyword'),


    url(r'^projects/$',                         ProjectList.as_view(),          name='project_list'),
    url(r'^project/(?P<pk>\d+)/delete/$',       ProjectDelete.as_view(),        name='project_delete'),
    url(r'^project/add/$',                      ProjectCreate.as_view(),        name='new_project'),

    url(r'^articles/claimaswriter/$',           ClaimArticlesAsWriter.as_view(),  name='claim_articles_as_writer'),
    url(r'^articles/claimasreviewer/$',         ClaimArticlesAsReviewer.as_view(), name='claim_articles_as_reviewer'),
    url(r'^articles/assignwriter/$',            AssignWriterToArticles.as_view(),name='assign_writer'),
    url(r'^articles/assignreviewer/$',          AssignReviewerToArticles.as_view(),name='assign_reviewer'),
    url(r'^articles/reject/$',                  RejectArticles.as_view(),       name='reject_articles'),
    url(r'^articles/releasewriter/$',           ReleaseWriter.as_view(),        name='release_writer'),
    url(r'^articles/releasereviewer/$',         ReleaseReviewer.as_view(),      name='release_reviewer'),
    url(r'^articles/initialrelease/$',          InitialRelease.as_view(),       name='initial_release_articles'),
    url(r'^articles/approve/$',                 ApproveArticles.as_view(),      name='approve_articles'),
    url(r'^articles/submit/$',                  SubmitArticles.as_view(),       name='submit_articles'),
    url(r'^articles/tag/$',                     TagArticles.as_view(),          name='tag_articles'),
    url(r'^articles/delete/$',                  DeleteArticles.as_view(),       name='delete_articles'),

    
    url(r'^user/mode/$',                        ChangeModeView.as_view(),       name='change_user_mode'),
    
    url(r'^requester/add/$',                    AddRequester.as_view(),         name='requester_add'),
    url(r'^writer/add/$',                       AddWriter.as_view(),            name='writer_add'),
    url(r'^writers/$',                          WriterList.as_view(),           name='writer_list'),
    url(r'^requesters/$',                       RequesterList.as_view(),        name='requester_list'),

    url(r'^relationship/(?P<pk>\d+)/delete/$', DeleteRelationship.as_view(),    name='relationship_delete'),
    url(r'^relationship/(?P<pk>\d+)/confirm/$', ConfirmRelationship.as_view(),  name='relationship_confirm'),

    url(r'^dashboard/$', direct_to_template, {'template': 'dashboard.html'},    name='dashboard'),
    
    url(r'^spellcheck/$', spellcheck, name="spellcheck"), 

)
