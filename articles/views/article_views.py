import slick.views as slick
from filter_views import FiltersMixin
from articles.models import Article, REQUESTER_MODE, PublishingOutletConfiguration
from extra_views import UpdateWithInlinesView, CreateWithInlinesView 
from articles.forms import (CreateArticleForm, KeywordInlineFormSet, KeywordInline, QuantityForm, UpdateArticleForm,
    WriteArticleForm)
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import FormView
import pickle
from django.http import HttpResponse

class ArticleListBase(FiltersMixin, slick.LoginRequiredMixin, slick.ListView): 
  model = Article
  extra_context = {
    'all_items_count':'get_object_list_count',
    'hidden_columns':'get_hidden_columns',
    # 'filter_menus':'get_filter_menus',
    'all_columns':['Project','Keywords','Writer','Reviewer','Status','Category','Length','Priority','Tags'],
  }
  # Functions for getting info about list for doing actions on all
  def get_object_list_count(self): return self.object_list.count()
  def get_serialized_qs(self): return pickle.dumps(self.object_list.query)
  def get_serialized_model_qs(self): self.object_list.model
  def get_hidden_columns(self):
    if self.request.user.mode == REQUESTER_MODE: 
      return ['Reviewer','Status','Category','Length','Priority','Tags']
    else: return ['Writer','Reviewer','Status','Category','Length','Priority','Tags']
  def get(self, request, *args, **kwargs):
    self.request.session['article_list_view'] = self.request.path
    return super(ArticleListBase, self).get(request, *args, **kwargs)

  def get_filter_menus(self):
    return {
      'project':(('Big','1'),('Small','2'),('Medium','3')),
      'writer':(('Joe','1'),('Fred','2'),('Pam','3')),
      }
  # def get_context_data(self, **kwargs):
  #   if self.request.user.mode == REQUESTER_MODE:
  #     kwargs['writer_list'] = self.request.user.writers.all()
  #     kwargs['reviewer_availability_list'] = self.request.user.reviewers.all()
  #   return super(ArticleListBase, self).get_context_data(**kwargs)
  
class AvailableArticles(ArticleListBase):
  search_on = ['tags','project__name','keyword__keyword']
  filter_on = ['available', 'project','available_to_writer']
  extra_context={
    # 'hidden_columns':['Writer','Reviewer','Status','Category','Length','Priority','Tags'],
    'heading':'Available Articles',
  }

class UnavailableArticles(ArticleListBase):
  search_on = ['tags','project__name','keyword__keyword']
  filter_on = ['unavailable', 'project']
  extra_context = {
    'hidden_columns':['Writer','Reviewer','Status','Category','Length','Priority','Tags'],
    'heading':'Unavailable Articles',
  }
class AssignedArticles(ArticleListBase):
  search_on = ['tags','project__name','keyword__keyword']
  filter_on = ['assigned', 'project','writer']
  extra_context = {'heading':'Assigned Articles'}

class ClaimedArticles(ArticleListBase):
  search_on = ['tags','project__name','keyword__keyword']
  filter_on = ['claimed', 'project','writer']
  extra_context = {'heading':'Claimed Articles'}
class SubmittedArticles(ArticleListBase):
  search_on = ['tags','project__name','keyword__keyword']
  filter_on = ['submitted', 'project','writer']
  extra_context = {'heading':'Submitted Articles'}
class ApprovedArticles(ArticleListBase):
  search_on = ['tags','project__name','keyword__keyword']
  filter_on = ['approved', 'project','writer']
  extra_context = {'heading':'Approved Articles','publishing_outlets':'get_publishing_outlets'}
  def get_publishing_outlets(self):
    return PublishingOutletConfiguration.objects.filter(user=self.request.user, active=True)
class RejectedArticles(ArticleListBase):
  search_on = ['tags','project__name','keyword__keyword']
  filter_on = ['rejected', 'project','writer']
  extra_context = {'heading':'Rejected Articles'}
class PublishedArticles(ArticleListBase):
  search_on = ['tags','project__name','keyword__keyword']
  filter_on = ['published', 'project','writer']
  extra_context = {'heading':'Published Articles','publishing_outlets':'get_publishing_outlets'}
  def get_publishing_outlets(self):
    print "PublishingOutletConfiguration.objects.filter(user=self.request.user, active=True) = %s" % str(PublishingOutletConfiguration.objects.filter(user=self.request.user, active=True))
    return PublishingOutletConfiguration.objects.filter(user=self.request.user, active=True)

class CreateArticle(slick.ExtraContextMixin, FiltersMixin, slick.FormWithUserMixin, slick.LoginRequiredMixin, CreateWithInlinesView):
  template_name = 'articles/article_edit.html'
  model = Article
  form_class=CreateArticleForm
  context_object_name = 'article'
  extra_context = {'heading':'New Article'}
  inlines = [KeywordInlineFormSet]
  def get_context_data(self, **kwargs):
      kwargs['article']=self.object
      context = super(CreateArticle, self).get_context_data(**kwargs)
      return context
  def forms_valid(self, form, inlines):
      response = super(CreateArticle, self).forms_valid(form, inlines)
      # If number_of_articles was specified, clone the model that many times
      if 'number_of_articles' in form.cleaned_data and form.cleaned_data['number_of_articles']:
        form.cleaned_data['number_of_articles']-1
        keywords = list(self.object.keyword_set.all())
        # Do one less since we already had one instance
        for x in xrange(form.cleaned_data['number_of_articles']-1):
          self.object.pk = None
          self.object.save()
          for keyword in keywords:
            keyword.pk = None
            keyword.article = self.object
            keyword.save()
      return response
  def get_success_url(self):
    return self.request.session.get('article_list_view', reverse('available'))

class UpdateArticle(slick.ExtraContextMixin, FiltersMixin, slick.LoginRequiredMixin, UpdateWithInlinesView):
  model = Article
  inlines = [KeywordInline]
  template_name = 'articles/article_edit.html'
  extra_context = {'heading':'get_heading'}
  extra = 1
  max_num = 1
  def get_heading(self): return self.object.name
  def get_success_url(self):
    return self.request.session.get('article_list_view', reverse('available'))
  def forms_valid(self, form, inlines):
    results = super(UpdateArticle, self).forms_valid(form, inlines)
    extra = self.request.POST.get('extra','')
    if extra=='Save': return results
    if extra=='submit': self.object.submit(self.request)
    if extra=='approve': self.object.approve(self.request.user)
    if extra=='reject': self.object.reject(self.request.user)
    return HttpResponse("AOK.")
  def get_form(self, data=None, files=None, **kwargs):
    if self.object.writer: 
      self.inlines = []
      return WriteArticleForm(data=data, files=files, **kwargs)
    else:
      return UpdateArticleForm(data=data, files=files, **kwargs)
  def get_template_names(self):
    if self.object.writer: return ['articles/article_write.html']
    else: return ['articles/article_edit.html']

class ShowTag(ArticleListBase):
  pass

class AjaxNewKeyword(slick.LoginRequiredMixin, FormView):
    template_name = "articles/keyword_inline_form.html"
    form_class = QuantityForm

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
        
    def form_valid(self, id_form):
        f=KeywordInlineFormSet(Article, self.request, Keyword.objects.all()[0])
        fs=f.get_formset()
        form=fs()._construct_form(id_form.cleaned_data['num'])
        return self.render_to_response(self.get_context_data(form=form))
