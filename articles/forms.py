from articles.models import *
from django.forms import ModelForm, DateField, ValidationError, BooleanField, ChoiceField, IntegerField, Form, \
    ModelChoiceField, CharField, ModelMultipleChoiceField, widgets, RegexField, PasswordInput
from extra_views import InlineFormSet
from articles.widgets import BootstrapDropdown, BootstrapDropdownPlus
from django.utils.encoding import smart_unicode
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from titlecase import titlecase

class FormWithLookupsMixin(object):
    lookup_field_names={}
    def auto_create_related_object(self, data, field_name, model):
        lookup_field=self.lookup_field_names[field_name]
        return model.objects.create(**{lookup_field:data})

    def fetch_object_from_lookup(self, data, field_name, model):
        lookup_field=self.lookup_field_names[field_name]
        return model.objects.filter(**{lookup_field:data}).get()

    def clean_lookup(self, name, model, by_pk=False, title=None, auto_create=False):
        if not title: title=name
        data = self.cleaned_data[name]
        if (not data) and (not self.fields[name].required): return None
        try: return self.fetch_object_from_lookup(data, name, model)
        except model.MultipleObjectsReturned: 
            raise ValidationError('There are more than one %ss with the name %s. Resolve this issue and try again.' % (title, data))
        except model.DoesNotExist: 
            if auto_create: return self.auto_create_related_object(data, name, model)
            else: raise ValidationError('Unable to find %s in the list of %ss.' % (data, title))
class CreateArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ('language', 'style', 'purpose','price','referrals','expires','priority','category','tags', 'minimum','article_type','project','title','body', 'owner','number_of_articles','article_notes','review_notes','description')
    # lookup_field_names = {'project':'name'}
    # project = CharField(required=False)
    article_notes   = CharField(widget=widgets.Textarea(attrs={'class':'notes boxsizingBorder','placeholder':'Notes to writer...','class':'form-control'}), required=False)
    review_notes    = CharField(widget=widgets.Textarea(attrs={'class':'notes boxsizingBorder','placeholder':'Notes to reviewer...','class':'form-control'}), required=False)
    description     = CharField(widget=widgets.Textarea(attrs={'class':'notes boxsizingBorder','placeholder':'Add description...','class':'form-control'}), required=False)
    number_of_articles = IntegerField(required=False, widget=widgets.TextInput(attrs={'placeholder':'Number of Articles: One','class':'form-control'}))
    project         = ModelChoiceField(queryset=Project.objects.all(), widget=BootstrapDropdownPlus(label="Project", plus_url="www.google.com", help_text='Select a project or start a new one.', attrs={'class':'article-select form-control', 'data-style':"btn-primary"}), required=False)
    category        = ModelChoiceField(queryset=Category.objects.all(), widget=BootstrapDropdownPlus(label="Category", plus_url="www.google.com", help_text='Select a category for your article(s).', attrs={'data-style':"btn-primary",'class':'form-control'}), required=False)
    article_type    = ModelChoiceField(queryset=ArticleType.objects.all(), widget=BootstrapDropdown(label="Type", plus_url="www.google.com", help_text='Select the type of content you want written.', attrs={'data-style':"btn-primary",'class':'form-control'}), initial='0')
    priority        = ChoiceField(choices = ARTICLE_PRIORITIES, widget=BootstrapDropdown(label="Priority", help_text='How urgent is/are the article(s)?', attrs={'data-style':"btn-primary",'class':'form-control'}), required=False)
    minimum         = CharField(initial="", widget=widgets.TextInput(attrs={'class':'high-input', 'placeholder':'Length:100','class':'form-control'}), required=False)
    expires         = DateField(initial="", widget=widgets.DateTimeInput(attrs={'placeholder':'Expires: Never','class':'form-control'}), required=False)
    tags            = CharField(initial="", widget=widgets.TextInput(attrs={'placeholder':'Tags','class':'form-control'}), required=False)
    referrals       = CharField(initial="", widget=widgets.TextInput(attrs={'placeholder':'Referrals','class':'form-control'}), required=False)
    language        = CharField(initial="", widget=widgets.TextInput(attrs={'placeholder':'Language','class':'form-control'}), required=False)
    style           = CharField(initial="", widget=widgets.TextInput(attrs={'placeholder':'Style','class':'form-control'}), required=False)
    purpose         = CharField(initial="", widget=widgets.TextInput(attrs={'placeholder':'Purpose','class':'form-control'}), required=False)
    price           = CharField(initial="", widget=widgets.TextInput(attrs={'placeholder':'Price','class':'form-control'}), required=False)

    # def clean_project(self):
    #     # Looksup project by name and creates it if it doesnt exist
    #     return self.clean_lookup('project', Project, auto_create=True)
    # def auto_create_related_object(self, data, field_name, model):
    #     # creates the new project with the user as owner
    #     return Project.objects.create(name=data, owner=self.user)
    def clean_minimum(self):
        if self.cleaned_data.get('minimum'):
            try:
                return int(self.cleaned_data['minimum'].strip())
            except ValueError:
                raise ValidationError("Invalid number")
        return 100
    def __init__(self, *args, **kwargs):
        # Recieves user from request
        self.user = kwargs.pop('user')
        # print "self.fields['project'] = %s" % str(self.fields['project'])
        # print "self.fields['article_type'] = %s" % str(self.fields['article_type'])
        super(CreateArticleForm, self).__init__(*args, **kwargs)
    def clean_title(self):
        data = self.cleaned_data['title']
        return titlecase(data)
