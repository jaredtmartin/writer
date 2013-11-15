from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import forms as django_forms
from django.utils.http import int_to_base36
from articles.widgets import BootstrapDropdown
from django.forms import widgets
from django.template import Context, loader
from django.conf import settings
from django import forms
import pytz
from django.core.mail import send_mail
from django.forms import ModelForm, ChoiceField
from articles.models import UserProfile, USER_MODES
class SimpleUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control'}))
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput(attrs={'placeholder':'Retype Password','class':'form-control'}),
                                help_text = "Enter the same password as above, for verification.")
    email = forms.EmailField(label="Email", max_length=75, widget=widgets.TextInput(attrs={'placeholder':'E-mail address','class':'form-control'}))

    class Meta:
        model = User
        fields = set()

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2
    
    def clean_email1(self):
        email = self.cleaned_data["email"]
        users_found = User.objects.filter(email__iexact=email)
        if len(users_found) >= 1:
            raise forms.ValidationError("A user with that email already exist.")
        return email

    def save(self, commit=True, domain_override=None,
             email_template_name='registration/signup_email.html',
             use_https=False, token_generator=default_token_generator):
        user = super(SimpleUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]
        user.is_active = False
        if commit:
            user.save()
        if not domain_override:
            current_site = Site.objects.get_current()
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        t = loader.get_template(email_template_name)
        c = {
            'email': user.email,
            'domain': domain,
            'site_name': site_name,
            'uid': int_to_base36(user.id),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': use_https and 'https' or 'http',
            }
        send_mail("Confirmation link sent on %s" % site_name,
                  t.render(Context(c)), settings.EMAIL_HOST_USER, [user.email])
        return user
class SimpleUserCreationFormWithFullName(SimpleUserCreationForm):
    class Meta:
        model = User
        fields = ("first_name","last_name")
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(attrs={'placeholder':'First Name','class':'form-control'}))
    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(attrs={'placeholder':'Last Name','class':'form-control'}))

# class UserCreationForm(forms.ModelForm):
#     username = forms.RegexField(label="Username", max_length=30, regex=r'^[\w.@+-]+$',
#                                 help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
#                                 error_messages = {'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."})
#     password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
#     password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput,
#                                 help_text = "Enter the same password as above, for verification.")
#     email1 = forms.EmailField(label="Email", max_length=75)
#     email2 = forms.EmailField(label="Email confirmation", max_length=75,
#                               help_text = "Enter your email address again. A confirmation email will be sent to this address.")

#     class Meta:
#         model = User
#         fields = ("username",)

#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1", "")
#         password2 = self.cleaned_data["password2"]
#         if password1 != password2:
#             raise forms.ValidationError("The two password fields didn't match.")
#         return password2
    
#     def clean_email1(self):
#         email1 = self.cleaned_data["email1"]
#         users_found = User.objects.filter(email__iexact=email1)
#         if len(users_found) >= 1:
#             raise forms.ValidationError("A user with that email already exist.")
#         return email1

#     def clean_email2(self):
#         email1 = self.cleaned_data.get("email1", "")
#         email2 = self.cleaned_data["email2"]
#         if email1 != email2:
#             raise forms.ValidationError("The two email fields didn't match.")
#         return email2

#     def save(self, commit=True, domain_override=None,
#              email_template_name='registration/signup_email.html',
#              use_https=False, token_generator=default_token_generator):
#         user = super(UserCreationForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         user.email = self.cleaned_data["email1"]
#         user.is_active = False
#         if commit:
#             user.save()
#         if not domain_override:
#             current_site = Site.objects.get_current()
#             site_name = current_site.name
#             domain = current_site.domain
#         else:
#             site_name = domain = domain_override
#         t = loader.get_template(email_template_name)
#         c = {
#             'email': user.email,
#             'domain': domain,
#             'site_name': site_name,
#             'uid': int_to_base36(user.id),
#             'user': user,
#             'token': token_generator.make_token(user),
#             'protocol': use_https and 'https' or 'http',
#             }
#         send_mail("Confirmation link sent on %s" % site_name,
#                   t.render(Context(c)), 'peyman.gohari@gmail.com', [user.email])
#         return user

def get_timezone_choices():
        return [(t,t) for t in pytz.common_timezones]
class UserForm(ModelForm):
  class Meta:
    model = User
    fields = ('first_name','last_name','email')
  first_name = forms.CharField(widget=widgets.TextInput(attrs={'placeholder':'First', 'class':'form-control'}), required=False)
  last_name = forms.CharField(widget=widgets.TextInput(attrs={'placeholder':'Last', 'class':'form-control'}), required=False)
  email = forms.CharField(widget=widgets.TextInput(attrs={'placeholder':'Email', 'class':'form-control'}), required=False)

class UserProfileForm(ModelForm):
  class Meta:
    model = UserProfile
    fields = ('mode','timezone')
  timezone = ChoiceField(choices=get_timezone_choices(), widget=forms.Select(attrs={'class':'selectpicker primary'}))
  mode = ChoiceField(choices=USER_MODES, widget=forms.Select(attrs={'class':'selectpicker primary'}))

class LoginForm(django_forms.AuthenticationForm):
    username = forms.CharField(label="E-mail", max_length=30, widget=widgets.TextInput(attrs={'placeholder':'E-mail address','class':'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control'}))
class PasswordResetForm(django_forms.PasswordResetForm):
    email = forms.EmailField(label="E-mail", max_length=75, widget=widgets.TextInput(attrs={'placeholder':'E-mail address','class':'form-control'}))
class SetPasswordForm(django_forms.SetPasswordForm):
    new_password1 = forms.CharField(label="New password",
                                    widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control'}))
    new_password2 = forms.CharField(label="New password confirmation",
                                    widget=forms.PasswordInput(attrs={'placeholder':'Retype Password','class':'form-control'}))
class PasswordChangeForm(django_forms.PasswordChangeForm):
    new_password1 = forms.CharField(label="New password",
                                    widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control'}))
    new_password2 = forms.CharField(label="New password confirmation",
                                    widget=forms.PasswordInput(attrs={'placeholder':'Retype Password','class':'form-control'}))
    old_password = forms.CharField(label="Old password",
                                   widget=forms.PasswordInput(attrs={'placeholder':'Old Password','class':'form-control'}))

