# from django.template import loader, Context
# import sys
# from django.conf import settings
# from django.http import Http404, HttpResponseServerError
# __all__ = ('UpdateFilters', 'AvailableArticles', 'UnavailableArticles', 'AssignedArticles', 
#   'ClaimedArticles', 'SubmittedArticles', 'ApprovedArticles', 'RejectedArticles', 
#   'PublishedArticles', 'CreateArticle', 'UpdateArticle', 'ShowTag', 'AjaxNewKeyword', 
#   'RejectArticles', 'ApproveArticles', 'MarkArticlesAsPublished', 'PublishArticles', 
#   'SubmitArticles', 'DeleteArticles', 'ClaimAsWriter', 'ClaimAsReviewer', 'ReleaseAsWriter', 
#   'ReleaseAsReviewer', 'MakeAvailableToWriter', 'MakeAvailableToAllMyWriters', 
#   'MakeAvailableToAllWriters', 'MakeAvailableToReviewer', 'MakeAvailableToAllMyReviewers', 
#   'MakeAvailableToAllReviewers', 'MakeUnavailableToWriters', 'MakeUnavailableToReviewers', 
#   'AssignToWriter', 'AssignToReviewer', 'CreateProject', 'ShowProject', 'ListProjects', 
#   'DeleteProject', 'PublishArticle', 'TagArticle', 'ChangeMode', 'Dashboard', 'UserSettingsView', 
#   'ListPendingWriters', 'ListMyWriters', 'ListAvailableWriters', 'ListPendingReviewers', 
#   'ListMyReviewers', 'ListAvailableReviewers', 'ListMyRequesters', 'ListPendingRequesters', 
#   'ListAvailableRequesters', 'CreateWriter', 'CreateReviewer', 'ConfirmContact', 'DeleteContact', 
#   'CancelContactRequest', 'RejectContactRequest', 'ListWriterGroups', 'ListReviewerGroups', 
#   'AddGroup', 'RenameGroup', 'RemoveGroup', 'AddToGroup', 'RemoveFromGroup', 'ShowGroup')

from filter_views import UpdateFilters, FiltersMixin
from article_views import (AvailableArticles, UnavailableArticles, AssignedArticles, 
  ClaimedArticles, SubmittedArticles, ApprovedArticles, RejectedArticles, PublishedArticles, 
  CreateArticle, UpdateArticle, ShowTag, AjaxNewKeyword)
from multi_action_views import (RejectArticles, ApproveArticles, #MarkArticlesAsPublished, 
  PublishArticles, SubmitArticles, DeleteArticles, ClaimAsWriter, ClaimAsReviewer, ReleaseAsWriter, 
  ReleaseAsReviewer, MakeAvailableToWriter, MakeAvailableToAllMyWriters, MakeAvailableToAllWriters, 
  MakeAvailableToReviewer, MakeAvailableToAllMyReviewers, MakeAvailableToAllReviewers, 
  MakeUnavailableToWriters, MakeUnavailableToReviewers, AssignToWriter, AssignToReviewer, 
  MakeAvailableToWriterGroup, MakeAvailableToReviewerGroup)
from project_views import (CreateProject, ShowProject, ListProjects, DeleteProject, CreateCategory)
from single_action_views import (TagArticle)
from user_views import (ChangeMode, Dashboard, UserSettingsView, OutletConfigUpdate, OutletActivation, 
  OutletSettings, CreateOutletConfig, DeleteOutletConfig)
from contact_views import (ListPendingWriters, ListMyWriters, ListAvailableWriters, ListPendingReviewers, 
  ListMyReviewers, ListAvailableReviewers, ListMyRequesters, ListPendingRequesters, 
  ListAvailableRequesters, CreateWriter, CreateReviewer, ConfirmContact, DeleteContact, 
  CancelContactRequest, RejectContactRequest)
from group_views import (ListWriterGroups, ListReviewerGroups, AddGroup, RenameGroup, RemoveGroup, 
  AddToGroup, RemoveFromGroup, ShowGroup)

# def test500(request, template_name='admin/500.html'):
#   """
#   500 error handler.

#   Templates: `500.html`
#   Context: sys.exc_info() results
#    """
#   print "template_name = %s" % str(template_name)
#   t = loader.get_template(template_name) # You need to create a 500.html template.
#   ltype,lvalue,ltraceback = sys.exc_info()
#   sys.exc_clear() #for fun, and to point out I only -think- this hasn't happened at 
#                   #this point in the process already
#   if settings.DEBUG == False: settings.DEBUG = True
#   return HttpResponseServerError(t.render(Context({'type':ltype,'value':lvalue,'traceback':ltraceback})))
