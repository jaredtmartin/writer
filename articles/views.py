from django.views.generic import ListView
from extra_views import SearchableListMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView, FormView
from articles.models import Article, Keyword, Project, ArticleAction
from django.views.generic.base import View, TemplateResponseMixin
from articles.forms import ArticleForm, KeywordInlineFormSet, KeywordInlineForm, ActionUserID, AssignToForm
#from django_actions.views import ActionViewMixin
import pickle
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
class GetActionsMixin(object):
    def get_context_data(self, *args, **kwargs):
        object_list_displayed = kwargs['object_list']
        kwargs['all_items_count'] = object_list_displayed.count()
        # Storing serialized queryset using query attribute
        self.request.session['serialized_qs'] = pickle.dumps(object_list_displayed.query)
        self.request.session['serialized_model_qs'] = object_list_displayed.model
        context = super(GetActionsMixin, self).get_context_data(**kwargs)
        context['actions']=self.get_actions()
        return context
    def get_actions(self):
        return self.actions
        
class PostActionsView(TemplateResponseMixin, View):
    def filter_action_queryset(qs):
        return qs
    def get_action_form_class(self):
        return self.action_form_class
    def get_requested_objects(self):
        if 'select-across' in self.request.POST:
            model_class = self.request.session['serialized_model_qs']
            if self.request.POST['select-across'] == u'0':
                # select a specific set of items
                qs = model_class.objects.filter(pk__in=(self.request.POST.getlist('action-select')))
            else:
                # Building a empty queryset to load pickled data
                qs = model_class.objects.all()[:1]
                qs.query = pickle.loads(self.request.session['serialized_qs'])
            return qs
        else: return []
    def get_action_queryset(self):
        try:
            if self.action_qs: return self.action_qs
        except AttributeError: pass
        qs=self.get_requested_objects()
        self.initial_action_qty=qs.count()
        if self.initial_action_qty:
            print "qs A: " + str(qs) 
            qs=self.filter_action_queryset(qs)
            print "qs D: " + str(qs) 
            self.final_action_qty=qs.count()
            return qs
        else:
            self.final_action_qty=0
            return []

    def create_action(self):
        raise NotImplemented
    def update_articles(self, qs, action):
        action.articles.add(*qs)
        qs.update(last_action=action)
    def get_action_verb(self):
        return self.action_verb
    def get_past_tense_action_verb(self):
        return self.get_action_verb()+'ed'
    def send_result_messages(self):
        if self.final_action_qty==0:
            messages.error(self.request, 'The articles selected are not ready to be %s or are not yours to %s.' % (self.get_past_tense_action_verb(), self.get_action_verb()))
        elif self.action_form and not self.action_form.is_valid():
            messages.error(self.request, 'You did not select a valid value to complete this action.')
        elif self.final_action_qty < self.initial_action_qty:
            messages.warning(self.request, 'Only %i of the articles selected have been %s. Please verify the operation and that you have authority to make this change on the remaining articles.' % (self.final_action_qty, self.get_past_tense_action_verb()))
        else: messages.info(self.request, 'All %s of the articles have been %s sucessfully' % (self.final_action_qty, self.get_past_tense_action_verb()))
    def post(self, request, *args, **kwargs):
        self.action_qs = self.get_action_queryset()
        # Make sure the articles are available
        form_class=self.get_action_form_class()
        if self.action_qs and self.final_action_qty > 0:
            if form_class: self.action_form=form_class(self.request.POST)
            else: self.action_form=None
            if (not self.action_form) or self.action_form.is_valid():
                qs=list(self.action_qs)  # Save it as a list so we don't lose track of the ones we change due to the filters
                print "self.action_qs: " + str(self.action_qs) 
                self.action=self.create_action()
                print "self.action_qs: " + str(self.action_qs) 
                self.update_articles(self.action_qs, self.action)
                print "self.action_qs: " + str(self.action_qs) 
                print "self.action_qs: " + str(self.action_qs) 
                self.action_qs=self.get_requested_objects()
                print "self.action_qs: " + str(self.action_qs) 
        else: self.action_form=form_class()
        self.send_result_messages()
        context = self.get_context_data()
        return self.render_to_response(context)
    def get_context_data(self, **kwargs):
        context = {'object_list': self.action_qs}
        context.update(kwargs)
        return context
    
class FilterableActionListView(GetActionsMixin, FilterableListView):
    pass
            
