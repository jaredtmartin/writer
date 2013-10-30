import slick.views as slick
from filter_views import FiltersMixin
from articles.models import ContactGroup, WRITER_POSITION, REVIEWER_POSITION
from articles.forms import NewGroupForm, RenameGroupForm, GroupMemberForm

class ListGroups(FiltersMixin, slick.LoginRequiredMixin, slick.ListView):
  model = ContactGroup
  template_name = 'articles/contact_group_list.html'
  extra_context = {'row_template_name':"articles/contact_group_row.html"}

class ListWriterGroups(ListGroups):
  extra_context = {'heading':"Writer Groups",'position':WRITER_POSITION}
  filter_on = ['writer_groups']

class ListReviewerGroups(ListGroups):
  extra_context = {'heading':"Reviewer Groups",'position':REVIEWER_POSITION}
  filter_on = ['reviewer_groups']

class AddGroup(slick.LoginRequiredMixin, slick.AjaxCreateView):
  model = ContactGroup
  form_class = NewGroupForm
  extra_context = {'row_template_name':"articles/contact_group_row.html"}
  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.owner = self.request.user
    self.object = form.save()
    return super(AddGroup, self).form_valid(form)

class RenameGroup(slick.LoginRequiredMixin, slick.AjaxUpdateView):
  model = ContactGroup
  form_class = RenameGroupForm
  extra_context = {'row_template_name':"articles/contact_group_row.html"}

class RemoveGroup(slick.LoginRequiredMixin, slick.AjaxDeleteView):
  model = ContactGroup
  extra_context = {
    'row_template_name':"articles/contact_group_row.html",
    'hide_row':True,
  }

class AddToGroup(slick.NonModelFormMixin, slick.LoginRequiredMixin, slick.AjaxUpdateView):
  model = ContactGroup
  form_class = GroupMemberForm
  template_name = "articles/contact_group_detail_lists.html"
  def form_valid(self, form):
    self.object.contacts.add(form.cleaned_data['contact'])
    return HttpResponse("AOK.")


class RemoveFromGroup(slick.NonModelFormMixin, slick.LoginRequiredMixin, slick.AjaxUpdateView):
  model = ContactGroup
  form_class = GroupMemberForm
  extra_context = {
    'row_template_name':"articles/group_member_row.html",
    'hide_row':True,
  }
  def form_valid(self, form):
    self.object.contacts.remove(form.cleaned_data['contact'])
    return HttpResponse("AOK.")


class ShowGroup(FiltersMixin, slick.LoginRequiredMixin, slick.DetailView):
  model = ContactGroup
  template_name = 'articles/contact_group_detail.html'
  extra_context={
    'heading':'get_header',
    'worker_list':'get_workers'
  }
  def get_header(self): return self.object.name + " Group"
  def get_workers(self):
    return Contact.objects.filter(requester=self.request.user, confirmation=True, position=self.object.position).exclude(contactgroup=self.object).exclude(worker=self.request.user)
