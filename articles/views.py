from django.views.generic import ListView
from extra_views import SearchableListMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin#, ModelFormMixin
from django.views.generic.detail import DetailView, BaseDetailView# , SingleObjectMixin
from django.views.generic import FormView #, TemplateView, 
from articles.models import Article, Keyword, Project, ArticleAction, ACTIONS, Contact, \
PublishingOutlet, PublishingOutletConfiguration, WRITER_POSITION, REVIEWER_POSITION
from django.views.generic.base import View, TemplateResponseMixin
from articles.forms import RejectForm, ArticleForm, KeywordInlineFormSet, QuantityForm, \
TagArticleForm, ActionUserID, AssignToForm, UserForm, UserProfileForm, NoteForm,\
TagForm, ProjectForm, ACT_SUBMIT, ACT_REJECT, ACT_APPROVE, \
ACT_ASSIGN_WRITER, ACT_ASSIGN_REVIEWER, ACT_CLAIM_REVIEWER, ACT_RELEASE, ACT_PUBLISH, ACT_COMMENT, \
ACT_REMOVE_REVIEWER, ACT_REMOVE_WRITER, ACT_CLAIM_WRITER, UserModeForm, PublishForm, \
STATUS_NEW, STATUS_RELEASED, STATUS_ASSIGNED, STATUS_SUBMITTED, STATUS_APPROVED, \
STATUS_PUBLISHED, WriteArticleForm, WRITER_MODE, REVIEWER_MODE, REQUESTER_MODE, AvailabilityForm, CreateArticleForm
#from django_actions.views import ActionViewMixin
from django.http import Http404, HttpResponseServerError
from django.template import loader, Context
import sys
import pickle
# from datetime import datetime
from django.db.models import Q, F
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from extra_views import UpdateWithInlinesView, CreateWithInlinesView 
import django_filters
# from actions import *
# from django import template
from django.conf import settings

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
        # context['actions']=self.get_actions() 
        return context
    # def get_actions(self):
    #     return self.actions
