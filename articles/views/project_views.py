from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
import slick.views as slick
from articles.models import Project, Category
from articles.forms import ProjectForm, CategoryForm
from article_views import ArticleListBase
from django.views.generic import ListView
from django.core.urlresolvers import reverse_lazy

class AjaxUpdateMixin(object):
  success_message_template = 'The %s has been updated successfully.'
  error_message_template = 'Unable to create %s.'
  def get_context_data(self, **kwargs):
      kwargs['model_name']=self.object._meta.module_name
      return super(AjaxUpdateMixin, self).get_context_data(**kwargs)
  def get_success_message_template(self):
    return self.success_message_template
  def get_error_message_template(self):
    return self.error_message_template
  def form_valid(self, form):
    self.object = form.save()
    name=self.object._meta.verbose_name
    template=self.get_success_message_template
    # msg = self.get_success_message_template() % self.object._meta.verbose_name
    messages.success(self.request, self.get_success_message_template() % self.object._meta.verbose_name)
    return self.render_to_response(self.get_context_data(form=form))
  def form_invalid(self, form):
    messages.error(self.request, self.get_error_message_template() % self.object._meta.verbose_name)
    messages.error(self.request, form.errors)
    return super(AjaxUpdateMixin, self).form_invalid(form)

class SimpleRelatedCreate(slick.FormWithUserMixin, AjaxUpdateMixin, CreateView):
  # This is a base class for creating categories and projects
  # Takes name, owner, and article_id
  # Creates object with given name and owner and assignes it to article
  # Returns message and option and list item
  error_message_template = 'Unable to create %s with given name.'
  template_name = 'articles/simple_related_form.html'
  # def get_template_names(self):
  #   return[]

class CreateProject(SimpleRelatedCreate):
  model = Project
  form_class = ProjectForm

class ShowProject(ArticleListBase):
  model = Project
  owner_field_name = 'owner'
  def get_object(self): return get_object_or_404(Project.objects.all(),pk=self.kwargs['pk'])
  def get_queryset(self): return self.object.articles.all()
  def get(self, request, *args, **kwargs):
    self.object = self.get_object()
    return super(ShowProject,self).get(request, *args, **kwargs)

class ListProjects(ListView):
    model = Project
    search_fields = ['name']
    owner_field_name = 'owner'
    # filter_fields={
    #     'owner':Filter(base=Project, model=User, display_attr='username'),
    # }
    def get_context_data(self, **kwargs):
        kwargs['selected_tab']='projects'
        return super(ListProjects, self).get_context_data(**kwargs)

class DeleteProject(DeleteView):
    model = Project
    success_url = reverse_lazy('list_projects')

class CreateCategory(SimpleRelatedCreate):
  # Takes name, owner, and article_id
  # Creates Project with given name and owner and assignes it to article
  # Returns message and article project field with new item selected
  model = Category
  form_class = CategoryForm
