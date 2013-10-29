import slick.views as slick
from filter_views import FiltersMixin
from articles.models import (Contact, User, Writer, Reviewer, WRITER_POSITION,REVIEWER_POSITION)
from articles.forms import (WriterForm, ReviewerForm)
from django.contrib import messages

class ListWorkersBase(FiltersMixin, slick.ListView):
  template_name = "articles/contact_list.html"
  extra_context = {'row_template_name':"articles/worker_row.html"}
  search_on=['worker__username', 'worker__first_name', 'worker__last_name']

class ListRequestersBase(FiltersMixin, slick.ListView):
  model=Contact
  template_name = "articles/contact_list.html"
  extra_context = {'row_template_name':"articles/requester_row.html"}
  search_on=['requester__username', 'requester__first_name', 'requester__last_name']

class ListUsersBase(FiltersMixin, slick.ListView):
  model = User
  extra_context = {'row_template_name':"articles/user_row.html"}
  search_on = ['username','first_name','last_name']
  template_name = "articles/user_list.html"
################################################################################
#                               Writers                                  #
################################################################################
class ListPendingWriters(ListWorkersBase):
  model = Writer
  extra_context = {'heading':"Writers Pending Approval"}
  filter_on = ['writers_pending']

class ListMyWriters(ListWorkersBase):
  model = Writer
  extra_context = {'heading' : "My Writers"}
  filter_on = ['my_writers']
  # def get_queryset(self): 
  #   return Contact.objects.filter(requester=self.request.user, confirmation = True, position=WRITER_POSITION)

class ListAvailableWriters(ListUsersBase):
  extra_context = {
    'heading':"Available Writers", 
    'position':WRITER_POSITION,
  }
  filter_on = ['writers_available']
  def get_queryset(self):
    return self.filter_writers_available(User.writer_users.all())
  #   # Filter for users with writing contracts or users in writer mode
  #   queryset = queryset.filter(Q(contacts_as_worker__position=WRITER_POSITION)|Q(userprofile__mode=WRITER_MODE)).distinct()
  #   # Filter for users I dont have a contact for.
  #   return queryset.exclude(contacts_as_worker__requester=self.request.user).exclude(pk=self.request.user.pk)


################################################################################
#                               Reviewers                                      #
################################################################################

class ListPendingReviewers(ListWorkersBase):
  model = Reviewer
  extra_context = {'heading':"Reviewers Pending Approval"}
  filter_on = ['reviewers_pending']
class ListMyReviewers(ListWorkersBase):
  model = Reviewer
  extra_context = {'heading' : "My Reviewers"}
  filter_on = ['my_reviewers']
class ListAvailableReviewers(ListUsersBase):
  extra_context = {
    'heading':"Available Reviewers", 
    'position':REVIEWER_POSITION,
  }
  filter_on = ['reviewers_available']
  def get_queryset(self):
    return self.filter_reviewers_available(User.reviewer_users.all())
class ListMyRequesters(ListRequestersBase):
  extra_context = {'heading':"Requesters Pending Approval"}
  filter_on = ['requesters_pending']
class ListPendingRequesters(ListRequestersBase):
  extra_context = {'heading' : "My Requesters"}
  filter_on = ['my_requesters']
class ListAvailableRequesters(FiltersMixin, slick.ListView):
  extra_context = {
    'heading':"Available Requesters", 
  }
  filter_on = ['requesters_available']

################################################################################
#                               Ajax                                           #
################################################################################
class CreateContact(slick.FormWithUserMixin, slick.CreateView):
  extra_context = {
    'row_template_name':"articles/user_row.html",
  }
  template_name = "design/ajax_row.html"
  success_message = "Your request is awaiting approval from the other user."
  error_message = "There was a problem processing your request."
  def form_valid(self, form):
    self.object = form.cleaned_data['user_asked']
    self.object.contact = form.save()
    messages.success(self.request, self.success_message)
    context = self.get_context_data(form=form)
    context['hide_row'] = True
    return self.render_to_response(context)

class CreateWriter(CreateContact):
  model = Writer
  form_class = WriterForm

class CreateReviewer(CreateContact):
  model = Reviewer
  form_class = ReviewerForm
 
class ConfirmContact(slick.GenericModelView):
  model = Contact
  extra_context = {
    'hide_row':True,
    'row_template_name':"articles/worker_row.html",
  }
  template_name = "design/ajax_row.html"
  success_message = "The contact has been confirmed successfully."

  def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    self.object.confirmation=True
    self.object.save()
    messages.success(self.request, self.success_message)
    return self.render_to_response(self.get_context_data())


class DeleteContact(slick.AjaxDeleteView):
  success_message = "The contact has been deleted."
  model = Contact
  extra_context = {
    'hide_row':True,
    'row_template_name':"articles/worker_row.html",
  }
  template_name = "design/ajax_row.html"

class CancelContactRequest(DeleteContact):
  success_message = "The contact request has been canceled."

class RejectContactRequest(DeleteContact):
  success_message = "The contact request has been rejected."