class FormWithUserMixin(object):
    def get_form_kwargs(self):
        # Passes user to the form
        kwargs = super(FormWithUserMixin, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

# class FilterableActionListView(GetActionsMixin, FilterableListView):

            
class SearchableListView(SearchableListMixin, ListView):
    # adds context "q" for searching and mixes in search
    def get_context_data(self, **kwargs):
        context = super(SearchableListView, self).get_context_data(**kwargs)
        context['q']=self.request.GET.get('q','')
        return context

# class ArticleList(GetActionsMixin, FilterableListView):
class SidebarContextMixin(object):
    def filter_approved(self, qs, user):
        return qs.filter(status=STATUS_APPROVED)
    def filter_assigned(self, qs, user):
        if user.mode==WRITER_MODE:
            return qs.filter(writer=user, was_claimed=False, status=STATUS_ASSIGNED)
        elif user.mode==REQUESTER_MODE:
            return qs.filter(writer__isnull=False, was_claimed=False, status=STATUS_ASSIGNED)
    def filter_available(self, qs, user):
        if user.mode==WRITER_MODE:
            return qs.filter(writer=None).filter(Q(writer_availability="")|Q(writer_availability__in=self.request.user.writing_contacts))
        elif user.mode==REQUESTER_MODE:
            return qs.filter(writer=None).exclude(writer_availability="Nobody")
        elif user.mode==REVIEWER_MODE:
            return qs.filter(reviewer=None,submitted__isnull=False).filter(Q(reviewer_availability="")|Q(reviewer_availability__in=self.request.user.reviewing_contacts))
    def filter_claimed(self, qs, user):
        if user.mode==WRITER_MODE:
            return qs.filter(writer=user, was_claimed=True, status=STATUS_ASSIGNED)
        elif user.mode==REQUESTER_MODE:
            return qs.filter(was_claimed=True, status=STATUS_ASSIGNED)
    def filter_rejected(self, qs, user):
        return qs.filter(rejected__isnull=False)
    def filter_published(self, qs, user):
        return qs.filter(status=STATUS_PUBLISHED)
    def filter_submitted(self, qs, user):
        if user.mode==WRITER_MODE:
            return qs.filter(writer=user, status=STATUS_SUBMITTED,submitted__isnull=False, approved__isnull=True)
        elif user.mode==REQUESTER_MODE:
            return qs.filter(status=STATUS_SUBMITTED,submitted__isnull=False, approved__isnull=True)
    def filter_unavailable(self, qs, user):
        return qs.filter(writer_availability="Nobody", status__in=[STATUS_NEW, STATUS_RELEASED])
    def get_filters(self, user):
        if user.mode==WRITER_MODE:
            return {
                'Available':self.filter_available,
                'Assigned':self.filter_assigned,
                'Claimed':self.filter_claimed,
                'Submitted':self.filter_submitted,
                'Approved':self.filter_approved,
                'Rejected':self.filter_rejected,
                'order':['Available','Assigned','Claimed','Submitted','Approved','Rejected']
            }
        elif user.mode==REQUESTER_MODE:
            return {
                'Unavailable':self.filter_unavailable,
                'Available':self.filter_available,
                'Assigned':self.filter_assigned,
                'Claimed':self.filter_claimed,
                'Submitted':self.filter_submitted,
                'Approved':self.filter_approved,
                'Rejected':self.filter_rejected,
                'Published':self.filter_published,
                'order':['Unavailable','Available','Assigned','Claimed','Submitted','Approved','Rejected','Published']
            }
        elif user.mode==REVIEWER_MODE:
            return {
                'Available':self.filter_available,
                'Approved':self.filter_approved,
                'Rejected':self.filter_rejected,
                'order':['Available','Approved','Rejected']
            }
    def get_sidebar_context(self):
        filters = self.get_filters(self.request.user)
        return [[f,reverse_lazy(f.lower()),filters[f](Article.objects.all(), self.request.user).count()] for f in filters['order']]

    def get_context_data(self, **kwargs):
        kwargs['view_filters']=self.get_sidebar_context()
        return super(SidebarContextMixin, self).get_context_data(**kwargs)
class AvailablilityMixin(object):
    # Adds in code to put together dropdowns for assigning articles and making articles available
    def get_available_list(self, group):
        return list(set([c.name for c in group]))
    def get_assignee_list(self, group):
        return list(set([contact.worker for contact in group]))
    def get_context_data(self, **kwargs):
        # print "self.request.user.writer_contacts = %s" % str(self.request.user.writer_contacts)
        try:
            kwargs['writer_availability_list']  = self.get_available_list(self.request.user.writer_contacts)
            kwargs['reviewer_availability_list']= self.get_available_list(self.request.user.reviewer_contacts)
            kwargs['writer_assignment_list']    = self.get_assignee_list(self.request.user.writer_contacts)
            kwargs['reviewer_assignment_list']  = self.get_assignee_list(self.request.user.reviewer_contacts)
        except AttributeError: pass
        # print "kwargs = %s" % str(kwargs)
        context = super(AvailablilityMixin, self).get_context_data(**kwargs)
        return context    


class ArticleList(AvailablilityMixin, SidebarContextMixin, GetActionsMixin, SearchableListView):
    model = Article
    search_fields = ['tags', 'project__name', 'keyword__keyword']
    hidden_columns = ['Reviewer','Status','Category','Length','Priority','Tags']
    name = "All"
    reverse_url=None
    
    def get_view_header(self):
        return self.current_filter.title()+ " Articles"
    def get_hidden_columns(self):
        return self.hidden_columns
    def get_reverse_url(self):
        if self.reverse_url: return self.reverse_url
        else: return self.name.lower()
    def get_context_data(self, **kwargs):
        # kwargs['view_filters']=self.get_sidebar_context()
        kwargs['current_filter'] = self.current_filter
        kwargs['selected_tab']=self.name
        kwargs['hidden_columns']=self.get_hidden_columns()
        kwargs['all_columns']=['Project','Keywords','Writer','Reviewer','Status','Category','Length','Priority','Tags']
        kwargs['header']=self.get_view_header()
        context = super(ArticleList, self).get_context_data(**kwargs)
        return context
    def get(self, request, *args, **kwargs):
        try: self.request.user.mode
        except: self.request.user.mode = None
        response = super(ArticleList, self).get(request, *args, **kwargs)
        try:
            user_profile=self.request.user.get_profile()
            user_profile.article_list_view = self.get_reverse_url()
            user_profile.save()
        except AttributeError:pass
        return response
    def get_queryset(self):
        self.current_filter = self.request.GET.get('view', 'Available')
        if not self.current_filter in self.get_filters(self.request.user).keys(): self.current_filter = 'Available'
        view_filter = self.get_filters(self.request.user).get(self.current_filter,None)
        qs=super(ArticleList, self).get_queryset()
        if view_filter: qs=view_filter(qs, self.request.user)
        return qs
    #     # if 'last_action' in self.request.GET:
    #     #     qs=qs.filter(last_action__code=self.request.GET['last_action'])
    #     if 'status' in self.request.GET:
    #         qs=qs.filter(status=self.request.GET['status'])
    #     return qs
# class AvailablilityView(ArticleList):
#     # Adds in code to put together dropdowns for assigning articles and making articles available
#     def get_available_list(self, group):
#         return list(set([c.name for c in group]))
#     def get_assignee_list(self, group):
#         return list(set([contact.worker for contact in group]))
#     def get_context_data(self, **kwargs):
#         # print "self.request.user.writer_contacts = %s" % str(self.request.user.writer_contacts)
#         try:
#             kwargs['writer_availability_list']  = self.get_available_list(self.request.user.writer_contacts)
#             kwargs['reviewer_availability_list']= self.get_available_list(self.request.user.reviewer_contacts)
#             kwargs['writer_assignment_list']    = self.get_assignee_list(self.request.user.writer_contacts)
#             kwargs['reviewer_assignment_list']  = self.get_assignee_list(self.request.user.reviewer_contacts)
#         except AttributeError: pass
#         # print "kwargs = %s" % str(kwargs)
#         context = super(AvailablilityView, self).get_context_data(**kwargs)
#         return context

# class MyArticles(ArticleList):
#     name = "My"
#     reverse_url = 'my_articles'
#     def get_queryset(self):
#         qs=super(MyArticles, self).get_queryset()
#         qs=qs.filter(writer=self.request.user).exclude(status=STATUS_SUBMITTED)
#         return qs
# class Approved(ArticleList):
#     name = "Approved"
#     def get_context_data(self, **kwargs):
#         kwargs['publishing_outlet_configs']=self.request.user.publishing_outlets
#         print "kwargs = %s" % str(kwargs)
#         context = super(Approved, self).get_context_data(**kwargs)
#         print "context = %s" % str(context)
#         return context
#     def get_queryset(self):
#         qs=super(Approved, self).get_queryset()
#         qs=qs.filter(status=STATUS_APPROVED)
#         return qs
# class Assigned(AvailablilityView):
#     name = "Assigned"
#     def get_queryset(self):
#         qs=super(Assigned, self).get_queryset()
#         user=self.request.user
#         if user.mode==WRITER_MODE:
#             qs=qs.filter(writer=user, was_claimed=False, status=STATUS_ASSIGNED)
#         elif user.mode==REQUESTER_MODE:
#             qs=qs.filter(writer__isnull=False, was_claimed=False, status=STATUS_ASSIGNED)
#         return qs
# class Available(AvailablilityView):
#     name = "Available"
#     def get_queryset(self):
#         qs=super(Available, self).get_queryset()
#         user=self.request.user
#         if user.mode==WRITER_MODE:
#             qs=qs.filter(writer=None).filter(Q(writer_availability="")|Q(writer_availability__in=self.request.user.writing_contacts))
#         elif user.mode==REQUESTER_MODE:
#             qs=qs.filter(writer=None).exclude(writer_availability="Nobody")
#         elif user.mode==REVIEWER_MODE:
#             qs=qs.filter(reviewer=None,submitted__isnull=False).filter(Q(reviewer_availability="")|Q(reviewer_availability__in=self.request.user.reviewing_contacts))
#         # This is for available from requesters viewpoint


#         # This is for available to writer
#         # 
#         return qs
# class Claimed(AvailablilityView):
#     name = "Claimed"
#     def get_queryset(self):
#         qs=super(Claimed, self).get_queryset()
#         user=self.request.user
#         if user.mode==WRITER_MODE:
#             qs=qs.filter(writer=user, was_claimed=True, status=STATUS_ASSIGNED)
#         elif user.mode==REQUESTER_MODE:
#             qs=qs.filter(was_claimed=True, status=STATUS_ASSIGNED)
#         return qs
# class Rejected(ArticleList):
#     name = "Rejected"
#     def get_queryset(self):
#         qs=super(Rejected, self).get_queryset()
#         qs=qs.filter(rejected__isnull=False)
#         return qs
# class Published(ArticleList):
#     name = "Published"
#     def get_queryset(self):
#         qs=super(Published, self).get_queryset()
#         qs=qs.filter(status=STATUS_PUBLISHED)
#         return qs
# class Submitted(AvailablilityView):
#     name = "Submitted"

#     def get_queryset(self):
#         qs=super(Submitted, self).get_queryset()
#         user=self.request.user
#         if user.mode==WRITER_MODE:
#             qs=qs.filter(writer=user, status=STATUS_SUBMITTED,submitted__isnull=False, approved__isnull=True)
#         elif user.mode==REQUESTER_MODE:
#             qs=qs.filter(status=STATUS_SUBMITTED,submitted__isnull=False, approved__isnull=True)
#         return qs

# class Unavailable(AvailablilityView):
#     name = "Unavailable"
#     def get_queryset(self):
#         qs=super(Unavailable, self).get_queryset()
#         qs=qs.filter(writer_availability="Nobody", status__in=[STATUS_NEW, STATUS_RELEASED])
#         return qs

class AjaxDeleteRowView(DeleteView):
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'The '+ self.object._meta.verbose_name+' has been created successfully.')
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
        messages.success(self.request, self.get_success_message())
        return self.render_to_response(self.get_context_data(form=form))
    def form_invalid(self, form):
        messages.error(self.request, self.get_failure_message())
        return super(AjaxRowTemplateResponseMixin, self).form_invalid(form)
    