class ArticleForm(CreateArticleForm):
    class Meta:
        model = Article
        fields = ('writer','reviewer','language', 'style',  'purpose','price','referrals','expires','priority','category','tags', 'minimum','article_type','project','title','body', 'owner','number_of_articles','article_notes','review_notes','description')
    title = CharField(initial="", widget=widgets.TextInput(attrs={'placeholder':'Title','class':'form-control'}), required=False)
class WriteArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ('title','body')    
    def __init__(self, *args, **kwargs):  
        self.user = kwargs.pop('user')
        super(WriteArticleForm, self).__init__(*args, **kwargs)

class KeywordForm(ModelForm):
    class Meta:
        model = Keyword
    keyword = CharField(widget=widgets.TextInput(attrs={'class':'form-control'}), required=False)
    url = CharField(widget=widgets.TextInput(attrs={'class':'form-control'}), required=False)
    times = CharField(widget=widgets.TextInput(attrs={'class':'form-control'}), required=False)


class KeywordInlineFormSet(InlineFormSet):
    # This is old and deprecated
    model = Keyword
    form_class = KeywordForm
    extra = 1
class KeywordInline(InlineFormSet):
    model = Keyword
    form_class = KeywordForm

class QuantityForm(Form):
    num = IntegerField(min_value=0)

class ActionUserID(Form):
    user = ModelChoiceField(queryset=User.objects.all())

class SimpleTextForm(Form):
    name = CharField(max_length=64)

class TagForm(Form):
    tags = CharField(max_length=128)

class RejectForm(Form):
    reason = CharField(max_length=128)
    return_to_writer = BooleanField(required=False)

class PublishForm(Form):
    outlet = ModelChoiceField(queryset=PublishingOutlet.objects.all())

class NoteForm(Form):
    note = CharField(max_length=128)

class ModelChoiceFieldWithFlexibleChoiceLabels(ModelChoiceField):
    def __init__(self, queryset, empty_label=u"---------", cache_choices=False,
                 required=True, widget=None, label=None, initial=None,
                 help_text=None, to_field_name=None, *args, **kwargs):
        self.pre_label=kwargs.pop('pre_label','')
        self.post_label=kwargs.pop('post_label','')
        return super(ModelChoiceFieldWithFlexibleChoiceLabels, self).__init__(queryset, empty_label, cache_choices,
                 required, widget, label, initial,
                 help_text, to_field_name, *args, **kwargs)
    def label_from_instance(self, obj):
        return smart_unicode(self.pre_label+smart_unicode(obj).title()+self.post_label)
        
