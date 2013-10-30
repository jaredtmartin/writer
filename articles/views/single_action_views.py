from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from articles.forms import TagArticleForm
from articles.models import Article
import slick.views as slick

class ArticleActionView(slick.LoginRequiredMixin, DetailView):
    template_name = "articles/ajax_article_list_row.html"
    model = Article
    def do_action(self): raise NotImplemented
    def get_context_data(self, **kwargs):
        if 'as_row' in self.request.POST: 
            kwargs.update({'as_row':True, 'as_form':False,'object_list':[self.object]})
        elif 'as_form' in self.request.POST: 
            kwargs.update({'as_row':False, 'as_form':True, 'form':ArticleForm(instance=self.object.get_profile()),'object_list':[self.object]})
        return super(ArticleActionView, self).get_context_data(**kwargs)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.do_action()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

class PublishArticle(ArticleActionView):
    def do_action(self):
        from django.utils.datastructures import MultiValueDictKeyError
        try: outlet = PublishingOutlet.objects.get(pk=self.request.POST['outlet_id'])
        except MultiValueDictKeyError: messages.error(self.request, 'Publishing outlet not specified.')
        except PublishingOutlet.DoesNotExist: messages.error(self.request, 'Unable to find specified publishing outlet.')
        else: 
            print "outlet = %s" % str(outlet)
            try: config = PublishingOutletConfiguration(outlet=outlet, user=self.request.user)
            except PublishingOutletConfiguration.DoesNotExist: messages.error(self.request, 'Unable to find configuration for specified publishing outlet.')
            else: 
                # pd=config.pickled_data
                # data = pickle.loads(str(config.pickled_data))
                print "config = %s" % str(config)
                print "config.pickled_data = %s" % str(config.pickled_data)
                # outlet.do_action(config.data, self.object)
                # messages.success(self.request, 'Article published successfully.')

class ArticleActionFormView(ArticleActionView, FormMixin):
    form_invalid_msg = ""
    def form_valid(self, form):
        self.form = form
        self.do_action()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
    def form_invalid(self, form):
        messages.error(self.request, self.form_invalid_msg)
        return self.render_to_response(self.get_context_data(form=form))
    def post(self, request, *args, **kwargs):
        # This is an exact copy of BaseFormView's post method, but due to multiple inheritance, 
        # I have to put it here
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class TagArticle(ArticleActionFormView):
    form_class = TagArticleForm
    form_invalid_msg = 'The specified tag was invalid.'
    def do_action(self):
        self.object.tags = self.form.cleaned_data['_tags']
        self.object.save()
        messages.success(self.request, 'The article has been tagged successfully.')