class AjaxUpdateMixin(object):
    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'The '+ self.object._meta.verbose_name+' has been updated successfully.')
        return self.render_to_response(self.get_context_data(form=form))

class ProjectCreate(FormWithUserMixin, AjaxUpdateMixin, CreateView):
    # Takes name, owner, and article_id
    # Creates Project with given name and owner and assignes it to article
    # Returns message and article project field with new item selected
    model = Project
    form_class = ProjectForm
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

class ArticleCreate(FormWithUserMixin, LoginRequiredMixin, CreateWithInlinesView):
    template_name = 'articles/article_edit.html'
    model = Article
    form_class=CreateArticleForm
    context_object_name = 'article'
    inlines = [KeywordInlineFormSet]
    success_url = reverse_lazy('article_list')
    def get_context_data(self, **kwargs):
        kwargs['article']=self.object
        context = super(ArticleCreate, self).get_context_data(**kwargs)
        return context
    def forms_valid(self, form, inlines):
        # print "form.cleaned_data = %s" % str(form.cleaned_data)
        response = super(ArticleCreate, self).forms_valid(form, inlines)
        # If number_of_articles was specified, clone the model that many times
        if 'number_of_articles' in form.cleaned_data and form.cleaned_data['number_of_articles']:
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
        try:
            user=self.request.user
            user_profile=self.request.user.get_profile()
            return reverse_lazy(user_profile.article_list_view)
        except: return super(ArticleCreate, self).get_success_url()
        

class ArticleUpdate(FormWithUserMixin, LoginRequiredMixin, UpdateWithInlinesView):
    template_name = 'articles/article_edit.html'
    model = Article
    form_class = ArticleForm
    extra = 1
    max_num = 1
    inlines = [KeywordInlineFormSet]
    success_url = reverse_lazy('article_list')
    def get_success_url(self):
        print "get_success_url"
        try:
            user=self.request.user
            print "user = %s" % str(user)
            user_profile=self.request.user.get_profile()
            print "user_profile = %s" % str(user_profile)
            url= reverse_lazy(user_profile.article_list_view)
            print "url = %s" % str(url)
        except: 
            print "hit error"
            url= super(ArticleUpdate, self).get_success_url()
        return url
    def get_form_class(self):
        if self.request.user == self.object.owner and self.request.user.in_requester_mode: 
            print "making an articleForm"
            return ArticleForm
        else: 
            self.inlines = []
            print "making a WriteArticleForm"
            return WriteArticleForm
    def forms_valid(self, form, inlines):
        results = super(ArticleUpdate, self).forms_valid(form, inlines)
        if 'saveandsubmit' in self.request.POST: self.object.submit(self.request)
        print "'saveandapprove' in self.request.POST = %s" % str('saveandapprove' in self.request.POST)
        if 'saveandapprove' in self.request.POST: 
            print "approving"
            self.object.approve(self.request.user)
        return results
    def get_context_data(self, **kwargs):
        kwargs['article']=self.object
        context = super(ArticleUpdate, self).get_context_data(**kwargs)
        return context

# class ArticleDelete(LoginRequiredMixin, DeleteView):
#     model = Article
#     success_url = reverse_lazy('article_list')

class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('list_projects')

