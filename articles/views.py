from django.views.generic import ListView
from django.template import RequestContext
import urlparse
import pytz
import vanilla
import slick.views as slick
# from extra_views import SearchableListMixin
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from accounts.views import UserUpdateView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.contrib.sites.models import get_current_site
from django.template.defaultfilters import slugify
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin#, ModelFormMixin
from django.views.generic.detail import DetailView, BaseDetailView# , SingleObjectMixin
from django.views.generic import FormView #, TemplateView, 
from articles.models import Article, Keyword, Project, ArticleAction, ACTIONS, Contact, Category, \
PublishingOutlet, PublishingOutletConfiguration, WRITER_POSITION, REVIEWER_POSITION, UserProfile, \
ContactGroup
from django.views.generic.base import View, TemplateResponseMixin
from articles.forms import RejectForm, ArticleForm, KeywordInline, KeywordInlineFormSet,  \
TagArticleForm, ActionUserID, AssignToForm, NoteForm, ContactForm, QuantityForm, \
TagForm, ProjectForm, ACT_SUBMIT, ACT_REJECT, ACT_APPROVE, CategoryForm, RenameGroupForm, \
ACT_ASSIGN_WRITER, ACT_ASSIGN_REVIEWER, ACT_CLAIM_REVIEWER, ACT_RELEASE, ACT_PUBLISH, \
ACT_COMMENT, ACT_REMOVE_REVIEWER, ACT_REMOVE_WRITER, ACT_CLAIM_WRITER, UserModeForm, PublishForm, \
LoginForm, STATUS_NEW, STATUS_RELEASED, STATUS_ASSIGNED, STATUS_SUBMITTED, STATUS_APPROVED, \
FiltersForm, RegistrationForm, STATUS_PUBLISHED, GroupMemberForm, NewGroupForm, \
WriteArticleForm, WRITER_MODE, REVIEWER_MODE, REQUESTER_MODE, SimpleTextForm, CreateArticleForm
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
# import django_filters
# from actions import *
# from django import template
from django.conf import settings

VALID_STRING_LOOKUPS = ('exact','isnull','iexact', 'contains', 'icontains', 'startswith', 'istartswith', 'endswith', 'iendswith', 'search', 'regex', 'iregex')
class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

################################################################################
          #   #   #   #   # ##### #     #       #  
          #   #  # #  ##  #   #   #     #      # # 
           # #   ###  # # #   #   #     #      ### 
           # #  #   # #  ##   #   #     #     #   #
            #   #   # #   # ##### ##### ##### #   #
################################################################################
class MessageMixin(object):
  success_message = None
  error_message = None
  def get_error_message(self, form):return self.error_message
  def get_success_message(self, form):return self.success_message
  def form_valid(self, form):
    msg=self.get_success_message(form)
    if msg: messages.success(self.request, msg)
    return super(MessageMixin, self).form_valid(form)

  def form_invalid(self, form):
    error_msg=self.get_error_message(form)
    if error_msg: messages.error(self.request, error_msg)
    # print "form.errors = %s" % str(form.errors)
    return super(MessageMixin, self).form_invalid(form)
# class HeaderMixin(object):
#   header='Header'
#   def get_header(self): return self.header
#   def get_context_data(self, **kwargs):
#     kwargs['header'] = self.get_header()
#     return super(HeaderMixin, self).get_context_data(**kwargs)
# class CreateView(HeaderMixin, MessageMixin, vanilla.CreateView): pass
# class UpdateView(HeaderMixin, MessageMixin, vanilla.UpdateView): pass
# class DeleteView(MessageMixin, vanilla.DeleteView): pass
# class FormView(HeaderMixin, MessageMixin, vanilla.FormView): pass



# class Filter(object):
#   value=None
#   user_profile=None
#   def __init__(self, **kwargs):
#     request = kwargs.pop('request', None)
#     if request: self.save_request(request)
#     self.model=kwargs.pop('model', None)                # Ex: Project
#     self.choices=kwargs.pop('choices',self.build_choices())
#     self.query_list=kwargs.pop('query_list', None)
#     self.base_attr_name=kwargs.pop('base_attr_name', None) # Attribute name to use to caluclate other attributes below
#     if not self.base_attr_name: 
#       try: self.base_attr_name = self.model._meta.module_name
#       except: self.base_attr_name = ""
#     self.attr_name=kwargs.pop('attr_name', None) # Attribute on profile where filter value is stored
#     if not self.attr_name: self.attr_name = self.base_attr_name+'_filter_value'
#     self.request_keyword=kwargs.pop('request_keyword', None) # keyword to look for in request data
#     if not self.request_keyword: self.request_keyword = self.base_attr_name
#     self.null_query=kwargs.pop('null_query', None) # query string to use to look for null values
#     if not self.null_query: self.null_query = self.base_attr_name+'__isnull'
#   def save_filter_values_from_request(self, request):
#     self.save_request(request)
#     args = (request.GET or request.POST)
#     print "args = %s" % str(args)
#     print "self.request_keyword = %s" % str(self.request_keyword)
#     print "self.request_keyword in args = %s" % str(self.request_keyword in args)
#     if self.request_keyword in args: self.value= args[self.request_keyword]
#     return None
#   def get_user_profile(self, request):
#     if not self.user_profile: 
#       try: self.user_profile = request.user.get_profile()
#       except: return None
#     return self.user_profile

