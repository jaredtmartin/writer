from django.views.generic import ListView
from extra_views import SearchableListMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView, FormView
from articles.models import Article, Keyword, Project
from articles.forms import ArticleForm, KeywordInlineFormSet, KeywordInlineForm
from django_actions.views import ActionViewMixin
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from extra_views import CreateWithInlinesView, UpdateWithInlinesView
import django_filters
from actions import *
VALID_STRING_LOOKUPS = ('exact','isnull','iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith', 'search', 'regex', 'iregex')
class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

#class ArticleFilter(django_filters.FilterSet):
#    class Meta:
#        model = Article
#        fields = ['project','minimum','article_type']
        
#    published
#    approved
#    submitted
#    assigned
#    rejected
#    released
class ChoiceContext(object):
    def __init__(self, display, qs, selected=False):
        self.display=display
        self.qs=qs
        self.selected=selected
class Filter(object):
    def __init__(self, name, model, **kwargs):
        self.name=name
        self.model=model
        self.title=kwargs.get('title', name.title())
        self.lookup=kwargs.get('lookup', 'icontains')
        self.ref=kwargs.get('ref', name)
        self.choices=self.get_choices()
    @property
    def query(self):
        return "%s__%s" % (self.name, self.lookup)
    def get_choices(self):
        choices=[]
        for choice in self.model.objects.all().distinct().order_by(self.name).values_list(self.name, flat=True):
            choices.append(ChoiceContext(display=unicode(choice), qs="&%s=%s" % (self.query, choice)))
        return choices
        
class FilterableListView(SearchableListMixin, ListView):
    def get_queryset(self):
        qs=super(FilterableListView, self).get_queryset()
        for arg, val in self.request.GET.items():
            if arg in self.get_filter_names(): qs=qs.filter(Q(**{arg: val}))
        return qs
    def get_field_from_class(self, cls, fieldname):
        for field in cls._meta.local_fields:
            if field.attname==fieldname: return field
    def get_filter_names(self):
        return [f.name for f in self.filter_fields]
    def get_context_data(self, **kwargs):
        context = super(FilterableListView, self).get_context_data(**kwargs)
        context['q']=self.request.GET.get('q','')
        context['filters']=self.filter_fields
        return context

class FilterableActionListView(ActionViewMixin, FilterableListView):
    pass

            
class SearchableListView(SearchableListMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super(SearchableListView, self).get_context_data(**kwargs)
        context['q']=self.request.GET.get('q','')
        return context
        
class ArticleList(ActionViewMixin, FilterableListView):
    model = Article
    actions = [publish_articles, claim_articles, submit_articles, release_articles]
#    queryset = Article.objects.filter(submitted=None)
    context_object_name = 'available'
    search_fields = ['tags', 'project__name', 'keyword__keyword']
    filter_fields = [Filter(title='Project', name='project__name', ref='project_id', model=Article),
                    Filter(title='Length', name='minimum', model=Article),
#                    Filter(title='Type', name='article_type', model=Article),
#                    Filter(name='published', lookup='isnull', model=Article),
#                    Filter(name='submitted', lookup='isnull', model=Article)
                ]
class ProjectCreate(CreateView):
    model = Project
    def get(self, request, *args, **kwargs):
        print "I am here!!!!"
        return super(ProjectCreate, self).get(request, *args, **kwargs)

class ArticleCreate(CreateView):
    model = Article

class ArticleUpdate(UpdateWithInlinesView):
    model = Article
    inlines = [KeywordInlineFormSet]

class ArticleDelete(DeleteView):
    model = Article
    success_url = reverse_lazy('article_list')

class AjaxKeywordInlineForm(FormView):
    template_name = "articles/keyword_inline_form.html"
    form_class = KeywordInlineForm

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form))
        
    def form_valid(self, id_form):
        f=KeywordInlineFormSet(Article, self.request, Keyword.objects.all()[0])
        fs=f.get_formset()
        form=fs()._construct_form(id_form.cleaned_data['num'])
        return self.render_to_response(self.get_context_data(form=form))
