from django.views.generic import ListView
from extra_views import SearchableListMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from articles.models import Article
from articles.forms import ArticleForm
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
import django_filters
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
#    def get_fields_with_filters(self):
#        fields = []
#        for ff in self.filter_fields:
#            if isinstance(ff, basestring):
#                fields.append((ff, 'icontains', ))
#            else:
#                if self.check_lookups and ff[1] not in VALID_STRING_LOOKUPS:
#                    raise ValueError(u'Invalid string lookup - %s' % ff[1])
#                fields.append(ff)
#        return fields
    def get_queryset(self):
        qs=super(FilterableListView, self).get_queryset()
#        search_pairs = self.get_fields_with_filters()
        for arg, val in self.request.GET.items():
            print "arg: " + str(arg) 
            print "val: " + str(val) 
            print "arg in self.get_filter_names(): " + str(arg in self.get_filter_names()) 
            print "self.get_filter_names(): " + str(self.get_filter_names()) 
            if arg in self.get_filter_names(): qs=qs.filter(Q(**{arg: val}))
        return qs
    def get_field_from_class(self, cls, fieldname):
        for field in cls._meta.local_fields:
            if field.attname==fieldname: return field
#    def get_filter_context(self):
#        for f in self.filter_fields:
#            print "f.__dict__: " + str(f.__dict__) 
#            for c in f.choices:
#                print "c.__dict__: " + str(c.__dict__)
#        return self.filter_fields
    def get_filter_names(self):
        return [f.name for f in self.filter_fields]
    def get_context_data(self, **kwargs):
        context = super(FilterableListView, self).get_context_data(**kwargs)
        context['q']=self.request.GET.get('q','')
        context['filters']=self.filter_fields
        return context
    
            
class SearchableListView(SearchableListMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super(SearchableListView, self).get_context_data(**kwargs)
        context['q']=self.request.GET.get('q','')
        return context
        
class ArticleList(FilterableListView):
    model = Article
#    queryset = Article.objects.filter(submitted=None)
    context_object_name = 'available'
    search_fields = ['tags',        'project__name',    'icontains', 'keyword__keyword']
    filter_fields = [Filter(title='Project', name='project__name', ref='project_id', model=Article),
                    Filter(title='Length', name='minimum', model=Article),
#                    Filter(title='Type', name='article_type', model=Article),
#                    Filter(name='published', lookup='isnull', model=Article),
#                    Filter(name='submitted', lookup='isnull', model=Article)
                ]
#    def get_queryset(self):
#        qs=super(SearchableListView, self).get_queryset()
#        self.filter = ArticleFilter(self.request.GET, queryset=qs)
#        return self.filter.qs
#    def get_context_data(self, **kwargs):
#        context = super(ArticleList, self).get_context_data(**kwargs)      
#        context['filter']=self.filter
#        print "self.filter: " + str(self.filter) 
#        print "self.filter.filters: " + str(self.filter.filters) 
#        for k,v in self.filter.filters.items():
#            print "k: " + str(k) 
#            print "v: " + str(v) 
#            print "v.__dict__: " + str(v.__dict__) 
#            print "Filter Title: " + str(k) 
##            for o in v.extra['queryset']:
##                print "Option: " + str(o) 
#            
#        print "self.filter.ordering_field: " + str(self.filter.ordering_field) 
#        print "self.filter.form: " + str(self.filter.form) 
        
#        return context

        
#class ArticleUpdate(LoginRequiredMixin, UpdateView):
#    model = Article
#    form_class = ArticleForm
#    success_url = "/articles/"
#    queryset = Article.objects.filter(submitted=None)
#    def form_valid(self, form):
#        form.instance.submitted = datetime.now()
#        return super(ArticleUpdate, self).form_valid(form)

class ArticleCreate(CreateView):
    model = Article

class ArticleUpdate(UpdateView):
    model = Article

class ArticleDelete(DeleteView):
    model = Article
    success_url = reverse_lazy('article_list')
