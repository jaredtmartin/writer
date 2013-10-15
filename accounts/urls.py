from django.conf.urls.defaults import *
from views import UserUpdateView
from forms import LoginForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm

urlpatterns = patterns('',
  # url(r'^settings/$', UserUpdateView.as_view(), name="user_settings"),
  url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html','authentication_form':LoginForm}, name='login'),
  url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'accounts/logged_out.html'}, name='logout'),
  url(r'^password_change/$', 'django.contrib.auth.views.password_change', {'template_name': 'accounts/password_change_form.html', 'password_change_form':PasswordChangeForm}, name='change_password'),
  url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'accounts/password_change_done.html'}, name='password_change_done'),
  url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', 
      {'template_name': 'accounts/password_reset_form.html', 'email_template_name': 'accounts/password_reset_email.html', 'password_reset_form':PasswordResetForm}, 
      name='password_reset'),
  url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'accounts/password_reset_done.html'}, name='password_reset_done'),
  url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'accounts/password_reset_confirm.html', 'set_password_form':SetPasswordForm}, name='password_reset_confirm'),
  url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'accounts/password_reset_complete.html'}, name='password_reset_complete'),
  url(r'^signup/$', 'accounts.views.signup', 
      {'template_name': 'accounts/signup_form.html', 'email_template_name': 'accounts/signup_email.html'}, name='signup'),
  url(r'^signup/done/$', 'accounts.views.signup_done', {'template_name': 'accounts/signup_done.html'}, name='signup_done'),
  url(r'^signup/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'accounts.views.signup_confirm'),
  url(r'^signup/complete/$', 'accounts.views.signup_complete', {'template_name': 'accounts/signup_complete.html'}, name='signup_complete'),
)