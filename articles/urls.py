from django.conf.urls import patterns, url, include
from articles.views import *
from django.views.generic.simple import direct_to_template
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = patterns('',
    url(r'^available/$', AvailableArticles.as_view(), name='available'),
    url(r'^unavailable/$', UnavailableArticles.as_view(), name='unavailable'),
    url(r'^assigned/$', AssignedArticles.as_view(), name='assigned'),
    url(r'^claimed/$', ClaimedArticles.as_view(), name='claimed'),
    url(r'^submitted/$', SubmittedArticles.as_view(), name='submitted'),
    url(r'^approved/$', ApprovedArticles.as_view(), name='approved'),
    url(r'^rejected/$', RejectedArticles.as_view(), name='rejected'),
    url(r'^published/$', PublishedArticles.as_view(), name='published'),
    # url(r'^articles/\?view=Available$',         ArticleList.as_view(),            name='article_list'),
    # url(r'^articles/\?view=Approved$',          ArticleList.as_view(),            name='approved'),
    # url(r'^articles/\?view=Assigned$',          ArticleList.as_view(),            name='assigned'),
    # url(r'^articles/\?view=Available$',         ArticleList.as_view(),            name='available'),
    # url(r'^articles/\?view=Submitted$',         ArticleList.as_view(),            name='submitted'),
    # url(r'^articles/\?view=Rejected$',          ArticleList.as_view(),            name='rejected'),
    # url(r'^articles/\?view=Published$',         ArticleList.as_view(),            name='published'),
    # url(r'^articles/\?view=Claimed$',           ArticleList.as_view(),            name='claimed'),
    # url(r'^articles/\?view=Unavailable$',       ArticleList.as_view(),            name='unavailable'),
    # url(r'^articles/$',                         ArticleList.as_view(),            name='article_list-alternate'),
    # url(r'^articles/mine/$',                    ArticleList.as_view(),           name='my_articles'),

    url(r'^article/add/$',                      ArticleCreate.as_view(),        name='article_add'),
    url(r'^article/(?P<pk>\d+)/tag/$',          TagArticle.as_view(),           name='tag_article'),
    url(r'^article/(?P<pk>\d+)/publish/$',      PublishArticle.as_view(),       name='publish_article'),
    url(r'^article/(?P<pk>\d+)/$',              UpdateArticle.as_view(),        name='article_update'),
    url(r'^keyword/new/$',                      AjaxKeywordInlineForm.as_view(),name='new_keyword'),
    url(r'^tag/(?P<slug>[-\w]+)/show/$',        ShowTag.as_view(),              name='show_tag'),

    url(r'^projects/$',                         ProjectList.as_view(),          name='project_list'),
    url(r'^project/(?P<pk>\d+)/delete/$',       ProjectDelete.as_view(),        name='project_delete'),
    url(r'^project/add/$',                      ProjectCreate.as_view(),        name='new_project'),
    url(r'^project/(?P<pk>\d+)/detail/$',       ProjectDetail.as_view(),        name='project_detail'),
    
    
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

    # url(r'^user/hire/$',                        WriterList.as_view(),   name='hire_user'),
    # url(r'^user/apply/$',                       WriterList.as_view(),   name='apply_user'),
    # url(r'^user/reject/$',                      WriterList.as_view(),   name='reject_user'),
    # url(r'^user/accept/$',                      WriterList.as_view(),  name='accept_user'),
    
    # url(r'^requester/add/$',                    AddRequester.as_view(),         name='requester_add'),
    # url(r'^writer/add/$',                       AddWriter.as_view(),            name='writer_add'),
    # url(r'^writers/$',                          WriterList.as_view(),           name='writer_list'),
    # url(r'^requesters/$',                       RequesterList.as_view(),        name='requester_list'),
    # url(r'^reviewers/$',                        ReviewerList.as_view(),         name='reviewer_list'),
    url(r'^my-writers/$', MyWritersList.as_view(), name = "my writers"),
    url(r'^available-writers/$', AvailableWritersList.as_view(), name = "writers avail."),
    url(r'^writers-pending/$', WritersPendingList.as_view(), name = "writers pending"),
    url(r'^my-reviewers/$', MyReviewersList.as_view(), name = "my reviewers"),
    url(r'^available-reviewers/$', AvailableReviewersList.as_view(), name = "reviewers avail."),
    url(r'^reviewers-pending/$', ReviewersPendingList.as_view(), name = "reviewers pending"),
    url(r'^my-requesters/$', MyRequestersList.as_view(), name = "my requesters"),
    url(r'^available-requesters/$', AvailableRequestersList.as_view(), name = "requesters avail."),
    url(r'^requesters-pending/$', RequestersPendingList.as_view(), name = "pending requesters"),

    url(r'^contact/(?P<pk>\d+)/create/$', CreateContact.as_view(),    name='create_contact'),
    url(r'^contact/(?P<pk>\d+)/delete/$', DeleteContact.as_view(),    name='delete_contact'),
    url(r'^contact/(?P<pk>\d+)/cancel_request/$', CancelContactRequest.as_view(), name='cancel_contact_request'),
    url(r'^contact/(?P<pk>\d+)/reject_request/$', RejectContactRequest.as_view(), name='reject_contact_request'),
    # url(r'^contact/writer/(?P<pk>\d+)/delete/$', DeleteWriterContact.as_view(),    name='delete_writer_contact'),
    # url(r'^contact/reviewer/(?P<pk>\d+)/delete/$', DeleteReviewerContact.as_view(),    name='delete_reviewer_contact'),
    url(r'^contact/(?P<pk>\d+)/confirm/$', ConfirmContact.as_view(),  name='confirm_contact'),

    url(r'^groups/writers/$', WriterGroupList.as_view(), name='writer groups'),
    url(r'^groups/reviewers/$', ReviewerGroupList.as_view(), name='reviewer groups'),
    url(r'^group/add/$', AddGroup.as_view(), name='add_group'),
    url(r'^group/(?P<pk>\d+)/delete/$', RemoveGroup.as_view(), name='remove_group'),
    url(r'^group/(?P<pk>\d+)/rename/$', RenameGroup.as_view(), name='rename_group'),
    url(r'^group/(?P<pk>\d+)/add-member/$', AddToGroup.as_view(), name='add_to_group'),
    url(r'^group/(?P<pk>\d+)/remove-member/$', RemoveFromGroup.as_view(), name='remove_from_group'),
    url(r'^group/(?P<pk>\d+)/detail/$', GroupDetail.as_view(), name='group_detail'),

    url(r'^dashboard/$', Dashboard.as_view(), name='dashboard'),

    url(r'^$', RedirectView.as_view(url=reverse_lazy('dashboard'))),

)