# class AjaxKeywordInlineForm(FormView):
#     template_name = "articles/keyword_inline_form.html"
#     form_class = KeywordInlineForm

#     def form_invalid(self, form):
#         return self.render_to_response(self.get_context_data(form=form))
        
#     def form_valid(self, id_form):
#         f=KeywordInlineFormSet(Article, self.request, Keyword.objects.all()[0])
#         fs=f.get_formset()
#         form=fs()._construct_form(id_form.cleaned_data['num'])
#         return self.render_to_response(self.get_context_data(form=form))
            
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

################################################################################
#                               Actions                                        #
################################################################################
class ArticleActionsView(TemplateResponseMixin, View):
    template_name = "articles/ajax_article_list_row.html"
    model = Article
    next_status = None
    action_property_name=None
    past_tense_action_verb=None
    action_verb=None
    action_form_class = None
    pks=[]
    def filter_by_owner(self, qs, user):
        if not user.is_authenticated(): return qs.none()
        if not self.request.user.is_staff: return qs.filter(owner_id=user.pk)
        else: return qs
    def filter_by_writer(self, qs, user):
        if not user.is_authenticated(): return qs.none()
        return qs.filter(writer_id=self.request.user.pk)
    def filter_by_owner_or_writer(self, qs, user):
        if not user.is_authenticated(): return qs.none()
        if not self.request.user.is_staff: return qs.filter(Q(owner_id=self.request.user.pk)|Q(writer_id=self.request.user.pk))
        else: return qs
    def filter_by_owner_or_reviewer(self, qs, user):
        if not user.is_authenticated(): return qs.none()
        if not self.request.user.is_staff: return qs.filter(Q(owner_id=self.request.user.pk)|Q(reviewer_id=self.request.user.pk))
        else: return qs
    def filter_by_writer(self, qs, user):
        if not user.is_authenticated(): return qs.none()
        if not self.request.user.is_staff: return qs.filter(writer_id=user.pk)
        else: return qs
    def filter_by_owner_or_writer_or_reviewer(self, qs, user):
        if not user.is_authenticated(): return qs.none()
        if not self.request.user.is_staff: return qs.filter(writer_id=user.pk)
        else: return qs
    def get_action_property_name(self):
        return self.action_property_name or self.action_verb+'ed'
    def filter_action_queryset(self, qs):
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
        qs = self.get_requested_objects()
        self.initial_action_qty = len(qs)
        if self.initial_action_qty:
            qs=self.filter_action_queryset(qs)
            self.final_qty = qs.count()
            return qs
        else:
            self.final_qty = 0
            return []

    def create_action(self):pass
    def update_status(self):
        if self.next_status: self.action_qs.update(status=self.next_status)
    def update_articles(self):
        self.update_status()
        if self.action:
            self.action_qs.update(**{'last_action':self.action})
            try:self.action_qs.update(**{self.get_action_property_name():self.action})
            except :pass
    def get_action_verb(self):
        return self.action_verb
    def get_past_tense_action_verb(self):
        if self.past_tense_action_verb: return self.past_tense_action_verb
        return str(self.get_action_verb())+'ed'
    def send_result_messages(self):
        if self.final_qty==0:
            messages.error(self.request, 'The articles selected are not ready to be %s or are not yours to %s.' % (self.get_past_tense_action_verb(), self.get_action_verb()))
        elif self.action_form and not self.action_form.is_valid():
            messages.error(self.request, 'You did not select a valid value to complete this action.')
        elif self.final_qty < self.initial_action_qty:
            messages.warning(self.request, 'Only %i of the articles selected have been %s. Please verify the operation and that you have authority to make this change on the remaining articles.' % (self.final_qty, self.get_past_tense_action_verb()))
        else: messages.success(self.request, 'All (%s) of the articles have been %s sucessfully' % (self.final_qty, self.get_past_tense_action_verb()))
    def post(self, request, *args, **kwargs):
        self.action_qs = self.get_action_queryset()
        form_class=self.get_action_form_class()
        if self.action_qs and self.final_qty > 0:
            if form_class: self.action_form=form_class(self.request.POST)
            else: self.action_form=None
            if (not self.action_form) or self.action_form.is_valid():
                self.action=self.create_action()
                self.update_articles()
                self.action_qs=self.get_requested_objects()
        elif form_class: self.action_form=form_class()
        self.send_result_messages()
        context = self.get_context_data()
        return self.render_to_response(context)
    def get_context_data(self, **kwargs):
        kwargs.update({'as_row':True,'object_list':self.action_qs})
        return kwargs

############################### Reject Actions ####################################

class RejectArticles(ArticleActionsView):
    action_verb="reject"
    action_form_class = RejectForm
    next_status = STATUS_RELEASED
    action_property_name = "XXX" # This is to disable automatic assigning of property. We'll do this ourself.
    def filter_action_queryset(self, qs):
        qs=qs.filter(submitted__isnull=False)
        return self.filter_by_owner_or_reviewer(qs, self.request.user)
    def create_action(self):
        self.authors = [User.objects.get(pk=w) for w in self.action_qs.values_list('writer', flat=True)]
        print "self.authors = %s" % str(self.authors)
        for author in self.authors:
            action = ArticleAction.objects.create(
                user=self.request.user, 
                code=ACT_REJECT, 
                comment=self.action_form.cleaned_data['reason'],
                author=author,
            )
            self.action_qs.filter(writer=author).update(rejected=action)
    def update_status(self):
        print "self.action_form.cleaned_data['return_to_writer'] = %s" % str(self.action_form.cleaned_data['return_to_writer'])
        if self.action_form.cleaned_data['return_to_writer']: self.next_status = STATUS_ASSIGNED
        else: self.next_status = STATUS_RELEASED
        super(RejectArticles, self).update_status()
    def update_articles(self):
        super(RejectArticles, self).update_articles()
        self.action_qs = Article.objects.filter(pk__in=list(self.action_qs.values_list('id', flat=True)))
        self.action_qs.update(submitted=None, approved=None)
        # print "qs[0].writer = %s" % str(qs[0].writer)
        print "self.action_form.cleaned_data['return_to_writer'] = %s" % str(self.action_form.cleaned_data['return_to_writer'])
        if not self.action_form.cleaned_data['return_to_writer']: 
            self.action_qs.update(writer=None)
            self.action_qs.update(content="")
            self.action_qs.update(title="")

        # print "qs[0].writer = %s" % str(qs[0].writer)
