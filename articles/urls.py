from django.conf.urls import patterns, url, include
from articles.views import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^articles/\?view=Available$',         ArticleList.as_view(),            name='article_list'),
    url(r'^articles/\?view=Approved$',          ArticleList.as_view(),            name='approved'),
    url(r'^articles/\?view=Assigned$',          ArticleList.as_view(),            name='assigned'),
    url(r'^articles/\?view=Available$',         ArticleList.as_view(),            name='available'),
    url(r'^articles/\?view=Submitted$',         ArticleList.as_view(),            name='submitted'),
    url(r'^articles/\?view=Rejected$',          ArticleList.as_view(),            name='rejected'),
    url(r'^articles/\?view=Published$',         ArticleList.as_view(),            name='published'),
    url(r'^articles/\?view=Claimed$',           ArticleList.as_view(),            name='claimed'),
    url(r'^articles/\?view=Unavailable$',       ArticleList.as_view(),            name='unavailable'),
    url(r'^articles/$',                         ArticleList.as_view(),            name='article_list-alternate'),
    # url(r'^articles/mine/$',                    ArticleList.as_view(),           name='my_articles'),

    url(r'^article/add/$',                      ArticleCreate.as_view(),        name='article_add'),
    url(r'^article/(?P<pk>\d+)/tag/$',          TagArticle.as_view(),           name='tag_article'),
    url(r'^article/(?P<pk>\d+)/publish/$',      PublishArticle.as_view(),       name='publish_article'),
    url(r'^article/(?P<pk>\d+)/$',              ArticleUpdate.as_view(),        name='article_update'),
    url(r'^keyword/new/$',                      AjaxKeywordInlineForm.as_view(),name='new_keyword'),


    url(r'^projects/$',                         ProjectList.as_view(),          name='project_list'),
    url(r'^project/(?P<pk>\d+)/delete/$',       ProjectDelete.as_view(),        name='project_delete'),
    url(r'^project/add/$',                      ProjectCreate.as_view(),        name='new_project'),
    
    url(r'^category/add/$',                     CategoryCreate.as_view(),        name='new_category'),

    url(r'^articles/claim-as-writer/$',         ClaimAsWriter.as_view(),        name='claim_as_writer'),
    url(r'^articles/claim-as-reviewer/$',       ClaimAsReviewer.as_view(),      name='claim_as_reviewer'),
    url(r'^articles/release-as-writer/$',       ReleaseAsWriter.as_view(),      name='release_as_writer'),
    url(r'^articles/release-as-reviewer/$',     ReleaseAsReviewer.as_view(),    name='release_as_reviewer'),

    url(r'^articles/publish/$',                 PublishArticles.as_view(),      name='publish'),
    url(r'^articles/mark-as-published/$',       MarkArticlesAsPublished.as_view(), name='mark_as_published'),

    url(r'^articles/make-available-to-writer/$',  MakeAvailableToWriter.as_view(), name='make_available_to_writer'),
    url(r'^articles/make-available-to-all-writers/$',  MakeAvailableToAllWriters.as_view(), name='make_available_to_all_writers'),
    url(r'^articles/make-unavailable-to-writers/$',  MakeUnavailableToWriters.as_view(),  name='make_unavailable_to_writers'),
    
    url(r'^articles/make-unavailable-to-reviewers/$',MakeUnavailableToReviewers.as_view(),  name='make_unavailable_to_reviewers'),
    url(r'^articles/make-available-to-reviewer/$',  MakeAvailableToReviewer.as_view(),  name='make_available_to_reviewer'),
    url(r'^articles/make-available-to-all-reviewers/$',  MakeAvailableToAllReviewers.as_view(),      name='make_available_to_all_reviewers'),
    
    url(r'^articles/assign-to-writer/$',        AssignToWriter.as_view(),       name='assign_to_writer'),
    url(r'^articles/assign-to-reviewer/$',      AssignToReviewer.as_view(),     name='assign_to_reviewer'),

    # url(r'^articles/add-filter/$',               AddFilterView.as_view(),                name='add_filter'),
    # url(r'^articles/remove-filter/$',            RemoveFilterView.as_view(),             name='remove_filter'),
    url(r'^articles/update-filters/$',            UpdateFilters.as_view(),             name='update_filters'),

    url(r'^articles/reject/$',                  RejectArticles.as_view(),       name='reject_articles'),
    url(r'^articles/approve/$',                 ApproveArticles.as_view(),      name='approve_articles'),
    url(r'^articles/submit/$',                  SubmitArticles.as_view(),       name='submit_articles'),
    # url(r'^articles/tag/$',                     TagArticles.as_view(),          name='tag_articles'),
    url(r'^articles/delete/$',                  DeleteArticles.as_view(),       name='delete_articles'),

    url(r'^user/mode/$',                        ChangeModeView.as_view(),       name='change_user_mode'),

    url(r'^user/hire/$',                        WriterList.as_view(),   name='hire_user'),
    url(r'^user/apply/$',                       WriterList.as_view(),   name='apply_user'),
    url(r'^user/reject/$',                      WriterList.as_view(),   name='reject_user'),
    url(r'^user/accept/$',                      WriterList.as_view(),  name='accept_user'),
    
    # url(r'^requester/add/$',                    AddRequester.as_view(),         name='requester_add'),
    # url(r'^writer/add/$',                       AddWriter.as_view(),            name='writer_add'),
    url(r'^writers/$',                          WriterList.as_view(),           name='writer_list'),
    url(r'^requesters/$',                       RequesterList.as_view(),        name='requester_list'),
    url(r'^reviewers/$',                        ReviewerList.as_view(),         name='reviewer_list'),
    
    # url(r'^relationship/(?P<pk>\d+)/delete/$', DeleteRelationship.as_view(),    name='relationship_delete'),
    # url(r'^relationship/(?P<pk>\d+)/confirm/$', ConfirmRelationship.as_view(),  name='relationship_confirm'),

    url(r'^dashboard/$', direct_to_template, {'template': 'dashboard.html'},    name='dashboard'),


)