class ModelChoiceFieldTitleLabels(ModelChoiceField):
    def label_from_instance(self, obj):
        return smart_unicode(obj).title()
    
class AssignToForm(Form):
#    assign_to_user = ModelChoiceFieldWithFlexibleChoiceLabels(queryset=User.objects.all(), pre_label="Assign to ")
    user = ModelChoiceFieldTitleLabels(queryset=User.objects.all(), empty_label="Assign select articles to:")

class TagArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ('tags',)

class FormWithUserMixin(object):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(FormWithUserMixin, self).__init__(*args, **kwargs)
class ModelFormWithUser(FormWithUserMixin, ModelForm):
    def save(self, commit=True):
        model = super(ModelFormWithUser, self).save(commit=False)
        model.owner = self.user
        if commit: model.save()
        return model

class ContactForm(FormWithUserMixin, ModelForm):
  class Meta:
    model = Contact
    fields = ('requester','user_asked')
  def clean(self):
    cleaned_data = self.cleaned_data
    # Figure out who is being asked and save with the object
    if cleaned_data['requester'] == self.user:
      cleaned_data['user_asked'] = cleaned_data['worker']
    else:
      cleaned_data['user_asked'] = cleaned_data['requester']
    # Always return the full collection of cleaned data.
    return cleaned_data

# class ConfirmContactForm(ModelForm):
#     class Meta:
#         model = Contact
#         fields = ('confirmation',)
#     def save(self, commit=True):
#         super(ConfirmContactForm, self).save(commit=False)
#         self.instance.confirmation=True
#         return super(ConfirmContactForm, self).save(commit=True)

class ProjectForm(ModelFormWithUser):
    class Meta:
        model = Project
        fields=('name',)
class CategoryForm(ModelFormWithUser):
    class Meta:
        model = Category
        fields=('name',)

class UserModeForm(Form):
    mode = IntegerField(min_value=1, max_value=3)
    next = CharField(max_length=128, required=False)

class GroupMemberForm(Form):
  contact = ModelChoiceField(queryset=Contact.objects.all())
class NewGroupForm(ModelForm):
  class Meta:
    model = ContactGroup
    fields=('name',)
class RenameGroupForm(ModelForm):
  class Meta:
    model = ContactGroup
    fields=('name',)

class FiltersForm(Form):
    filters = CharField(max_length=128, required=False)
class RegistrationForm(UserCreationForm):
    username = RegexField(label="Username", max_length=30,
        widget=widgets.TextInput(attrs={'placeholder':'Username'}),
        regex=r'^[\w.@+-]+$',
        help_text = "Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only.",
        error_messages = {
            'invalid': "This value may contain only letters, numbers and "
                         "@/./+/-/_ characters."})
    password1 = CharField(label="Password", 
        widget=PasswordInput(attrs={'placeholder':'Password','class':'form-control'}))
    password2 = CharField(label="Password confirmation",
        widget=PasswordInput(attrs={'placeholder':'Please re-type your password','class':'form-control'}),
        help_text = "Enter the same password as above, for verification.")
    first_name = CharField(label="First Name", max_length=30,
        widget=widgets.TextInput(attrs={'placeholder':'First Name','class':'form-control'}))
    last_name = CharField(label="Last Name", max_length=30,
        widget=widgets.TextInput(attrs={'placeholder':'Last Name','class':'form-control'}))
    class Meta:
        model = User
        fields = ("username","first_name","last_name")
class LoginForm(AuthenticationForm):
    username = CharField(label="Username", max_length=30,
        widget=widgets.TextInput(attrs={'placeholder':'Username','class':'form-control'}))
    password = CharField(label="Password", 
        widget=PasswordInput(attrs={'placeholder':'Password','class':'form-control'}))