############################### Approve Actions ####################################

class ApproveArticles(ArticleActionsView):
    action_verb="approve"
    action_property_name="approved"
    next_status = STATUS_APPROVED
    def filter_action_queryset(self, qs):
        qs=qs.filter(submitted__isnull=False)
        return self.filter_by_owner_or_reviewer(qs, self.request.user)
    def create_action(self):
        return ArticleAction.objects.create(
            user=self.request.user, 
            code=ACT_APPROVE
        )
############################### Publish Articles ####################################
class MarkArticlesAsPublished(ArticleActionsView):
    next_status = STATUS_PUBLISHED
    def filter_action_queryset(self, qs):
        qs=qs.filter(approved__isnull=False)
        return self.filter_by_owner(qs, self.request.user)

class PublishArticles(MarkArticlesAsPublished):
    action_form_class = PublishForm
    next_status = STATUS_PUBLISHED
    def create_action(self):
        outlet = self.action_form.cleaned_data['outlet']
        outlet.do_action(self.action_qs)
        
############################### Submit Actions ####################################

class SubmitArticles(ArticleActionsView):
    action_verb="submit"
    action_property_name="submitted"
    next_status = STATUS_SUBMITTED
    def filter_action_queryset(self, qs):
        qs=qs.filter(submitted__isnull=True)
        print "qs = %s" % str(qs)
        qs=Article.filter_valid(qs, self.request)
        print "qs = %s" % str(qs)
        return self.filter_by_writer(qs, self.request.user)
    def create_action(self):
        return ArticleAction.objects.create(
            user=self.request.user, 
            author=self.request.user, 
            code=ACT_SUBMIT, 
        )
############################### Delete Actions ####################################

class DeleteArticles(ArticleActionsView):
    action_verb="delete"
    action_property_name="deleted"
    def filter_action_queryset(self, qs):
        # Make sure user has permission to submit the articles
        qs=qs.filter(submitted__isnull=True)
        qs = self.filter_by_owner(qs, self.request.user)
        return qs
    def create_action(self):
        return True
    def update_articles(self):
        l=list(qs.values_list('id', flat=True))
        self.action_qs=Article.all_objects.filter(pk__in=l)
        super(DeleteArticles, self).update_articles(qs, action)
        

# ## TO BE REMOVED ##
# class ReleaseArticles(ArticleActionsView):
#     action_verb="release"
#     past_tense_action_verb="released"
#     def create_action(self):
#         return ArticleAction.objects.create(
#             user=self.request.user, 
#             code=self.action_type, 
#         )
# ## TO BE REMOVED ##
# class ReleaseWriter(ReleaseArticles):
#     action_type=ACT_REMOVE_WRITER
#     next_status = STATUS_RELEASED
#     def filter_action_queryset(self, qs):
#         qs = qs.filter(writer__isnull=False, submitted__isnull=True)
#         return self.filter_by_owner_or_writer(qs, self.request.user)
#     def update_articles(self):
#         print "Redy to change status"
#         print "self.next_status = %s" % str(self.next_status)
#         if self.next_status: self.action_qs.update(status=self.next_status)
#         self.action_qs.update(writer=None)

# ## TO BE REMOVED ##
# class ReleaseReviewer(ReleaseArticles):
#     action_type=ACT_REMOVE_REVIEWER 
#     def filter_action_queryset(self, qs):
#         qs = qs.filter(reviewer__isnull=False, approved__isnull=True)
#         return self.filter_by_owner_or_reviewer(qs, self.request.user)
#     def update_articles(self):
#         self.action_qs.update(reviewer=None)

## TO BE REMOVED ##
# class InitialRelease(ReleaseArticles):
#     action_type=ACT_RELEASE
#     next_status = STATUS_RELEASED
#     action_property_name="released"
#     def filter_action_queryset(self, qs):
#         qs = qs.filter(released=False)
#         return self.filter_by_owner(qs, self.request.user)
#     def update_articles(self):
#         if self.next_status: self.action_qs.update(status=self.next_status)
#         self.action_qs.update(released=True)


############################### Claim Actions ##################################
class Claim(ArticleActionsView):
    action_verb="claim"

class ClaimAsWriter(Claim):
    next_status = STATUS_ASSIGNED
    def update_articles(self):
        super(ClaimAsWriter, self).update_articles()
        self.action_qs.update(writer=self.request.user, was_claimed=True)
    def filter_action_queryset(self, qs):
        return qs.filter(Q(writer_availability__in=self.request.user.writing_contacts)|Q(writer_availability=""))

class ClaimAsReviewer(Claim):
    def update_articles(self):
        super(ClaimAsReviewer, self).update_articles()
        self.action_qs.update(reviewer=self.request.user, was_claimed=True)
    def filter_action_queryset(self, qs):
        return qs.filter(Q(reviewer_availability__in=self.request.user.reviewing_contacts)|Q(reviewer_availability=""))

############################### Release Actions ##################################
class Release(ArticleActionsView):
    action_verb="release"
    past_tense_action_verb="released"
    next_status = STATUS_RELEASED
class ReleaseAsWriter(Release):
    def filter_action_queryset(self, qs):
        qs = qs.filter(writer__isnull=False, submitted__isnull=True)
        return self.filter_by_owner_or_writer(qs, self.request.user)
    def update_articles(self):
        super(ReleaseAsWriter, self).update_articles()
        self.action_qs.update(writer=None, was_claimed=False)
