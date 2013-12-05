import vanilla
from articles.forms import (UserModeForm, OutletActivationForm, NewOutletConfigForm, OutletConfigForm, 
  OAuthVerificationForm)
from filter_views import FiltersMixin
import slick.views as slick
from accounts.views import UserUpdateView
from articles.models import PublishingOutletConfiguration, PublishingOutlet, OAuthRequestToken
from django.contrib.auth.models import User
import pytz
from django.http import HttpResponse
import json
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class ChangeMode(slick.LoginRequiredMixin, vanilla.FormView):
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

class Dashboard(FiltersMixin, slick.LoginRequiredMixin, slick.TemplateView):
  extra_context = {'heading':'Dashboard'}
  template_name = "articles/dashboard.html"

class UserSettingsView(slick.ExtraContextMixin, FiltersMixin, slick.LoginRequiredMixin, UserUpdateView):
  model=User
  success_url="/user/settings/"
  template_name = "articles/user_settings_form.html"
  def get_context_data(self, **kwargs):
    kwargs.update({
      'outlets':PublishingOutletConfiguration.objects.filter(user=self.request.user),
    })
    return super(UserSettingsView, self).get_context_data(**kwargs)
  def form_valid(self, form, user_profile_form):
    # self.request.session['tz'] = user_profile_form.cleaned_data['timezone']
    self.request.session['django_timezone'] = pytz.timezone(user_profile_form.cleaned_data['timezone'])
    return super(UserSettingsView, self).form_valid(form, user_profile_form)

class OutletSettings(slick.ExtraContextMixin, FiltersMixin, slick.LoginRequiredMixin, vanilla.TemplateView):
  template_name = "articles/publishing_outlets_form.html"
  extra_context={
      'object_list':'get_objects',
      'plugins_available':'get_plugins_available',
  }
  def get_plugins_available(self): return PublishingOutlet.objects.all()
  def get_objects(self): return PublishingOutletConfiguration.objects.filter(user=self.request.user)

class OutletConfigUpdate(vanilla.GenericView):
  lookup_field = 'pk'
  lookup_url_kwarg = None
  def get_object(self):
    """
    Returns the object the view is displaying.
    """
    queryset = PublishingOutletConfiguration.objects.all()
    lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

    try:
      lookup = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
      print "lookup = %s" % str(lookup)
    except KeyError:
      msg = "Lookup field '%s' was not provided in view kwargs to '%s'"
      raise ImproperlyConfigured(msg % (lookup_url_kwarg, self.__class__.__name__))

    return get_object_or_404(queryset, **lookup)
  def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    name_form = OutletConfigForm(data=request.POST, files=request.FILES, instance=self.object)
    values = {}
    for setting in self.object.outlet.settings:
      values[setting] = request.POST.get(setting.lower(),"")
    self.object.config=values
    self.object.save()
    if name_form.is_valid():
      name_form.save()
      return HttpResponse(json.dumps({'msg':"Configuration saved successfully."}), content_type="application/json")
    else:
      return HttpResponse(json.dumps({'msg':"There were problems saving your configuration."}), content_type="application/json")

class OutletActivation(vanilla.UpdateView):
  model = PublishingOutletConfiguration
  form_class = OutletActivationForm
  def form_valid(self, form):
    print "form.fields = %s" % str(form.fields)
    print "self.request.POST['active'] = %s" % str(self.request.POST['active'])
    self.object = form.save()
    print "self.object.active = %s" % str(self.object.active)
    if self.object.active: msg = "Outlet Activated Successfully."
    else: msg = "Outlet Deactivated Successfully."
    return HttpResponse(json.dumps({'msg':msg}), content_type="application/json")
  def form_invalid(self, form):
    print "form.errors = %s" % str(form.errors)
    return HttpResponse(json.dumps({'msg':"There was an error activating the outlet."}), content_type="application/json")

# class CreateOutletConfig(vanilla.GenericModelView):
#   model = PublishingOutletConfiguration
#   form_class = NewOutletConfigForm
#   def get(self, request, *args, **kwargs):
#     form = self.get_form(data=request.POST, files=request.FILES)
#     if form.is_valid():
#       return self.form_valid(form)
#     return self.form_invalid(form)
#   def form_valid(self, form):
#     self.object = self.model.objects.create(user=self.request.user, outlet=form.cleaned_data['outlet'])

#     return HttpResponse(json.dumps({
#       'msg':"Outlet created successfully.",
#       'fields':self.object.outlet.settings,
#     }), content_type="application/json")

#   def form_invalid(self, form):
#     return HttpResponse(json.dumps({'msg':"Unable to find specified outlet."}), content_type="application/json")


class CreateOutletConfig(vanilla.GenericModelView):
  model = PublishingOutlet
  template_name = "articles/outlet_config.html"
  def post(self, request, *args, **kwargs):
      self.object = self.get_object()
      outlet_config = PublishingOutletConfiguration.objects.create(user=self.request.user, outlet=self.object)
      context = self.get_context_data(outlet=outlet_config)
      return self.render_to_response(context)

class DeleteOutletConfig(vanilla.DeleteView):
  model = PublishingOutletConfiguration
  def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    pk=self.object.pk
    self.object.delete();
    return HttpResponse(json.dumps({'msg':"The outlet has been removed.",'pk':pk}), content_type="application/json")

class ConfirmOAuthForOutlet(vanilla.GenericView):
  def get(self, request, *args, **kwargs):
    form = OAuthVerificationForm(data=request.GET, files=request.FILES)
    if not form.is_valid(): return self.form_invalid(form)
    request_token = OAuthRequestToken.objects.get(token=form.cleaned_data['oauth_token'])
    config = request_token.config
    config.token, config.secret = config.outlet.plugin.verify_token(request_token, self.request)
    config.save()
    messages.success(self.request, "The account has been authorized successfully.")
    return HttpResponseRedirect(reverse('outlet_settings'))
  def form_valid(self, form): 
    verifier = form.cleaned_data['oauth_verifier']
    
  def form_invalid(self, form):
    messages.error(self.request, "There was an error authorizing your account.")
    return HttpResponseRedirect(reverse('outlet_settings'))
  # def form_valid(self, form):
  #   self.object = form.save()
  #   return HttpResponse(json.dumps({'msg':"Configuration saved successfully."}), content_type="application/json")
  # def form_invalid(self, form):
  #   print "form.errors = %s" % str(form.errors)
  #   return HttpResponse(json.dumps({'msg':"There was an error saving your configuration."}), content_type="application/json")