#   def get_choice_key(self, choice):
#     return unicode(choice)
#   def filter_choices(self, qs):
#     return qs
#   def get_choice_list(self):
#     if self.model: return self.filter_choices(self.model.objects.all()).distinct()
#     return []
#   def build_choices(self):
#     choices = {}
#     # print "self.get_choice_list() = %s" % str(self.get_choice_list())
#     for choice in self.get_choice_list():
#       choices[self.get_choice_key(choice)] = choice
#     return choices
#   def return_pipe(self, x,y=None):
#     if x and y: return x | y
#     elif x: return x
#     elif y: return y
#   def save_request(self, request):
#     self.request = request
#   def filter(self, qs, value=None, request=None):
#     if request: self.save_request(request)
#     if not value: value=self.value
#     if not value: return qs
#     if not type(self.query_list)== list: self.query_list=[self.query_list]
#     if ',' in value: value=value.split(',')
#     q=None
#     for query in self.query_list:
#       print "query = %s" % str(query)
#       print "value = %s" % str(value)
#       new_q = Q(**{query:value})
#       print "qs.filter(new_q) = %s" % str(qs.filter(new_q))
#       q=self.return_pipe(q, new_q)
#       print "qs.filter(q) = %s" % str(qs.filter(q))
#     qs=qs.filter(q)
#     return qs
# class ViewFilter(Filter):
#   def get_context(self):
#     # print "self.filters['order'] = %s" % str(self.filters['order'])
#     return [[f,reverse_lazy(f.lower()),self.filters[f](Article.objects.all()).count()] for f in self.filters['order']]

#   def save_request(self, request):
#     self.request = request
#     self.filters=self.get_filters()
#     self.context=self.get_context()
#   def filter_approved(self, qs):
#       return qs.filter(status=STATUS_APPROVED)
#   def filter_assigned(self, qs):
#       if self.user_mode==WRITER_MODE:
#           return qs.filter(writer=self.request.user, was_claimed=False, status=STATUS_ASSIGNED)
#       elif self.user_mode==REQUESTER_MODE:
#           return qs.filter(writer__isnull=False, was_claimed=False, status=STATUS_ASSIGNED)
#   def filter_available(self, qs):
#       if self.user_mode==WRITER_MODE:
#           return qs.filter(writer=None).filter(Q(writer_availability="")|Q(writer_availability__in=self.request.user.writing_contacts))
#       elif self.user_mode==REQUESTER_MODE:
#           return qs.filter(writer=None).exclude(writer_availability="Nobody")
#       elif self.user_mode==REVIEWER_MODE:
#           return qs.filter(reviewer=None,submitted__isnull=False).filter(Q(reviewer_availability="")|Q(reviewer_availability__in=self.request.user.reviewing_contacts))
#   def filter_claimed(self, qs):
#       if self.user_mode==WRITER_MODE:
#           return qs.filter(writer=self.request.user, was_claimed=True, status=STATUS_ASSIGNED)
#       elif self.user_mode==REQUESTER_MODE:
#           return qs.filter(was_claimed=True, status=STATUS_ASSIGNED)
#   def filter_rejected(self, qs):
#       return qs.filter(rejected__isnull=False)
#   def filter_published(self, qs):
#       return qs.filter(status=STATUS_PUBLISHED)
#   def filter_submitted(self, qs):
#       if self.user_mode==WRITER_MODE:
#           return qs.filter(writer=self.request.user, status=STATUS_SUBMITTED,submitted__isnull=False, approved__isnull=True)
#       elif self.user_mode==REQUESTER_MODE:
#           return qs.filter(status=STATUS_SUBMITTED,submitted__isnull=False, approved__isnull=True)
#   def filter_unavailable(self, qs):
#       return qs.filter(writer_availability="Nobody", status__in=[STATUS_NEW, STATUS_RELEASED])
#   def get_filters(self):
#     self.user_mode=self.request.user.mode
#     if self.user_mode==WRITER_MODE:
#         return {
#             'Available':self.filter_available,
#             'Assigned':self.filter_assigned,
#             'Claimed':self.filter_claimed,
#             'Submitted':self.filter_submitted,
#             'Approved':self.filter_approved,
#             'Rejected':self.filter_rejected,
#             'order':['Available','Assigned','Claimed','Submitted','Approved','Rejected']
#         }
#     elif self.user_mode==REQUESTER_MODE:
#         return {
#             'Unavailable':self.filter_unavailable,
#             'Available':self.filter_available,
#             'Assigned':self.filter_assigned,
#             'Claimed':self.filter_claimed,
#             'Submitted':self.filter_submitted,
#             'Approved':self.filter_approved,
#             'Rejected':self.filter_rejected,
#             'Published':self.filter_published,
#             'order':['Unavailable','Available','Assigned','Claimed','Submitted','Approved','Rejected','Published']
#         }
#     elif self.user_mode==REVIEWER_MODE:
#         return {
#             'Available':self.filter_available,
#             'Approved':self.filter_approved,
#             'Rejected':self.filter_rejected,
#             'order':['Available','Approved','Rejected']
#         }
#     else: return {'order':[]}
#   # def save_filter_values_from_request(self, request):
#   #   super(ViewFilter, self).save_filter_values_from_request(request)
#   #   self.filters=self.get_filters()
#   def filter(self, qs, value=None, request=None):
#     if request: self.request=request
#     if not value: value=self.value
#     if not value: return qs
#     return self.filters[value](qs)
class FormWithUserMixin(object):
  def get_form(self, data=None, files=None, **kwargs):
    kwargs['user'] = self.request.user
    return super(FormWithUserMixin, self).get_form(data=data, files=files, **kwargs)