class ReleaseAsReviewer(Release):
    def filter_action_queryset(self, qs):
        qs = qs.filter(reviewer__isnull=False, submitted__isnull=True)
        return self.filter_by_owner_or_writer(qs, self.request.user)
    def update_articles(self):
        super(ReleaseAsReviewer, self).update_articles()
        self.action_qs.update(reviewer=None, was_claimed=False)
############################### Available Actions ##################################



class MakeAvailable(ArticleActionsView):
    action_verb="make available"
    past_tense_action_verb="made available"
    def filter_action_queryset(self, qs):
        return self.filter_by_owner(qs, self.request.user)

class MakeAvailableTo(MakeAvailable):
    action_form_class = AvailabilityForm

class MakeAvailableToAllWriters(MakeAvailable):
    next_status = STATUS_RELEASED
    def update_articles(self):
        super(MakeAvailableToAllWriters, self).update_articles()
        self.action_qs.update(writer_availability="")
        self.action_qs.update(writer=None, was_claimed=False)
class MakeAvailableToWriter(MakeAvailableTo):
    next_status = STATUS_RELEASED
    def update_articles(self):
        super(MakeAvailableToWriter, self).update_articles()
        self.action_qs.update(writer_availability=self.action_form.cleaned_data['name'])
        self.action_qs.update(writer=None, was_claimed=False)

class MakeAvailableToReviewer(MakeAvailableTo):
    def update_articles(self):
        super(MakeAvailableToReviewer, self).update_articles()
        self.action_qs.update(reviewer_availability=self.action_form.cleaned_data['name'])
        self.action_qs.update(reviewer=None, was_claimed=False)
class MakeAvailableToAllReviewers(MakeAvailable):
    def update_articles(self):
        super(MakeAvailableToAllReviewers, self).update_articles()
        self.action_qs.update(reviewer_availability="")
        self.action_qs.update(reviewer=None, was_claimed=False)
############################### Unavailable Actions ##################################
class MakeUnavailable(ArticleActionsView):
    action_verb="make unavailable"
    past_tense_action_verb="made unavailable"
    def filter_action_queryset(self, qs):
        return self.filter_by_owner(qs, self.request.user)
class MakeUnavailableToWriters(MakeUnavailable):
    next_status = STATUS_NEW
    def update_articles(self):
        super(MakeUnavailableToWriters, self).update_articles()
        self.action_qs.update(writer_availability="Nobody")
        self.action_qs.update(writer=None, was_claimed=False)
class MakeUnavailableToReviewers(MakeUnavailable):
    def update_articles(self):
        super(MakeUnavailableToReviewers, self).update_articles()
        self.action_qs.update(reviewer_availability="Nobody")
        self.action_qs.update(reviewer=None, was_claimed=False)
############################### Assign Actions ##################################
class Assign(ArticleActionsView):
    action_form_class = AssignToForm
    action_verb="assign"
    def filter_action_queryset(self, qs):
        return self.filter_by_owner(qs, self.request.user)
class AssignToWriter(Assign):
    next_status = STATUS_ASSIGNED
    def update_articles(self):
        super(AssignToWriter, self).update_articles()
        self.action_qs.update(writer=self.action_form.cleaned_data['user'], was_claimed=False)
class AssignToReviewer(Assign):
    def update_articles(self):
        super(AssignToReviewer, self).update_articles()
        self.action_qs.update(reviewer=self.action_form.cleaned_data['user'], was_claimed=False)



# ## TO BE REMOVED ##
# class ClaimArticles(ArticleActionsView):
#     action_verb="claim"
#     def create_action(self):
#         return ArticleAction.objects.create(
#             user=self.request.user, 
#             code=self.action_type, 
#             author=self.request.user,
#         )
#     def update_articles(self):
#         if self.next_status: self.action_qs.update(status=self.next_status)
#         self.action_qs.update(last_action=action)
# ## TO BE REMOVED ##
# class ClaimArticlesAsWriter(ClaimArticles):
#     action_property_name="writer"
#     action_type = ACT_CLAIM_WRITER
#     next_status = STATUS_ASSIGNED
#     def filter_action_queryset(self, qs):
#         return qs.filter(writer__isnull=True, released = True)
#     def update_articles(self):
#         super(ClaimArticlesAsWriter, self).update_articles(qs, action)
#         self.action_qs.update(writer=action.author)
# ## TO BE REMOVED ##
# class ClaimArticlesAsReviewer(ClaimArticles):
#     action_property_name="reviewer"
#     action_type = ACT_CLAIM_REVIEWER
#     def filter_action_queryset(self, qs):
#         return qs.filter(reviewer__isnull=True, released = True)
#     def update_articles(self):
#         super(ClaimArticlesAsReviewer, self).update_articles(qs, action)
#         self.action_qs.update(reviewer=action.author)
        
# ############################### Tag Actions ####################################
# class TagArticles(ArticleActionsView):
#     action_verb="tag"
#     action_form_class = TagForm
#     past_tense_action_verb = 'tagged'
#     def filter_action_queryset(self, qs):
#         # Make sure user has permission to tag articles
#         return self.filter_by_owner(qs, self.request.user)
#     def create_action(self):
#         return self.action_form.cleaned_data['tags']
#     def update_articles(self):
#         for article in qs:
#             if self.request.POST['append']=='True': tags=article.tags
#             else: tags=[]
#             tags.append(action)
#             article.tags = tags
#             article.save()
       


################################################################################
#                               User Profile                                   #
################################################################################
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
            messages.success(self.request, 'The changes to your profile have been made successfully.')
            return super(UserUpdateView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, user_profile_form=user_profile_form))