class SearchableListView(SearchableListMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super(SearchableListView, self).get_context_data(**kwargs)
        context['q']=self.request.GET.get('q','')
        return context
        
class ArticleList(GetActionsMixin, FilterableListView):
    model = Article
    actions = [
        claim_articles,
        assign_articles,
        release_articles,
        submit_articles,
#        tag_articles,
        approve_articles,
        reject_articles,
        publish_articles,
        reject_and_release_articles,
    ]
#    queryset = Article.objects.filter(submitted=None)
    context_object_name = 'available'
    search_fields = ['tags', 'project__name', 'keyword__keyword']
    filter_fields = [Filter(title='Project', name='project__name', ref='project_id', model=Article),
                     Filter(title='Length', name='minimum', model=Article),
#                    Filter(title='Type', name='article_type', model=Article),
#                    Filter(name='published', lookup='isnull', model=Article),
#                    Filter(name='submitted', lookup='isnull', model=Article)
                ]
#    def get_action_user_id_form(self):
#        form=ActionUserID()
##        form.fields["user"].queryset = User.objects.filter(user__factory)
#        return form
    def get_actions(self):
        return [
            ('Assign', ActionUserID(),'/articles/various/assign/'),
            ('Tag', TagForm(),'/articles/various/tag/'),
            ('Approve','','/articles/various/approve/'),
            ('Reject',NoteForm(),'/articles/various/reject/'),
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
    form_class=ArticleForm
    inlines = [KeywordInlineFormSet]

class ArticleDelete(DeleteView):
    model = Article
    success_url = reverse_lazy('article_list')

class AjaxKeywordInlineForm(FormView):
    template_name = "articles/keyword_inline_form.html"
    form_class = KeywordInlineForm

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
        
    def form_valid(self, id_form):
        f=KeywordInlineFormSet(Article, self.request, Keyword.objects.all()[0])
        fs=f.get_formset()
        form=fs()._construct_form(id_form.cleaned_data['num'])
        return self.render_to_response(self.get_context_data(form=form))

class ArticleActionView(DetailView):
    template_name = "articles/article_list_row.html"
    model = Article
    def do_action(self): raise NotImplemented
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.do_action()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
        
class ArticleSubmit(ArticleActionView):
    def do_action(self):
        if self.request.user == self.object.assigned.author or self.request.user.is_staff:
            self.object.submit(self.request.user)

class ArticleRelease(ArticleActionView):
    def do_action(self):
        if not self.object.assigned:
            messages.error(self.request, 'This article has not been assigned.')
        elif self.request.user == self.object.owner or self.request.user.is_staff or self.request.user==self.object.assigned.author:
            self.object.release(self.request.user)
            messages.info(self.request, 'The article has been released successfully.')
        else:
            messages.error(self.request, 'You must be the owner or author to release this article.')
        
class ArticleApprove(ArticleActionView):
    def do_action(self):
        if not self.object.submitted:
            messages.error(self.request, 'This article has not been submitted.')
        elif self.request.user == self.object.owner or self.request.user.is_staff:
            self.object.approve(self.request.user)
            messages.info(self.request, 'The article has been submitted successfully.')
        else:
            messages.error(self.request, 'You do not have permission to approve this article.')

class AssignVariousArticles(PostActionsView):
    def filter_action_queryset(self, qs):
        # Make sure user has permission to assign articles
        qs=qs.filter(assigned__isnull=True)
        if not self.request.user.is_staff: return qs.filter(owner=self.request.user)
        else: return qs
    template_name = "articles/ajax_article_list_row.html"
    model = Article
    action_verb="assign"
    action_form_class = ActionUserID
    def create_action(self):
        action = ArticleAction.objects.create(user=self.request.user, 
                    code=ACT_ASSIGN, 
                    author=self.action_form.cleaned_data['user'],
                )
        return action
    def update_articles(self, qs, action):
        super(AssignVariousArticles, self).update_articles(qs, action)
        qs.update(assigned=action)

class RejectVariousArticles(PostActionsView):
    def filter_action_queryset(self, qs):
        # Make sure user has permission to assign articles
        qs=qs.filter(submitted__isnull=False)
        if not self.request.user.is_staff: return qs.filter(owner=self.request.user)
        else: return qs
    template_name = "articles/ajax_article_list_row.html"
    model = Article
    action_verb="reject"
    action_form_class = NoteForm
    def create_action(self):
        action = ArticleAction.objects.create(user=self.request.user, 
                    code=ACT_REJECT, 
                    comment=self.action_form.cleaned_data['note'],
                )
        return action
    def update_articles(self, qs, action):
        super(RejectVariousArticles, self).update_articles(qs, action)
        qs.update(rejected=action)
        qs.update(submitted=None)
        qs.update(approved=None)

class ApproveVariousArticles(PostActionsView):
    def filter_action_queryset(self, qs):
        # Make sure user has permission to assign articles
        qs=qs.filter(submitted__isnull=False)
        if not self.request.user.is_staff: return qs.filter(owner=self.request.user)
        else: return qs
    template_name = "articles/ajax_article_list_row.html"
    model = Article
    action_verb="approve"
    action_form_class = None
    def create_action(self):
        action = ArticleAction.objects.create(user=self.request.user, 
                    code=ACT_APPROVE, 
                )
        return action
    def update_articles(self, qs, action):
        super(ApproveVariousArticles, self).update_articles(qs, action)
        qs.update(approved=action)
        
class TagVariousArticles(PostActionsView):
    def filter_action_queryset(self, qs):
        # Make sure user has permission to tag articles
        if not self.request.user.is_staff: return qs.filter(owner=self.request.user)
        else: return qs
    template_name = "articles/ajax_article_list_row.html"
    model = Article
    action_verb="tag"
    action_form_class = TagForm
    def create_action(self):
        return self.action_form.cleaned_data['tags']
    def update_articles(self, qs, action):
        for article in qs:
            article.tags.add(*[x.pk for x in action]) # action actual is an array of tags, this will add them all at once.
    def get_past_tense_action_verb(self):
        return 'tagged'
