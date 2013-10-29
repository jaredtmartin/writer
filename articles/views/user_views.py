import vanilla
from articles.forms import UserModeForm
from filter_views import FiltersMixin
import slick.views as slick
from accounts.views import UserUpdateView
from django.contrib.auth.models import User
import pytz

class ChangeMode(vanilla.FormView):
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

class Dashboard(FiltersMixin, slick.TemplateView):
  extra_context = {'heading':'Dashboard'}
  template_name = "articles/dashboard.html"

class UserSettingsView(FiltersMixin, UserUpdateView):
  model=User
  success_url="/user/settings/"
  template_name = "accounts/user_form.html"
  def form_valid(self, form, user_profile_form):
    # self.request.session['tz'] = user_profile_form.cleaned_data['timezone']
    self.request.session['django_timezone'] = pytz.timezone(user_profile_form.cleaned_data['timezone'])
    return super(UserSettingsView, self).form_valid(form, user_profile_form)