################################################################################
      ##### ##### #     ##### ##### ####   ####
      #       #   #       #   #     #   # #    
      ####    #   #       #   ####  ####   ### 
      #       #   #       #   #     #   #     #
      #     ##### #####   #   ##### #   # #### 
################################################################################

class FiltersMixin(object):
  extra_context ={
    "article_filter_counts": 'get_article_filter_counts',
    "writer_filter_counts": 'get_writer_filter_counts',
    "reviewer_filter_counts": 'get_reviewer_filter_counts',
  }
  def filter_approved(self, qs, value=True):
    return qs.filter(status=STATUS_APPROVED)
  def filter_assigned(self, qs, value=True):
    if self.request.user.mode==WRITER_MODE:
      return qs.filter(writer=self.request.user, was_claimed=False, status=STATUS_ASSIGNED)
    elif self.request.user.mode==REQUESTER_MODE:
      return qs.filter(writer__isnull=False, was_claimed=False, status=STATUS_ASSIGNED)
  def filter_available(self, qs, value=True):
    if self.request.user.mode==WRITER_MODE:
      return qs.filter(writer=None).filter(Q(writer_availability="")|Q(writer_availability__in=self.request.user.writing_contacts))
    elif self.request.user.mode==REQUESTER_MODE:
      return qs.filter(writer=None).exclude(writer_availability="Nobody")
    elif self.request.user.mode==REVIEWER_MODE:
      return qs.filter(reviewer=None,submitted__isnull=False).filter(Q(reviewer_availability="")|Q(reviewer_availability__in=self.request.user.reviewing_contacts))
  def filter_claimed(self, qs, value=True):
    if self.request.user.mode==WRITER_MODE:
      return qs.filter(writer=self.request.user, was_claimed=True, status=STATUS_ASSIGNED)
    elif self.request.user.mode==REQUESTER_MODE:
      return qs.filter(was_claimed=True, status=STATUS_ASSIGNED)
  def filter_rejected(self, qs, value=True):
    return qs.filter(rejected__isnull=False)
  def filter_published(self, qs, value=True):
    return qs.filter(status=STATUS_PUBLISHED)
  def filter_submitted(self, qs, value=True):
    if self.request.user.mode==WRITER_MODE:
      return qs.filter(writer=self.request.user, status=STATUS_SUBMITTED,submitted__isnull=False, approved__isnull=True)
    elif self.request.user.mode==REQUESTER_MODE:
      return qs.filter(status=STATUS_SUBMITTED,submitted__isnull=False, approved__isnull=True)
  def filter_unavailable(self, qs, value=True):
    return qs.filter(writer_availability="Nobody", status__in=[STATUS_NEW, STATUS_RELEASED])
  def filter_my_writers(self, qs, value=True):
    return qs.filter(requester=self.request.user, confirmation = True, position=WRITER_POSITION)
  def filter_writers_pending(self, qs, value=True):
    return qs.filter(requester=self.request.user, confirmation__isnull=True, position=WRITER_POSITION)
  def filter_writers_available(self, qs, value=True):
    qs = qs.filter(Q(contacts_as_worker__position=WRITER_POSITION)|Q(userprofile__mode=WRITER_MODE)).distinct()
    return qs.exclude(contacts_as_worker__requester=self.request.user, contacts_as_worker__position=WRITER_POSITION).exclude(pk=self.request.user.pk)
  def filter_my_reviewers(self, qs, value=True):
    return qs.filter(requester=self.request.user, confirmation = True, position=REVIEWER_POSITION)
  def filter_reviewers_pending(self, qs, value=True):
    return qs.filter(requester=self.request.user, confirmation__isnull=True, position=REVIEWER_POSITION)
  def filter_reviewers_available(self, qs, value=True):
    qs = qs.filter(Q(contacts_as_worker__position=REVIEWER_POSITION)|Q(userprofile__mode=REVIEWER_MODE)).distinct()
    return qs.exclude(contacts_as_worker__requester=self.request.user, contacts_as_worker__position=REVIEWER_POSITION).exclude(pk=self.request.user.pk)
  def filter_writer_groups(self, qs, value=True):
    return qs.filter(position=WRITER_POSITION, owner=self.request.user)
  def filter_reviewer_groups(self, qs, value=True):
    return qs.filter(position=REVIEWER_POSITION, owner=self.request.user)
  def get_article_filter_counts(self):
    # Last value, when True, forces item to show in sidebar even when empty
    return {
      'Unavailable': (self.filter_unavailable(Article.objects.all()).count(),False),
      'Available': (self.filter_available(Article.objects.all()).count(),not self.request.user.mode==REQUESTER_MODE),
      'Assigned': (self.filter_assigned(Article.objects.all()).count(),False),
      'Claimed': (self.filter_claimed(Article.objects.all()).count(),False),
      'Submitted': (self.filter_submitted(Article.objects.all()).count(),False),
      'Approved': (self.filter_approved(Article.objects.all()).count(),False),
      'Rejected': (self.filter_rejected(Article.objects.all()).count(),False),
      'Published': (self.filter_published(Article.objects.all()).count(),False),
    }
  def get_writer_filter_counts(self):
    # Last value, when True, forces item to show in sidebar even when empty
    return {
      'My Writers': (self.filter_my_writers(Contact.objects.all()).count(),False),
      'Writers Pending': (self.filter_writers_pending(Contact.objects.all()).count(),False),
      'Writers Avail.': (self.filter_writers_available(User.objects.all()).count(),True),
      'Writer Groups': (self.filter_writer_groups(ContactGroup.objects.all()).count(),True),
    }
  def get_reviewer_filter_counts(self):
    # Last value, when True, forces item to show in sidebar even when empty
    return {
      'My Reviewers': (self.filter_my_reviewers(Contact.objects.all()).count(),False),
      'Reviewers Pending': (self.filter_reviewers_pending(Contact.objects.all()).count(),False),
      'Reviewers Avail.': (self.filter_reviewers_available(User.objects.all()).count(),True),
      'Reviewer Groups': (self.filter_reviewer_groups(ContactGroup.objects.all()).count(),True),
    }

