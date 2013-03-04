from django.views.generic import ListView
from extra_views import SearchableListMixin
# from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin#, ModelFormMixin
from django.views.generic.detail import DetailView# , SingleObjectMixin
from django.views.generic import FormView #, TemplateView, 
from articles.models import Article, Keyword, Project, ArticleAction, ACTIONS, Relationship
from django.views.generic.base import View, TemplateResponseMixin
from articles.forms import RejectForm, ArticleForm, KeywordInlineFormSet, KeywordInlineForm, ConfirmRelationshipForm, \
TagArticleForm, ActionUserID, AssignToForm, UserForm, UserProfileForm, NoteForm, TagForm, RelationshipForm, ProjectForm, \
ACT_SUBMIT, ACT_REJECT, ACT_APPROVE, ACT_ASSIGN, ACT_CLAIM, ACT_RELEASE, ACT_PUBLISH, ACT_COMMENT

#from django_actions.views import ActionViewMixin
import pickle
# from datetime import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from extra_views import UpdateWithInlinesView #, CreateWithInlinesView, 
# import django_filters
# from actions import *
# from django import template

VALID_STRING_LOOKUPS = ('exact','isnull','iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith', 'search', 'regex', 'iregex')
class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class Choice(object):
    def __init__(self, **kwargs):
        self.label = kwargs.pop('label')
        self.base = kwargs.pop('base')
        self.value = kwargs.pop('value', self.label)
        self.lookup = kwargs.pop('lookup', 'icontains')
    def filter(self, qs):
        print "%s__%s % (self.base, self.lookup): " + str("%s__%s" % (self.base, self.lookup)) 
        print "self.value: " + str(self.value) 
        return qs.filter(**{"%s__%s" % (self.base, self.lookup):self.value}) 
        
