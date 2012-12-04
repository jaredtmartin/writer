from django.views.generic import ListView
from extra_views import SearchableListMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from articles.models import Article
from articles.forms import ArticleForm
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
import django_filters

class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = ['project']
            
class SearchableListView(SearchableListMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super(SearchableListView, self).get_context_data(**kwargs)
        context['q']=self.request.GET.get('q','')
        return context
        
class ArticleList(SearchableListView):
    model = Article
    queryset = Article.objects.filter(submitted=None)
    context_object_name = 'available'
    search_fields = ['tags', 'project__name','keyword__keyword']
    filter_fields = ['article_type__name','minimum']
    def get_queryset(self):
        qs=super(SearchableListView, self).get_queryset()
        self.filter = ArticleFilter(self.request.GET, queryset=qs)
        return self.filter.qs
    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)      
        context['filter']=self.filter
        return context

        
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