# class AvailablilityMixin(object):
#   # Adds in code to put together dropdowns for assigning articles and making articles available
#   def get_available_list(self, group):
#     return list(set([c.name for c in group]))
#   def get_assignee_list(self, group):
#     return list(set([contact.worker for contact in group]))
#   def get_context_data(self, **kwargs):
#     try:
#       kwargs['writer_availability_list']  = self.get_available_list(self.request.user.writer_contacts)
#       kwargs['reviewer_availability_list']= self.get_available_list(self.request.user.reviewer_contacts)
#       kwargs['writer_assignment_list']    = self.get_assignee_list(self.request.user.writer_contacts)
#       kwargs['reviewer_assignment_list']  = self.get_assignee_list(self.request.user.reviewer_contacts)
#     except AttributeError: pass
#     context = super(AvailablilityMixin, self).get_context_data(**kwargs)
#     return context    

# class GetActionsMixin(object):
#     def get_context_data(self, *args, **kwargs):
#         object_list_displayed = kwargs['object_list']
#         kwargs['all_items_count'] = object_list_displayed.count()
#         # Storing serialized queryset using query attribute
#         self.request.session['serialized_qs'] = pickle.dumps(object_list_displayed.query)
#         self.request.session['serialized_model_qs'] = object_list_displayed.model
#         context = super(GetActionsMixin, self).get_context_data(**kwargs)
#         # context['actions']=self.get_actions() 
#         return context

################################################################################
        #   ####  ##### #####  ###  #     #####       #     #####  #### #####
       # #  #   #   #     #   #   # #     #           #       #   #       #  
       ###  ####    #     #   #     #     ####        #       #    ###    #  
      #   # #   #   #     #   #   # #     #           #       #       #   #  
      #   # #   #   #   #####  ###  ##### #####       ##### ##### ####    #  
################################################################################

class ArticleListBase(FiltersMixin, slick.ListView): 
  model = Article
  extra_context ={
    'writer_availability_list':'get_writer_availability_list',
    'reviewer_availability_list':'get_reviewer_availability_list',
    'writer_availability_list':'get_writer_availability_list',
    'writer_assignment_list':'get_writer_assignment_list',
    'all_items_count':'get_object_list_count',
    'serialized_qs':'get_serialized_qs',
    'serialized_model_qs':'get_serialized_model_qs',
    'hidden_columns':['Reviewer','Status','Category','Length','Priority','Tags'],
    'all_columns':['Project','Keywords','Writer','Reviewer','Status','Category','Length','Priority','Tags'],
  }
  # Functions for getting lists of contacts for assignment dropdowns
  def get_available_list(self, group): return list(set([c.name for c in group]))
  def get_assignee_list(self, group): return list(set([contact.worker for contact in group]))
  def get_writer_availability_list(self): return self.get_available_list(self.request.user.writer_contacts)
  def get_reviewer_availability_list(self): return self.get_available_list(self.request.user.reviewer_contacts)
  def get_writer_availability_list(self): return self.get_assignee_list(self.request.user.writer_contacts)
  def get_writer_assignment_list(self): return self.get_assignee_list(self.request.user.reviewer_contacts)
  # Functions for getting info about list for doing actions on all
  def get_object_list_count(self): return self.object_list.count()
  def get_serialized_qs(self): return pickle.dumps(self.object_list.query)
  def get_serialized_model_qs(self): self.object_list.model
  def get(self, request, *args, **kwargs):
    self.request.session['article_list_view'] = self.request.path
    return super(ArticleListBase, self).get(request, *args, **kwargs)
  