class ChangeModeView(FormView, ArticleList):
    form_class=UserModeForm
    def form_valid(self, form):
        p = self.request.user.get_profile()
        p.mode = form.cleaned_data['mode']
        p.save()
        # self.request.user.mode = form.cleaned_data['mode']
        messages.info(self.request, "You are now in %s mode." % self.request.user.mode_display)
        return HttpResponseRedirect(reverse_lazy('article_list'))
    def form_invalid(self, form): 
        return HttpResponseRedirect(reverse_lazy('article_list'))

class AjaxKeywordInlineForm(FormView):
    template_name = "articles/keyword_inline_form.html"
    form_class = QuantityForm

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
        
    def form_valid(self, id_form):
        f=KeywordInlineFormSet(Article, self.request, Keyword.objects.all()[0])
        fs=f.get_formset()
        form=fs()._construct_form(id_form.cleaned_data['num'])
        return self.render_to_response(self.get_context_data(form=form))

class UserList(SearchableListView):
    model=User
    search_fields = ['username','first_name','last_name']
    template_name = "articles/user_list.html"
    user_group = ''
    def get_context_data(self, **kwargs):
        kwargs['mine'] = None
        if 'status' in self.request.GET and self.request.GET['status']: 
            kwargs['status']=self.request.GET['status']
            if self.request.GET['status'] == 'other': kwargs['mine'] = self.get_mine()
        else: kwargs['status']='all'
        kwargs['user_group'] = self.user_group
        return super(UserList, self).get_context_data(**kwargs)
    def get_queryset(self): 
        self.user = self.request.user
        if 'status' in self.request.GET: 
            if self.request.GET['status'] == 'mine': qs = self.get_mine()
            if self.request.GET['status'] == 'requested': qs = self.get_requested()
            elif self.request.GET['status'] == 'unconfirmed': qs = self.get_unconfirmed()
            elif self.request.GET['status'] == 'other': qs = self.get_other()
        else: qs = self.get_all()
        if 'q' in self.request.GET and self.request.GET['q']:
            qs.filter(username__icontains=self.request.GET['q'])
        return qs

class WriterList(UserList):
    user_group='Writer'
    def get_all(self):
        return User.objects.filter(Q(contacts_as_worker__position=WRITER_POSITION, contacts_as_worker__confirmation=True)|Q(userprofile__mode=WRITER_MODE)).exclude(pk=self.user.pk).distinct()
    def get_mine(self):
        return User.objects.filter(contacts_as_worker__requester=self.user, contacts_as_worker__position=WRITER_POSITION, contacts_as_worker__confirmation = True).distinct()
    def get_unconfirmed(self):
        return User.objects.filter(contacts_as_worker__requester=self.user, contacts_as_worker__position=WRITER_POSITION, contacts_as_worker__confirmation = False, contacts_as_worker__created_by=self.user).distinct()
    def get_requested(self):
        return User.objects.filter(contacts_as_worker__requester=self.user, contacts_as_worker__confirmation = False).exclude(contacts_as_worker__created_by=self.user).distinct()
    def get_other(self):
        return User.objects.filter(Q(contacts_as_worker__worker__isnull=False).exclude(contacts_as_worker__requester=self.user)|Q(userprofile__mode=WRITER_MODE)).distinct()

class RequesterList(UserList):
    user_group='Requester'
    def get_all(self):
        return User.objects.filter(contacts_as_requester__requester__isnull=False).exclude(pk=self.user.pk).distinct()
    def get_mine(self):
        if self.request.user.mode == WRITER_MODE:
            return User.objects.filter(contacts_as_requester__worker=self.user, contacts_as_requester__confirmation = True).distinct()
        else:
            return User.objects.filter(contacts_as_requester__reviewer=self.user, contacts_as_requester__confirmation = True).distinct()
    def get_unconfirmed(self):
        if self.request.user.mode == WRITER_MODE:
            return User.objects.filter(contacts_as_requester__worker=self.user, contacts_as_requester__confirmation = False, contacts_as_requester__created_by=self.user).distinct()
        else:
            return User.objects.filter(contacts_as_requester__reviewer=self.user, contacts_as_requester__confirmation = False, contacts_as_requester__created_by=self.user).distinct()
    def get_requested(self):
        if self.request.user.mode == WRITER_MODE:
            return User.objects.filter(contacts_as_requester__worker=self.user, contacts_as_requester__confirmation = False).exclude(contacts_as_requester__created_by=self.user).distinct()
        else:
            return User.objects.filter(contacts_as_requester__reviewer=self.user, contacts_as_requester__confirmation = False).exclude(contacts_as_requester__created_by=self.user).distinct()
    def get_other(self):
        if self.request.user.mode == WRITER_MODE:
            return User.objects.filter(contacts_as_requester__requester__isnull=False).exclude(contacts_as_worker__requester=self.user).distinct()
        else:
            return User.objects.filter(contacts_as_requester__requester__isnull=False).exclude(contacts_as_reviewer__requester=self.user).distinct()
        
class ReviewerList(UserList):
  user_group='Reviewer'
  def get_all(self):
    return User.objects.filter(Q(contacts_as_worker__position=REVIEWER_POSITION, contacts_as_worker__confirmation=True)|Q(userprofile__mode=REVIEWER_MODE)).exclude(pk=self.user.pk).distinct()
  def get_mine(self):
    return User.objects.filter(contacts_as_worker__requester=self.user, contacts_as_worker__position=REVIEWER_POSITION, contacts_as_worker__confirmation = True).distinct()
  def get_unconfirmed(self):
    return User.objects.filter(contacts_as_worker__requester=self.user, contacts_as_worker__position=REVIEWER_POSITION, contacts_as_worker__confirmation = False, contacts_as_worker__created_by=self.user).distinct()
  def get_requested(self):
    return User.objects.filter(contacts_as_worker__position=REVIEWER_POSITION, contacts_as_worker__requester=self.user, contacts_as_worker__confirmation = False).exclude(contacts_as_worker__created_by=self.user).distinct()
  def get_other(self):
    return User.objects.filter(Q(contacts_as_worker__position=REVIEWER_POSITION).exclude(contacts_as_worker__requester=self.user)|Q(userprofile__mode=REVIEWER_MODE)).distinct()
    
