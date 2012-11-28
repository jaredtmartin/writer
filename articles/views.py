from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from articles.models import Article
from articles.forms import ArticleForm
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
        
class ArticleList(ListView):
    model = Article
    queryset = Article.objects.filter(_submitted=False)
    context_object_name = 'available'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ArticleList, self).get_context_data(**kwargs)      
        # Add in a QuerySet of all assigned articles
#        context['assigned'] = Article.objects.filter(_assigned=self.request.user, _submitted=False)
        return context
        
class ArticleUpdate(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    success_url = "/articles/"
    queryset = Article.objects.filter(_submitted=False)
    def form_valid(self, form):
        form.instance.submitted = datetime.now()
        return super(ArticleUpdate, self).form_valid(form)