class AvailableArticles(ArticleListBase):
  search_on = ['tags','project__name','keyword__keyword']
  filter_on = ['available', 'project','writer']
  header = "Available Articles"
  def get_context_data(self, **kwargs):
    context = super(AvailableArticles, self).get_context_data(**kwargs)
    return context
class UnavailableArticles(ArticleListBase):
  search_on = ['tags','project__name','keyword__keyword']
  filter_on = ['unavailable', 'project','writer']
  extra_context = {
    'hidden_columns':['Writer','Reviewer','Status','Category','Length','Priority','Tags'],
    'header':'Unavailable Articles',
  }
class AssignedArticles(ArticleListBase):
  search_on = ['tags','project__name','keyword__keyword']
  filter_on = ['assigned', 'project','writer']
  extra_context = {'header':'Assigned Articles'}
class ClaimedArticles(ArticleListBase):
  search_on = ['tags','project__name','keyword__keyword']
  filter_on = ['claimed', 'project','writer']
  extra_context = {'header':'Claimed Articles'}
class SubmittedArticles(ArticleListBase):
  search_on = ['tags','project__name','keyword__keyword']
  filter_on = ['submitted', 'project','writer']
  extra_context = {'header':'Submitted Articles'}
class ApprovedArticles(ArticleListBase):
  search_on = ['tags','project__name','keyword__keyword']
  filter_on = ['approved', 'project','writer']
  extra_context = {'header':'Approved Articles'}
class RejectedArticles(ArticleListBase):
  search_on = ['tags','project__name','keyword__keyword']
  filter_on = ['rejected', 'project','writer']
  extra_context = {'header':'Rejected Articles'}
class PublishedArticles(ArticleListBase):
  search_on = ['tags','project__name','keyword__keyword']
  filter_on = ['published', 'project','writer']
  extra_context = {'header':'Published Articles'}

class UserProfileMixin(object):
  user_profile=None
  @property
  def user_profile(self):
    if not self.user_profile:
      try: self.user_profile = self.request.user.get_profile()
      except: pass

# class FilterMixin(UserProfileMixin):
#   filter_fields=[]
#   def save_filter_values_from_request(self, request):
#     for v in self.filters.values():
#       v.save_filter_values_from_request(request)
#   def get_context_data(self, **kwargs):
#     context = super(FilterMixin, self).get_context_data(**kwargs)
#     context['filters']=self.filters
#     return context
#   def get_queryset(self):
#     qs=super(FilterMixin, self).get_queryset()
#     for f in self.filters.values():
#       print "qs = %s" % str(qs)
#       qs=f.filter(qs)
#     return qs
#   def get_query_filters(self):
#     filters={}
#     if self.filter_fields:
#       for args in self.filter_fields:
#         field_filter=args.get('field_filter', Filter)
#         name=args.get('name')
#         filters[name] = field_filter(
#           model=args.get('model', None),
#           query_list=args.get('query_list'),
#           attr_name=args.get('attr_name',None),
#           request_keyword=args.get('request_keyword',None),
#           base_attr_name=args.get('base_attr_name',None),
#           null_query=args.get('null_query',None),
#           )
#     return filters
#   def __init__(self, **kwargs):
#     self.filters = self.get_query_filters()
#   def get(self, request, *args, **kwargs):
#     self.save_filter_values_from_request(request)
#     return super(FilterMixin, self).get(request, *args, **kwargs)

# class ArticleFilterMixin(FilterMixin):
#     filter_fields=[
#       {'name':'project', 'model':Project, 'field_filter':Filter, 'query_list':'project__name__in'}, 
#       {'name':'search', 'base_attr_name':'q', 'query_list':['tags__icontains','project__name__icontains','keyword__keyword__icontains']},
#       {'name':'writer', 'model':User, 'field_filter':Filter,'base_attr_name':'writer', 'query_list':["writer__username__in","writer__first_name__in","writer__last_name__in"]},
#       {'name':'view','field_filter':ViewFilter, 'base_attr_name':'view',},
#     ]

# class ArticleList(AvailablilityMixin, GetActionsMixin, ArticleFilterMixin, ListView):
#     model = Article
#     # search_fields = ['tags', 'project__name', 'keyword__keyword']
#     hidden_columns = ['Reviewer','Status','Category','Length','Priority','Tags']
#     name = "Available"
#     reverse_url=None
    