# class CreateRelationship(CreateView):
#   model = Relationship
#   form_class = RelationshipForm
#   template_name = "articles/ajax_user_list_row.html"
#   def form_valid(self, form):
#     self.form = form
#     self.object = self.form.save(commit=False)
#     self.object.created_by = self.request.user
#     self.object = self.form.save()
#     user = self.get_user_object()
#     user.relationship = self.object
#     context = self.get_context_data(form=form)
#     context['object'] = user
#     return self.render_to_response(context)
#   def send_messages_for_form_errors(self, form):
#     for field,error_list in form.errors.items():
#       for error in error_list:
#         messages.error(self.request, "%s: %s" % (field, error))
#   def form_invalid(self, form):
#     self.form = form
#     self.send_messages_for_form_errors(self.form)
#     messages.error(self.request, form.errors)
#     return self.render_to_response(self.get_context_data(form=form))
#   def get_user_object(self):
#     for f in ['Requester','Reviewer','Writer']:
#       if self.form.cleaned_data[f.lower()] and not self.form.cleaned_data[f.lower()] == self.request.user:
#         return self.form.cleaned_data[f.lower()]
#   def get_user_group(self):
#     for f in ['Requester','Reviewer','Writer']:
#       if self.form.cleaned_data[f.lower()] == self.request.user: return f
#   def get_context_data(self, **kwargs):
#     if 'user_group' in self.request.POST: kwargs['user_group'] = self.request.POST['user_group']
#     return super(CreateRelationship, self).get_context_data(**kwargs)

# class DeleteRelationship(DeleteView):
#   model = Relationship
#   template_name = "articles/ajax_user_list_row.html"
#   def get_object(self, queryset=None):
#     self.requester_id = self.request.POST.get('requester')
#     self.writer_id = self.request.POST.get('writer')
#     self.reviewer_id = self.request.POST.get('reviewer')
#     self.user_group = self.request.POST.get('user_group')
#     try:
#       if self.writer_id: 
#         print "looking from writer_id"
#         return Relationship.objects.filter(requester_id=self.requester_id, writer_id=self.writer_id)[0]
#       else: 
#         print "looking from reviewer_id"
#         print "self.requester_id = %s" % str(self.requester_id)
#         print "self.reviewer_id = %s" % str(self.reviewer_id)
#         print "Relationship.objects.filter(requester_id=self.requester_id, reviewer_id=self.reviewer_id) = %s" % str(Relationship.objects.filter(requester_id=self.requester_id, reviewer_id=self.reviewer_id))
#         return Relationship.objects.filter(requester_id=self.requester_id, reviewer_id=self.reviewer_id)[0]
#     except IndexError: raise Http404("No Relationships found matching the query")
#   def get_user(self):
#     if not self.user_group in ['Writer', 'Reviewer']: pk = self.requester_id
#     else: pk = self.writer_id or self.reviewer_id
#     print "pk = %s" % str(pk)
#     print "User.objects.get(pk=pk) = %s" % str(User.objects.get(pk=pk))
#     return User.objects.get(pk=pk)
#   def post(self, request, *args, **kwargs):
#     self.object = self.get_object()
#     self.user = self.get_user()
#     self.object.delete()
#     self.object = self.user
#     context = self.get_context_data()
#     print "context = %s" % str(context)
#     return self.render_to_response(context)
#   def get_context_data(self, **kwargs):
#     kwargs['user_group'] = self.user_group
#     kwargs['object'] = self.object
#     print "kwargs = %s" % str(kwargs)
#     return super(DeleteRelationship, self).get_context_data(**kwargs)
    
# class ConfirmRelationship(TemplateResponseMixin, BaseDetailView):
#   model=Relationship
#   template_name = "articles/ajax_user_list_row.html"
#   def get_object(self, queryset=None):
#     self.requester_id = self.request.POST.get('requester')
#     self.writer_id = self.request.POST.get('writer')
#     self.reviewer_id = self.request.POST.get('reviewer')
#     self.user_group = self.request.POST.get('user_group')
#     try:
#       if self.writer_id: return Relationship.objects.filter(requester_id=self.requester_id, writer_id=self.writer_id)[0]
#       else: return Relationship.objects.filter(requester_id=self.requester_id, reviewer_id=self.reviewer_id)[0]
#     except IndexError: raise Http404("No Relationships found matching the query")
#   def get_user(self):
#     if not self.user_group in ['Writer', 'Reviewer']: pk = self.requester_id
#     else: pk = self.writer_id or self.reviewer_id
#     return User.objects.get(pk=pk)
#   def post(self, *args, **kwargs):
#     self.object = self.get_object()
#     self.object.confirmed = True
#     self.object.save()
#     self.user = self.get_user()
#     context = self.get_context_data()
#     print "context = %s" % str(context)
#     return self.render_to_response(context)
#   def get_context_data(self, **kwargs):
#     kwargs['user_group'] = self.user_group
#     kwargs['object'] = self.user
#     print "kwargs = %s" % str(kwargs)
#     return super(ConfirmRelationship, self).get_context_data(**kwargs)

def test500(request, template_name='admin/500.html'):
    """
    500 error handler.

    Templates: `500.html`
    Context: sys.exc_info() results
     """
    t = loader.get_template(template_name) # You need to create a 500.html template.
    ltype,lvalue,ltraceback = sys.exc_info()
    sys.exc_clear() #for fun, and to point out I only -think- this hasn't happened at 
                    #this point in the process already
    if settings.DEBUG == False: settings.DEBUG = True
    return HttpResponseServerError(t.render(Context({'type':ltype,'value':lvalue,'traceback':ltraceback})))