class Filter(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name')
        self.display_name=kwargs.pop('display_name', self.name)
        self.lookup=kwargs.pop('lookup', 'icontains')
        self.choices=kwargs.pop('choices',self.build_choices())
    def filter(self, qs, selection):
        return self.choices[selection].filter(qs)
    def get_choice_key(self, choice):
    	    return unicode(choice)
    def build_choice(self, choice):
    	    return Choice(label=unicode(choice), base=self.name)
    def build_choices(self):
        choices={}
        for choice in self.get_choice_list():
            choices[self.get_choice_key(choice)] = self.build_choice(choice)
        return choices
        
class FilterWithChoicesFromModel(Filter):
    def __init__(self, **kwargs):
        self.model=kwargs.pop('model')
        super(FilterWithChoicesFromModel, self).__init__(**kwargs)
    def get_choice_list(self):
    	    return self.model.objects.all().distinct().order_by(self.name).values_list(self.name, flat=True)

class RelatedFilter(FilterWithChoicesFromModel):
    def __init__(self, **kwargs):
        self.display_attr = kwargs.pop('display_attr','')
        super(RelatedFilter, self).__init__(**kwargs)
    def build_choice(self, choice):
    	    return Choice(label=unicode(choice), base=self.name, lookup=self.display_attr)
    def get_choice_list(self):
        attr="%s__%s" % (self.name,self.display_attr)
        return self.model.objects.all().distinct().order_by(attr).values_list(attr, flat=True)
    def filter(self, qs, selection):
        try: return self.choices[selection].filter(qs)
        except KeyError: return qs.none()
    def build_choices(self):
        choices = super(RelatedFilter, self).build_choices()
        if 'None' in choices.keys(): choices['None'].lookup = 'isnull'
        return choices

class StatusFilter(RelatedFilter):
    def __init__(self, **kwargs):
        self.codes={}
        for code, name in ACTIONS: self.codes[code]=name
        super(StatusFilter, self).__init__(**kwargs)
        self.display_name="Status"

    def build_choice(self, choice):
        if not choice: return Choice(label=unicode('New'), base=self.name, lookup=self.display_attr, value=choice)
        return Choice(label=unicode(self.codes[choice]), base=self.name, lookup=self.display_attr, value=choice)

class FilterableListView(SearchableListMixin, ListView):
    def get_queryset(self):
        qs=super(FilterableListView, self).get_queryset()
        for arg, val in self.request.GET.items():
            if arg in self.filter_fields.keys(): 
                qs=self.filter_fields[arg].filter(qs, val)
#            if arg in self.get_filter_names(): qs=qs.filter(Q(**{arg: val}))
        return qs
    def get_field_from_class(self, cls, fieldname):
        for field in cls._meta.local_fields:
            if field.attname==fieldname: return field
#    def get_filter_names(self):
#        return [f.name for f in self.filter_fields]
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
class FormWithUserMixin(object):
    def get_form_kwargs(self):
        # Passes user to the form
        kwargs = super(FormWithUserMixin, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
class PostActionsView(TemplateResponseMixin, View):
    template_name = "articles/ajax_article_list_row.html"
    model = Article
    action_property_name=None
    action_verb=None
    action_form_class = None
    pks=[]
    def get_action_property_name(self):
        return self.action_property_name or self.action_verb+'ed'
    def filter_action_queryset(qs):
        return qs
    def get_action_form_class(self):
        return self.action_form_class
    def get_requested_objects(self):
        if not self.pks:
            if 'select-across' in self.request.POST and self.request.POST['select-across'] == u'0':
                # Building a empty queryset to load pickled data
                qs = self.model.objects.all()#[:1]
                qs.query = pickle.loads(self.request.session['serialized_qs'])
            else:
                # select a specific set of items
                qs = self.model.objects.filter(pk__in=(self.request.POST.getlist('action-select')))
            self.pks = list(qs.values_list('id', flat=True))
        else: qs=Article.all_objects.filter(pk__in=self.pks)
        return qs

    def get_action_queryset(self):
        try:
            if self.action_qs: return self.action_qs
        except AttributeError: pass
        qs=self.get_requested_objects()
        self.initial_action_qty=len(qs)
        if self.initial_action_qty:
            qs=self.filter_action_queryset(qs)
            # self.pks = list(qs.values_list('id', flat=True))
            self.final_action_qty=qs.count()
            return qs
        else:
            self.final_action_qty=0
            return []

    def create_action(self):
        raise NotImplemented
    def update_articles(self, qs, action):
        # qs= self.model_class.objects.filter(pk__in=list(qs)) # This converts the queryset so objects will not 'slip out'
        qs.update(**{'last_action':action})
        try:qs.update(**{self.get_action_property_name():action})
        except AttributeError:pass
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
        else: messages.info(self.request, 'All (%s) of the articles have been %s sucessfully' % (self.final_action_qty, self.get_past_tense_action_verb()))
    def post(self, request, *args, **kwargs):
        self.action_qs = self.get_action_queryset()
        # Make sure the articles are available
        form_class=self.get_action_form_class()
        if self.action_qs and self.final_action_qty > 0:
            if form_class: self.action_form=form_class(self.request.POST)
            else: self.action_form=None
            if (not self.action_form) or self.action_form.is_valid():
                # qs=list(self.action_qs)  # Save it as a list so we don't lose track of the ones we change due to the filters
                self.action=self.create_action()
                if self.action:
                    self.update_articles(self.action_qs, self.action)
                    self.action_qs=self.get_requested_objects()
        elif form_class: self.action_form=form_class()
        self.send_result_messages()
        context = self.get_context_data()
        print "context = %s" % str(context)
        return self.render_to_response(context)
    def get_context_data(self, **kwargs):
        kwargs.update({'as_row':True,'object_list':self.action_qs})
        return kwargs
    
class FilterableActionListView(GetActionsMixin, FilterableListView):
    pass
            
class SearchableListView(SearchableListMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super(SearchableListView, self).get_context_data(**kwargs)
        context['q']=self.request.GET.get('q','')
        return context

class ArticleList(GetActionsMixin, FilterableListView):
    model = Article
#     actions = [
#         claim_articles,
#         assign_articles,
#         release_articles,
#         submit_articles,
# #        tag_articles,
#         approve_articles,
#         reject_articles,
#         publish_articles,
#         reject_and_release_articles,
#     ]
#    queryset = Article.objects.filter(submitted=None)
    # context_object_name = 'available'
    search_fields = ['_tags', 'project__name', 'keyword__keyword']
    filter_fields={
        'minimum':FilterWithChoicesFromModel(name='minimum', model=Article),
        'project':RelatedFilter(name='project', model=Article, display_attr='name'),
        'last_action':StatusFilter(name='last_action', model=Article, display_attr='code'),
    }
    def get_actions(self):
        return [
            ('Assign', ActionUserID(),'/articles/various/assign/'),
            ('Tag', TagForm(),'/articles/various/tag/'),
            ('Approve','','/articles/various/approve/'),
            ('Reject',NoteForm(),'/articles/various/reject/'),
        ]
    def get_context_data(self, **kwargs):
        kwargs['selected_tab']='articles'
        return super(ArticleList, self).get_context_data(**kwargs)

class AjaxDeleteRowView(DeleteView):
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.info(self.request, 'The '+ self.object._meta.verbose_name+' has been created successfully.')
        return self.render_to_response(self.get_context_data())

class AjaxRowTemplateResponseMixin(object):
    template_name = 'articles/ajax_row.html'
    def get_context_data(self, **kwargs):
        kwargs['row_template']=self.get_row_template()
        kwargs['row_id']=self.get_row_id()
        kwargs['object']=self.object
        return super(AjaxRowTemplateResponseMixin, self).get_context_data(**kwargs)
    def get_row_id(self): return self.row_id
    def get_row_template(self): return self.row_template
    def get_success_message(self): return "The %s has been updated successfully." % (self.object._meta.verbose_name,)
    def get_failure_message(self): return "We were unable to update the %s." % (self.object._meta.verbose_name,)
    def form_valid(self, form):
        self.object = form.save()
        print "self.object: " + str(self.object) 
        messages.info(self.request, self.get_success_message())
        return self.render_to_response(self.get_context_data(form=form))
    def form_invalid(self, form):
        messages.error(self.request, self.get_failure_message())
        return super(AjaxRowTemplateResponseMixin, self).form_invalid(form)
    
class AjaxUpdateMixin(object):
    def form_valid(self, form):
        self.object = form.save()
        messages.info(self.request, 'The '+ self.object._meta.verbose_name+' has been updated successfully.')
        return self.render_to_response(self.get_context_data(form=form))

class ProjectCreate(FormWithUserMixin, AjaxUpdateMixin, CreateView):
    # Takes name, owner, and article_id
    # Creates Project with given name and owner and assignes it to article
    # Returns message and article project field with new item selected
    model = Project
    form_class = ProjectForm

    # def form_valid(self, form):
    #     self.object = form.save()
    #     messages.info(self.request, 'The '+ self.object._meta.verbose_name+' has been created successfully.')
    #     return self.render_to_response(self.get_context_data(form=form))
    # def get_context_data(self, **kwargs):
    #     return super(ProjectCreate, self).get_context_data(**kwargs)
    # def post(self, request, *args, **kwargs):
    #     return super(ProjectCreate, self).post(request, *args, **kwargs)
    def form_invalid(self, form):
        messages.error(self.request, 'Unable to create project with the name given.')
        messages.error(self.request, form.errors)
        return super(ProjectCreate, self).form_invalid(form)

class ProjectList(FilterableListView):
    model = Project
    search_fields = ['name']
    filter_fields={
        'owner':RelatedFilter(name='owner', model=Project, display_attr='username'),
    }
    def get_context_data(self, **kwargs):
        kwargs['selected_tab']='projects'
        return super(ProjectList, self).get_context_data(**kwargs)

class ArticleCreate(FormWithUserMixin, LoginRequiredMixin, CreateView):
    template_name = 'articles/article_edit.html'
    model = Article
    context_object_name = 'article'
    def get_context_data(self, **kwargs):
        kwargs['article']=self.object
        return super(ArticleCreate, self).get_context_data(**kwargs)

class ArticleUpdate(FormWithUserMixin, LoginRequiredMixin, UpdateWithInlinesView):
    template_name = 'articles/article_edit.html'
    model = Article
    form_class=ArticleForm
    inlines = [KeywordInlineFormSet]

# class ArticleDelete(LoginRequiredMixin, DeleteView):
#     model = Article
#     success_url = reverse_lazy('article_list')

class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('list_projects')

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
        
# class ArticleClaim(ArticleActionView):
#     def do_action(self):
#         if self.object.assigned:
#             messages.error(self.request, 'This article has already been assigned or claimed.')
#         elif self.request.user == self.object.owner:
#             messages.error(self.request, 'A requester cannot claim his or her own article. Try assigning it to a writer.')
#         else:
#             self.object.claim(self.request.user)
#             messages.info(self.request, 'The article has been claimed successfully.')
            
# class ArticleSubmit(ArticleActionView):
#     def do_action(self):
#         if self.request.user == self.object.assigned.author or self.request.user.is_staff:
#             self.object.submit(self.request.user)

# class ArticleRelease(ArticleActionView):
#     def do_action(self):
#         if not self.object.assigned:
#             messages.error(self.request, 'This article has not been assigned.')
#         elif self.request.user == self.object.owner or self.request.user.is_staff or self.request.user==self.object.assigned.author:
#             self.object.release(self.request.user)
#             messages.info(self.request, 'The article has been released successfully.')
#         else:
#             messages.error(self.request, 'You must be the owner or author to release this article.')
        
# class ArticleApprove(ArticleActionView):
#     def do_action(self):
#         if not self.object.submitted:
#             messages.error(self.request, 'This article has not been submitted.')
#         elif self.request.user == self.object.owner or self.request.user.is_staff:
#             self.object.approve(self.request.user)
#             messages.info(self.request, 'The article has been submitted successfully.')
#         else:
#             messages.error(self.request, 'You do not have permission to approve this article.')
# class ArticleDelete(ArticleActionView):
#     def do_action(self):
#         if self.request.user == self.object.owner or self.request.user.is_staff:
#             self.old_object_id = self.object.pk
#             self.object.delete()
#             messages.info(self.request, 'The article has been submitted successfully.')
#         else:
#             messages.error(self.request, 'You do not have permission to delete this article.')
#     def get_context_data(self, **kwargs):
#         self.object=Article(pk=self.old_object_id)
#         kwargs.update({'deleted':True})
#         return super(ArticleDelete, self).get_context_data(**kwargs)

class ArticleActionFormView(ArticleActionView, FormMixin):
    form_invalid_msg = ""
    def form_valid(self, form):
        self.form = form
        self.do_action()
        context = self.get_context_data(object=self.object)
        print "context = %s" % str(context)
        return self.render_to_response(context)
    def form_invalid(self, form):
        messages.info(self.request, self.form_invalid_msg)
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

# class AssignArticle(ArticleActionFormView):
#     form_class = AssignToForm
#     form_invalid_msg = 'The specified user was not found.'
#     def do_action(self):
#         self.object.assign(author=self.form.cleaned_data['assign_to_user'], user=self.request.user)
#         messages.info(self.request, 'The article has been assigned successfully.')

class TagArticle(ArticleActionFormView):
    form_class = TagArticleForm
    form_invalid_msg = 'The specified tag was invalid.'
    def do_action(self):
        self.object.tags = self.form.cleaned_data['_tags']
        self.object.save()
        messages.info(self.request, 'The article has been tagged successfully.')

# class RejectArticle(ArticleActionFormView):
#     form_class = RejectForm
#     form_invalid_msg = 'The reason specified was invalid.'
#     def do_action(self):
#         self.object.reject(comment=self.form.cleaned_data['reason'], user=self.request.user)
#         messages.info(self.request, 'The article has been rejected and the reason has been noted.')
# class AssignArticle(SingleObjectMixin, FormView):
#     model=Article
#     template_name = "articles/ajax_article_list_row.html"
#     form_class = AssignToForm
#     def get_context_data(self, **kwargs):
#         kwargs['object']=self.object
#         if 'as_row' in self.request.POST: 
#             kwargs.update({'as_row':True, 'as_form':False,'object_list':[self.object]})
#         elif 'as_form' in self.request.POST: 
#             kwargs.update({'as_row':False, 'as_form':True, 'form':ArticleForm(instance=self.object.get_profile()),'object_list':[self.object]})
#         return super(AssignArticle, self).get_context_data(**kwargs)
#     def get_template_names(self):
#         return [self.template_name]
#     def form_invalid(self, form):
#         messages.info(self.request, 'The specified user was not found.')
#     def form_valid(self, form):
#         self.object = self.get_object()
#         self.object.assign(author=form.cleaned_data['assign_to_user'], user=self.request.user)
#         messages.info(self.request, 'The article has been assigned successfully.')
#         # return self.render_to_response(self.get_context_data(form=form))
#         context = self.get_context_data(form=form) 
#         print "context:%s" % context
#         print "self.get_template_names():%s" % self.get_template_names()
#         return self.render_to_response(context)

# class TagArticle(UpdateView):
#     model=Article
#     template_name = "articles/article_tags_td.html"  # Old Template: "articles/ajax_article_tags_row.html"
#     form_class = TagArticleForm
#     def get_context_data(self, **kwargs):
#         kwargs['object']=self.object
#         if 'as_row' in self.request.POST: 
#             kwargs.update({'as_row':True, 'as_form':False,'object_list':[self.object]})
#         elif 'as_form' in self.request.POST: 
#             kwargs.update({'as_row':False, 'as_form':True, 'form':ArticleForm(instance=self.object.get_profile()),'object_list':[self.object]})
#         return super(TagArticle, self).get_context_data(**kwargs)
#     def get_template_names(self):
#         return [self.template_name]
#     def form_valid(self, form):
#         self.object = form.save()
#         messages.info(self.request, 'The article has been tagged successfully.')
#         return self.render_to_response(self.get_context_data(form=form))

class AssignArticles(PostActionsView):
    def filter_action_queryset(self, qs):
        # Make sure user has permission to assign articles
        print "qs = %s" % str(qs)
        qs=qs.filter(assigned__isnull=True)
        if not self.request.user.is_staff: return qs.filter(owner=self.request.user)
        else: return qs
    action_verb="assign"
    action_form_class = ActionUserID
    def create_action(self):
        action = ArticleAction.objects.create(user=self.request.user, 
                    code=ACT_ASSIGN, 
                    author=self.action_form.cleaned_data['user'],
                )
        return action
    def update_articles(self, qs, action):
        super(AssignArticles, self).update_articles(qs, action)
        qs.update(assigned=action)

class RejectArticles(PostActionsView):
    action_verb="reject"
    action_form_class = NoteForm
    def filter_action_queryset(self, qs):
        # Make sure user has permission to reject articles
        qs=qs.filter(submitted__isnull=False)
        if not self.request.user.is_staff: return qs.filter(owner=self.request.user)
        else: return qs
    def create_action(self):
        return ArticleAction.objects.create(
            user=self.request.user, 
            code=ACT_REJECT, 
            comment=self.action_form.cleaned_data['note'],
        )
    def update_articles(self, qs, action):
        super(RejectArticles, self).update_articles(qs, action)
        qs.update(submitted=None)
        qs.update(approved=None)
        qs.update(assigned=None)

class ApproveArticles(PostActionsView):
    action_verb="approve"
    action_property_name="approved"
    def filter_action_queryset(self, qs):
        # Make sure user has permission to Approve the articles
        qs=qs.filter(submitted__isnull=False)
        if not self.request.user.is_staff: return qs.filter(owner=self.request.user)
        else: return qs
    def create_action(self):
        return ArticleAction.objects.create(
            user=self.request.user, 
            code=ACT_APPROVE, 
        )

class SubmitArticles(PostActionsView):
    action_verb="submit"
    action_property_name="submitted"
    def filter_action_queryset(self, qs):
        # Make sure user has permission to submit the articles
        qs=qs.filter(submitted__isnull=True)
        if not self.request.user.is_staff: return qs.filter(last_action__author=self.request.user)
        else: return qs
    def create_action(self):
        return ArticleAction.objects.create(
            user=self.request.user, 
            author=self.request.user, 
            code=ACT_SUBMIT, 
        )

class DeleteArticles(PostActionsView):
    action_verb="delete"
    action_property_name="deleted"
    def filter_action_queryset(self, qs):
        # Make sure user has permission to submit the articles
        # qs=qs.filter(submitted__isnull=True)
        if not self.request.user.is_staff: return qs.filter(owner=self.request.user)
        else: return qs
    def create_action(self):
        print "rinngin action"
        return True
    def update_articles(self, qs, action):
        print "self.action_qs = %s" % str(self.action_qs)
        l=list(qs.values_list('id', flat=True))

        self.action_qs=Article.all_objects.filter(pk__in=l)
        print "qs = %s" % str(qs)
        print "self.action_qs = %s" % str(self.action_qs)
        super(DeleteArticles, self).update_articles(qs, action)
        print "qs = %s" % str(qs)
        print "self.action_qs = %s" % str(self.action_qs)
        

class ReleaseArticles(PostActionsView):
    action_verb="release"
    action_property_name="released"
    def filter_action_queryset(self, qs):
        # Make sure user has permission to release the articles
        qs=qs.filter(assigned__isnull=False)
        if not self.request.user.is_staff: return qs.filter(owner=self.request.user)
        else: return qs
    def create_action(self):
        return ArticleAction.objects.create(
            user=self.request.user, 
            code=ACT_RELEASE, 
        )
    def update_articles(self, qs, action):
        super(ReleaseArticles, self).update_articles(qs, action)
        qs.update(assigned=None)

class ClaimArticles(PostActionsView):
    action_verb="claim"
    action_property_name="assigned"
    def filter_action_queryset(self, qs):
        return qs.filter(assigned__isnull=True)
    def create_action(self):
        return ArticleAction.objects.create(
            user=self.request.user, 
            author=self.request.user, 
            code=ACT_CLAIM, 
        )
        
class TagArticles(PostActionsView):
    action_verb="tag"
    action_form_class = TagForm
    def filter_action_queryset(self, qs):
        # Make sure user has permission to tag articles
        if not self.request.user.is_staff: return qs.filter(owner=self.request.user)
        else: return qs
    def create_action(self):
        # if self.request.POST['append'] == 'true': tags=self.object._tags+self.action_form.cleaned_data['tags']
        # else: tags=self.action_form.cleaned_data['tags']
        return self.action_form.cleaned_data['tags']
    def update_articles(self, qs, action):
        for article in qs:
            if self.request.POST['append']=='True': tags=article.tags
            else: tags=[]
            tags.append(action)
            article.tags = tags
            article.save()
        # else:
        #     qs.update(_tags=action)
            #.add(*[x.pk for x in action]) # action actual is a list of tags, this will add them all at once.
    def get_past_tense_action_verb(self): return 'tagged'

class UserUpdateView(UpdateView):
    model=User
    form_class = UserForm
    def get_context_data(self, **kwargs):
        kwargs.update({
            'user_profile_form':UserProfileForm(instance=self.object.get_profile()),
        })
        return super(UserUpdateView, self).get_context_data(**kwargs)
    def form_valid(self, form):
        user_profile_form = UserProfileForm(self.request.POST, instance=self.object.get_profile())
        if user_profile_form.is_valid():
            user_profile_form.save()
            self.request.session['tz'] = user_profile_form.cleaned_data['timezone']
            messages.info(self.request, 'The changes to your profile have been made successfully.')
            return super(UserUpdateView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, user_profile_form=user_profile_form))

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

class AddRelationship(AjaxRowTemplateResponseMixin, CreateView):
    model=Relationship
    form_class = RelationshipForm
    row_template="articles/relationship_list_row.html"
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        return super(AddRelationship, self).form_valid(form)
    def get_context_data(self, **kwargs):
        user=self.get_user_to_display()
        user.relationship=self.object
        c= super(AddRelationship, self).get_context_data(**kwargs)
        c['object']=user
        c['user_group'] = self.user_group
        return c
    
class AddRequester(AddRelationship):
    row_id='requester'
    user_group = "Requesters"
    def get_user_to_display(self):
        return self.object.requester
    
class AddWriter(AddRelationship):
    row_id='writer'
    user_group = "Writers"
    def get_user_to_display(self):
        return self.object.writer

class UserList(SearchableListView):
    model=User
    search_fields = ['username','first_name','last_name']
    template_name = "articles/user_list.html"
    def get_context_data(self, **kwargs):
        if 'q' in self.request.GET and self.request.GET['q']: 
            kwargs['title'] = "%s called '%s'" % (self.user_group, self.request.GET['q'] )
        else:
            kwargs['title'] = 'Available %s' % self.user_group
        kwargs['user_group'] = self.user_group
        return super(UserList, self).get_context_data(**kwargs)
    
class WriterList(UserList):
    def get_queryset(self):
        return User.objects.filter(Q(userprofile__preferred_mode=3)|Q(userprofile__preferred_mode=1)).exclude(requester_relationships__requester=self.request.user).exclude(pk=self.request.user.pk)
    user_group='Writers'
    
class RequesterList(UserList):
    def get_queryset(self):
        return User.objects.filter(userprofile__preferred_mode__gte=2).exclude(requester_relationships__requester=self.request.user).exclude(pk=self.request.user.pk)
    user_group='Requesters'

class DeleteRelationship(AjaxDeleteRowView):
    model=Relationship
    
class ConfirmRelationship(AjaxRowTemplateResponseMixin, UpdateView):
    model=Relationship
    row_template="articles/relationship_list_row.html"
    form_class = ConfirmRelationshipForm
    def get_row_id(self): 
        if self.object.requester == self.request.user: return "writer"
        else: return "requester"
    def get_user_to_display(self):
        return self.object.writer
        if self.object.requester == self.request.user: return self.object.writer
        else: return self.object.requester
    def get_context_data(self, **kwargs):
        user=self.get_user_to_display()
        user.relationship=Relationship.objects.get(pk=self.object.pk)
        user.is_confirmed= user.relationship.confirmed
        user.is_confirmable = not user.relationship.confirmed and not self.request.user == user.relationship.created_by
        c=super(ConfirmRelationship, self).get_context_data(**kwargs)
        c['object']=user
        return c
    def post(self, request, *args, **kwargs):
        # Make sure we can only confirm if we are the reciever of the invitation.
        self.object = self.get_object()
        if not (self.request.user in [self.object.requester, self.object.writer]) or self.object.created_by == self.request.user:
            messages.error(self.request, 'You are not the recipient of this invitation.')
            return self.form_invalid(self.get_form(self.get_form_class()))
        return super(ConfirmRelationship, self).post(request, *args, **kwargs)