#     def get_view_header(self):
#       header=self.filters['view'].value
#       if header: return header.title()+ " Articles"
#       else: return "Available Articles"
#       # return self.current_filter.title()+ " Articles"
#     def get_hidden_columns(self):
#       current_view = self.filters['view'].value
#       if current_view == 'Unavailable':return ['Writer','Reviewer','Status','Category','Length','Priority','Tags']
#       elif current_view == 'Available':return ['Reviewer','Status','Category','Length','Priority','Tags']
#       elif current_view == 'Assigned':return ['Reviewer','Status','Category','Length','Priority','Tags']
#       elif current_view == 'Claimed':return ['Reviewer','Status','Category','Length','Priority','Tags']
#       elif current_view == 'Submitted':return ['Reviewer','Status','Category','Length','Priority','Tags']
#       elif current_view == 'Approved':return ['Reviewer','Status','Category','Length','Priority','Tags']
#       elif current_view == 'Rejected':return ['Reviewer','Status','Category','Length','Priority','Tags']
#       elif current_view == 'Published':return ['Reviewer','Status','Category','Length','Priority','Tags']
#       return self.hidden_columns
#     def get_reverse_url(self):
#         if self.reverse_url: return self.reverse_url
#         else: return self.name.lower()
#     def get_context_data(self, **kwargs):
#         # kwargs['view_filters']=self.get_sidebar_context()
#         # kwargs['current_filter'] = self.current_filter
#         # kwargs['user']=self.request.user
#         kwargs['selected_tab']=self.name
#         kwargs['hidden_columns']=self.get_hidden_columns()
#         kwargs['all_columns']=['Project','Keywords','Writer','Reviewer','Status','Category','Length','Priority','Tags']
#         kwargs['header']=self.get_view_header()
#         # kwargs['active_filters']='January,February,July'
#         context = super(ArticleList, self).get_context_data(**kwargs)
#         return context
#     def get(self, request, *args, **kwargs):
#         # self.filter_fields = self.get_filter_fields()
#         try: self.request.user.mode
#         except: self.request.user.mode = None
#         response = super(ArticleList, self).get(request, *args, **kwargs)
#         try:
#             user_profile=self.request.user.get_profile()
#             user_profile.article_list_view = self.get_reverse_url()
#             user_profile.save()
#         except AttributeError:pass
#         return response
    #     # if 'last_action' in self.request.GET:
    #     #     qs=qs.filter(last_action__code=self.request.GET['last_action'])
    #     if 'status' in self.request.GET:
    #         qs=qs.filter(status=self.request.GET['status'])
    #     return qs


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

class SimpleRelatedCreate(FormWithUserMixin, AjaxUpdateMixin, CreateView):
  # This is a base class for creating categories and projects
  # Takes name, owner, and article_id
  # Creates object with given name and owner and assignes it to article
  # Returns message and option and list item
  error_message_template = 'Unable to create %s with given name.'
  template_name = 'articles/simple_related_form.html'
  # def get_template_names(self):
  #   return[]

class ProjectCreate(SimpleRelatedCreate):
  model = Project
  form_class = ProjectForm
class CategoryCreate(SimpleRelatedCreate):
  # Takes name, owner, and article_id
  # Creates Project with given name and owner and assignes it to article
  # Returns message and article project field with new item selected
  model = Category
  form_class = CategoryForm


class ProjectList(ListView):
    model = Project
    search_fields = ['name']
    # filter_fields={
    #     'owner':Filter(base=Project, model=User, display_attr='username'),
    # }
    def get_context_data(self, **kwargs):
        kwargs['selected_tab']='projects'
        return super(ProjectList, self).get_context_data(**kwargs)

class ArticleCreate(FiltersMixin, FormWithUserMixin, LoginRequiredMixin, CreateWithInlinesView):
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
        print "============================"
        print "response = %s" % str(response)
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
        try:
            user=self.request.user
            user_profile=self.request.user.get_profile()
            return reverse_lazy(user_profile.article_list_view)
        except: return super(ArticleCreate, self).get_success_url()
class UpdateArticle(LoginRequiredMixin, UpdateWithInlinesView):
    model = Article
    inlines = [KeywordInline]
    template_name = 'articles/article_edit.html'
    extra = 1
    max_num = 1
    def get_success_url(self):
      try: return reverse_lazy(self.request.user.get_profile())
      except: return reverse_lazy('available')
    def get_form_class(self):
      if self.request.user == self.object.owner and self.request.user.in_requester_mode: 
        return ArticleForm
      else: 
        self.inlines = []
        return WriteArticleForm
    def forms_valid(self, form, inlines):
      results = super(ArticleUpdate, self).forms_valid(form, inlines)
      if 'saveandsubmit' in self.request.POST: self.object.submit(self.request)
      if 'saveandapprove' in self.request.POST: self.object.approve(self.request.user)
      return results
    def get_form(self, data=None, files=None, **kwargs):
        kwargs['user'] = self.request.user
        return super(UpdateArticle, self).get_form(data=data, files=files, **kwargs)
# class ArticleUpdate(ArticleFilterMixin, FormWithUserMixin, LoginRequiredMixin, UpdateWithInlinesView):
#     template_name = 'articles/article_edit.html'
#     model = Article
#     form_class = ArticleForm
#     extra = 1
#     max_num = 1
#     inlines = [KeywordInlineFormSet]
#     success_url = reverse_lazy('available')
#     def get_success_url(self):
#         try:
#             user=self.request.user
#             user_profile=self.request.user.get_profile()
#             url= reverse_lazy(user_profile.article_list_view)
#         except: 
#             url= super(ArticleUpdate, self).get_success_url()
#         return url
#     def get_form_class(self):
#         if self.request.user == self.object.owner and self.request.user.in_requester_mode: 
#             return ArticleForm
#         else: 
#             self.inlines = []
#             return WriteArticleForm
#     def get_context_data(self, **kwargs):
#         kwargs['article']=self.object
#         context = super(ArticleUpdate, self).get_context_data(**kwargs)
#         return context

