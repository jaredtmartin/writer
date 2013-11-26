import vanilla
from articles.forms import UserModeForm, OutletActivationForm
from filter_views import FiltersMixin
import slick.views as slick
from accounts.views import UserUpdateView
from articles.models import PublishingOutletConfiguration
from django.contrib.auth.models import User
import pytz
from django.http import HttpResponse
import json
from django.shortcuts import get_object_or_404

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

class UserSettingsView(FiltersMixin, slick.LoginRequiredMixin, UserUpdateView):
  model=User
  success_url="/user/settings/"
  template_name = "accounts/user_form.html"
  def get_context_data(self, **kwargs):
    kwargs.update({
      'outlets':PublishingOutletConfiguration.objects.filter(user=self.request.user),
    })
    return super(UserSettingsView, self).get_context_data(**kwargs)
  def form_valid(self, form, user_profile_form):
    # self.request.session['tz'] = user_profile_form.cleaned_data['timezone']
    self.request.session['django_timezone'] = pytz.timezone(user_profile_form.cleaned_data['timezone'])
    return super(UserSettingsView, self).form_valid(form, user_profile_form)

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
    values = {}
    for setting in self.object.outlet.settings:
      values[setting] = request.POST.get(setting.lower(),"")
    self.object.config=values
    self.object.save()
    return HttpResponse(json.dumps({'msg':"Configuration saved successfully."}), content_type="application/json")

class OutletActivation(vanilla.UpdateView):
  model = PublishingOutletConfiguration
  form_class = OutletActivationForm
  def form_valid(self, form):
    print "form.fields = %s" % str(form.fields)
    print "self.request.POST['active'] = %s" % str(self.request.POST['active'])
    self.object = form.save()
    print "self.object.active = %s" % str(self.object.active)
    if self.object.active: msg = ": Outlet Activated Successfully."
    else: msg = ": Outlet Deactivated Successfully."
    return HttpResponse(json.dumps({'msg':msg}), content_type="application/json")
  def form_invalid(self, form):
    print "form.errors = %s" % str(form.errors)
    return HttpResponse(json.dumps({'msg':"There was an error activating the outlet."}), content_type="application/json")



  # def form_valid(self, form):
  #   self.object = form.save()
  #   return HttpResponse(json.dumps({'msg':"Configuration saved successfully."}), content_type="application/json")
  # def form_invalid(self, form):
  #   print "form.errors = %s" % str(form.errors)
  #   return HttpResponse(json.dumps({'msg':"There was an error saving your configuration."}), content_type="application/json")