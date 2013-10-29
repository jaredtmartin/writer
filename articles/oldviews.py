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
ContactGroup, Writer, Reviewer, WriterGroup, ReviewerGroup
from django.views.generic.base import View, TemplateResponseMixin
from articles.forms import RejectForm, ArticleForm, KeywordInline, KeywordInlineFormSet,  \
TagArticleForm, ActionUserID, AssignToForm, NoteForm, WriterForm, ReviewerForm, QuantityForm, \
TagForm, ProjectForm, ACT_SUBMIT, ACT_REJECT, ACT_APPROVE, CategoryForm, RenameGroupForm, \
ACT_ASSIGN_WRITER, ACT_ASSIGN_REVIEWER, ACT_CLAIM_REVIEWER, ACT_RELEASE, ACT_PUBLISH, \
ACT_COMMENT, ACT_REMOVE_REVIEWER, ACT_REMOVE_WRITER, ACT_CLAIM_WRITER, UserModeForm, PublishForm, \
LoginForm, STATUS_NEW, STATUS_RELEASED, STATUS_ASSIGNED, STATUS_SUBMITTED, STATUS_APPROVED, \
FiltersForm, RegistrationForm, STATUS_PUBLISHED, GroupMemberForm, NewGroupForm, ContactForm, \
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

class ShowTag(ArticleListBase):
  pass
################################################################################
  #   # #   # #     ##### #####         #    ###  ##### #####  ###  #   #  ####
  ## ## #   # #       #     #          # #  #   #   #     #   #   # ##  # #    
  # # # #   # #       #     #          ###  #       #     #   #   # # # #  ### 
  #   # #   # #       #     #         #   # #   #   #     #   #   # #  ##     #
  #   #  ###  #####   #   #####       #   #  ###    #   #####  ###  #   # #### 
################################################################################


################################################################################
#                               User Profile                                   #
################################################################################




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




################################################################################
      #   # #####  ####  ### 
      ## ##   #   #     #   #
      # # #   #    ###  #    
      #   #   #       # #   #
      #   # ##### ####   ### 
################################################################################


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