# class ArticleDelete(LoginRequiredMixin, DeleteView):
#     model = Article
#     success_url = reverse_lazy('article_list')

class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('list_projects')
    
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
    action_form_class = SimpleTextForm

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

################################################################################
#                               User Profile                                   #
################################################################################



class ChangeModeView(vanilla.FormView):
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

class UpdateFilters(FiltersMixin, ListView):
    template_name = "articles/ajax_article_list_row.html"
    model = Article
# class ContactMixin(object):
#   worker_type = None
#   def get_contact(self, user):
#     q = Contact.objects.filter(Q(requester=user)|Q(worker=user))
#     if self.worker_type: q = q.filter(position = self.worker_type) 
#     try: return q[0]
#     except: return get_object_or_404()
#   def get_object(self):
#     """
#     Sets the current relationship as object.contact
#     """
#     obj = super(ContactMixin, self).get_object()
#     obj.contact = self.get_contact(obj)
#     return obj
################################################################################
            ###   ###  #   # #####   #    ###  #####  ###
           #   # #   # ##  #   #    # #  #   #   #   #   
           #     #   # # # #   #    ###  #       #    ##
           #   # #   # #  ##   #   #   # #   #   #      #
            ###   ###  #   #   #   #   #  ###    #   ###
################################################################################

class WorkerListBase(FiltersMixin, slick.ListView):
  model=Contact
  template_name = "articles/contact_list.html"
  extra_context = {'row_template_name':"articles/worker_row.html"}
  search_on=['worker__username', 'worker__first_name', 'worker__last_name']

class RequesterListBase(FiltersMixin, slick.ListView):
  model=Contact
  template_name = "articles/contact_list.html"
  extra_context = {'row_template_name':"articles/requester_row.html"}
  search_on=['requester__username', 'requester__first_name', 'requester__last_name']

class UserListBase(FiltersMixin, slick.ListView):
  model = User
  extra_context = {
    'row_template_name':"articles/user_row.html",
  }
  search_on = ['username','first_name','last_name']
  template_name = "articles/user_list.html"
################################################################################
#                               Writers                                  #
################################################################################
class WritersPendingList(WorkerListBase):
  extra_context = {'header':"Writers Pending Approval"}
  filter_on = ['writers_pending']

class MyWritersList(WorkerListBase):
  extra_context = {'header' : "My Writers"}
  filter_on = ['my_writers']
  # def get_queryset(self): 
  #   return Contact.objects.filter(requester=self.request.user, confirmation = True, position=WRITER_POSITION)

class AvailableWritersList(UserListBase):
  extra_context = {
    'header':"Available Writers", 
    'position':WRITER_POSITION,
  }
  filter_on = ['writers_available']
  # def get_queryset(self):
  #   queryset = super(AvailableWritersList, self).get_queryset()
  #   # Filter for users with writing contracts or users in writer mode
  #   queryset = queryset.filter(Q(contacts_as_worker__position=WRITER_POSITION)|Q(userprofile__mode=WRITER_MODE)).distinct()
  #   # Filter for users I dont have a contact for.
  #   return queryset.exclude(contacts_as_worker__requester=self.request.user).exclude(pk=self.request.user.pk)


################################################################################
#                               Reviewers                                      #
################################################################################

class ReviewersPendingList(WorkerListBase):
  extra_context = {'header':"Reviewers Pending Approval"}
  filter_on = ['reviewers_pending']
class MyReviewersList(WorkerListBase):
  extra_context = {'header' : "My Reviewers"}
  filter_on = ['my_reviewers']
class AvailableReviewersList(UserListBase):
  extra_context = {
    'header':"Available Reviewers", 
  }
  filter_on = ['reviewers_available']
class MyRequestersList(RequesterListBase):
  extra_context = {'header':"Requesters Pending Approval"}
  filter_on = ['requesters_pending']
class RequestersPendingList(RequesterListBase):
  extra_context = {'header' : "My Requesters"}
  filter_on = ['my_requesters']
class AvailableRequestersList(FiltersMixin, slick.ListView):
  extra_context = {
    'header':"Available Requesters", 
  }
  filter_on = ['requesters_available']

################################################################################
#                               Ajax                                           #
################################################################################
class CreateContact(slick.UpdateView):
  extra_context = {
    'hide_row':True,
    'row_template_name':"articles/user_row.html",
  }
  model = User
  form_class = ContactForm
  template_name = "design/ajax_row.html"
  success_message = "Your request has been processed."
  error_message = "There was a problem processing your request."

  def get_form(self, data=None, files=None, **kwargs):
    # Creates a blank ContactForm rather than an UserUpdate form
    cls = self.get_form_class()
    instance=kwargs.pop('instance')
    kwargs['user']=self.request.user
    return cls(data=data, files=files, **kwargs)

  def form_valid(self, form):
    self.object.contact = form.save()
    messages.success(self.request, self.success_message)
    context = self.get_context_data(form=form)
    return self.render_to_response(context)

