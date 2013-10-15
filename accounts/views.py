from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from accounts.forms import UserForm, UserProfileForm, SimpleUserCreationFormWithFullName
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from django.utils.http import urlquote, base36_to_int
from django.contrib.sites.models import Site
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages


from django.views.decorators.csrf import csrf_protect

@csrf_protect
def signup(request, template_name='registration/signup.html', 
           email_template_name='registration/signup_email.html',
           signup_form=SimpleUserCreationFormWithFullName,
           token_generator=default_token_generator,
           post_signup_redirect=None):
    if post_signup_redirect is None:
        post_signup_redirect = reverse('signup_done')
    if request.method == "POST":
        form = signup_form(request.POST)
        if form.is_valid():
            opts = {}
            opts['use_https'] = request.is_secure()
            opts['token_generator'] = token_generator
            opts['email_template_name'] = email_template_name
            if not Site._meta.installed:
                opts['domain_override'] = RequestSite(request).domain
            form.save(**opts)
            return HttpResponseRedirect(post_signup_redirect)
    else:
        form = signup_form()
    return render_to_response(template_name, {'form': form,}, 
                              context_instance=RequestContext(request))

def signup_done(request, template_name='registration/signup_done.html'):
    return render_to_response(template_name, 
                              context_instance=RequestContext(request))

def signup_confirm(request, uidb36=None, token=None,
                   token_generator=default_token_generator,
                   post_signup_redirect=None):
    assert uidb36 is not None and token is not None #checked par url
    if post_signup_redirect is None:
        post_signup_redirect = reverse('signup_complete')
    try:
        uid_int = base36_to_int(uidb36)
    except ValueError:
        raise Http404

    user = get_object_or_404(User, id=uid_int)
    context_instance = RequestContext(request)

    if token_generator.check_token(user, token):
        context_instance['validlink'] = True
        user.is_active = True
        user.save()
    else:
        context_instance['validlink'] = False
    return HttpResponseRedirect(post_signup_redirect)

def signup_complete(request, template_name='registration/signup_complete.html'):
    return render_to_response(template_name, 
                              context_instance=RequestContext(request, 
                                                              {'login_url': settings.LOGIN_URL}))

class UserUpdateView(UpdateView):
  model=User
  form_class = UserForm
  def get_object(self, queryset=None):
        return self.request.user
  def get_context_data(self, **kwargs):
    kwargs.update({
      'user_profile_form':UserProfileForm(instance=self.object.get_profile()),
    })
    return super(UserUpdateView, self).get_context_data(**kwargs)
  def form_invalid(self, form, user_profile_form):
    return self.render_to_response(self.get_context_data(form=form, user_profile_form=user_profile_form))
  def form_valid(self, form, user_profile_form):
    user_profile_form.save()
    messages.success(self.request, 'The changes to your profile have been made successfully.')
    return super(UserUpdateView, self).form_valid(form)
  def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    form_class = self.get_form_class()
    form = self.get_form(form_class)
    user_profile_form = UserProfileForm(self.request.POST, instance=self.object.get_profile())
    if form.is_valid() and user_profile_form.is_valid():
      return self.form_valid(form, user_profile_form)
    else:
      return self.form_invalid(form, user_profile_form)