class ConfirmContact(slick.GenericModelView):
  model = Contact
  extra_context = {
    'hide_row':True,
    'row_template_name':"articles/worker_row.html",
  }
  template_name = "design/ajax_row.html"
  success_message = "The contact has been confirmed successfully."
  def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    self.object.confirmation=True
    self.object.save()
    messages.success(self.request, self.success_message)
    return self.render_to_response(self.get_context_data())

class DeleteContact(slick.AjaxDeleteView):
  success_message = "The contact has been deleted."
  model = Contact
  extra_context = {
    'hide_row':True,
    'row_template_name':"articles/worker_row.html",
  }
  template_name = "design/ajax_row.html"

class CancelContactRequest(DeleteContact):
  success_message = "The contact request has been canceled."

class RejectContactRequest(DeleteContact):
  success_message = "The contact request has been rejected."


################################################################################
       ###  ####   ###  #   # ####   ####
      #     #   # #   # #   # #   # #    
      #  ## ####  #   # #   # ####   ### 
      #   # #   # #   # #   # #         #
       ###  #   #  ###   ###  #     #### 
################################################################################
class GroupList(FiltersMixin, slick.ListView):
  model = ContactGroup
  template_name = 'articles/contact_group_list.html'
  extra_context = {'row_template_name':"articles/contact_group_row.html"}

class WriterGroupList(GroupList):
  extra_context = {'header':"Writer Groups",'position':WRITER_POSITION}
  filter_on = ['writer_groups']

class ReviewerGroupList(GroupList):
  extra_context = {'header':"Reviewer Groups",'position':REVIEWER_POSITION}
  filter_on = ['reviewer_groups']

class AddGroup(slick.AjaxCreateView):
  model = ContactGroup
  form_class = NewGroupForm
  extra_context = {'row_template_name':"articles/contact_group_row.html"}
  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.owner = self.request.user
    self.object = form.save()
    return super(AddGroup, self).form_valid(form)

class RenameGroup(slick.AjaxUpdateView):
  model = ContactGroup
  form_class = RenameGroupForm
  extra_context = {'row_template_name':"articles/contact_group_row.html"}

class RemoveGroup(slick.AjaxDeleteView):
  model = ContactGroup
  extra_context = {
    'row_template_name':"articles/contact_group_row.html",
    'hide_row':True,
  }

class AddToGroup(slick.NonModelFormMixin, slick.AjaxUpdateView):
  model = ContactGroup
  form_class = GroupMemberForm
  template_name = "articles/contact_group_detail_lists.html"
  def form_valid(self, form):
    self.object.contacts.add(form.cleaned_data['contact'])
    return HttpResponse("AOK.")


class RemoveFromGroup(slick.NonModelFormMixin, slick.AjaxUpdateView):
  model = ContactGroup
  form_class = GroupMemberForm
  extra_context = {
    'row_template_name':"articles/group_member_row.html",
    'hide_row':True,
  }
  def form_valid(self, form):
    self.object.contacts.remove(form.cleaned_data['contact'])
    return HttpResponse("AOK.")


class GroupDetail(FiltersMixin, slick.DetailView):
  model = ContactGroup
  template_name = 'articles/contact_group_detail.html'
  extra_context={
    'header':'get_header',
    'worker_list':'get_workers'
  }
  def get_header(self): return self.object.name + " Group"
  def get_workers(self):
    return Contact.objects.filter(requester=self.request.user, confirmation=True, position=self.object.position).exclude(contactgroup=self.object).exclude(worker=self.request.user)

################################################################################
      #   # #####  ####  ### 
      ## ##   #   #     #   #
      # # #   #    ###  #    
      #   #   #       # #   #
      #   # ##### ####   ### 
################################################################################

class Dashboard(FiltersMixin, slick.TemplateView):
  extra_context = {'header':'Dashboard'}
  template_name = "articles/dashboard.html"

class ChangeModeView(FormView):
  form_class=LoginForm
  def form_valid(self, form):
    p = self.request.user.get_profile()
    p.mode = form.cleaned_data['mode']
    p.save()
    # self.request.user.mode = form.cleaned_data['mode']
    messages.info(self.request, "You are now in %s mode." % self.request.user.mode_display)
    return HttpResponseRedirect(reverse_lazy('article_list'))
  def form_invalid(self, form): 
    return HttpResponseRedirect(reverse_lazy('article_list'))

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


class UserSettingsView(FiltersMixin, UserUpdateView):
  model=User
  success_url="/user/settings/"
  template_name = "accounts/user_form.html"
  def form_valid(self, form, user_profile_form):
    # self.request.session['tz'] = user_profile_form.cleaned_data['timezone']
    self.request.session['django_timezone'] = pytz.timezone(user_profile_form.cleaned_data['timezone'])
    return super(UserSettingsView, self).form_valid(form, user_profile_form)
