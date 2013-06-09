from articles.models import *
from django.forms import ModelForm, DateField, ValidationError, ChoiceField, IntegerField, Form, \
    ModelChoiceField, CharField, ModelMultipleChoiceField, widgets
from extra_views import InlineFormSet
from articles.widgets import SelectWithFlexibleOptionLabels, BootstrapDropdownWidget, BootstrapSplitDropdownWidget, BootstrapDropdownWidgetWithPlus
from django.utils.encoding import smart_unicode
import pytz
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

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ('writer','reviewer','writer_availability','reviewer_availability', 'language', 'style',  'purpose','price','referrals','expires','priority','category','tags', 'minimum','article_type','project','title','body', 'owner','number_of_articles','article_notes','review_notes','description')
    # lookup_field_names = {'project':'name'}
    # project = CharField(required=False)
    article_notes   = CharField(widget=widgets.Textarea(attrs={'class':'notes'}), required=False)
    review_notes    = CharField(widget=widgets.Textarea(attrs={'class':'notes'}), required=False)
    description     = CharField(widget=widgets.Textarea(attrs={'class':'notes'}), required=False)
    tags            = CharField(widget=widgets.TextInput(attrs={'style':'width:344px;height: 20px;'}), required=False)
    number_of_articles = IntegerField(required=False)
    project         = ModelChoiceField(queryset=Project.objects.all(), widget=BootstrapDropdownWidget(), empty_label='Select a Project')
    category        = ModelChoiceField(queryset=Category.objects.all(), widget=BootstrapDropdownWidget(), required=False, empty_label='Select a Category')
    article_type    = ModelChoiceField(queryset=ArticleType.objects.all(), widget=BootstrapDropdownWidget(), empty_label='Select a Content Type')
    priority        = ChoiceField(choices = ARTICLE_PRIORITIES, widget=BootstrapDropdownWidget(), required=False)
    
    # def clean_project(self):
    #     # Looksup project by name and creates it if it doesnt exist
    #     return self.clean_lookup('project', Project, auto_create=True)
    # def auto_create_related_object(self, data, field_name, model):
    #     # creates the new project with the user as owner
    #     return Project.objects.create(name=data, owner=self.user)
    def __init__(self, *args, **kwargs):
        # Recieves user from request
        self.user = kwargs.pop('user')
        # print "self.fields['project'] = %s" % str(self.fields['project'])
        # print "self.fields['article_type'] = %s" % str(self.fields['article_type'])
        super(ArticleForm, self).__init__(*args, **kwargs)
    def clean_title(self):
        data = self.cleaned_data['title']
        return titlecase(data)
        
class WriteArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ('title','body')    
    def __init__(self, *args, **kwargs):  
        self.user = kwargs.pop('user')
        super(WriteArticleForm, self).__init__(*args, **kwargs)

class KeywordInlineFormSet(InlineFormSet):
    model = Keyword
    extra = 1

class QuantityForm(Form):
    num = IntegerField(min_value=0)

class ActionUserID(Form):
    user = ModelChoiceField(queryset=User.objects.all())

class TagForm(Form):
    tags = CharField(max_length=128)

class RejectForm(Form):
    reason = CharField(max_length=128)

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
def get_timezone_choices():
        return [(t,t) for t in pytz.common_timezones]
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')
class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('preferred_mode','timezone')
    timezone = ChoiceField(choices=get_timezone_choices())
class TagArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ('tags',)
# class RelationshipForm(ModelForm):
#     class Meta:
#         model = Relationship
#         fields = ('requester','writer','reviewer')
# class ConfirmRelationshipForm(ModelForm):
#     class Meta:
#         model = Relationship
#         fields = ('confirmed',)
#     def save(self, commit=True):
#         super(ConfirmRelationshipForm, self).save(commit=False)
#         self.instance.confirmed=True
#         return super(ConfirmRelationshipForm, self).save(commit=True)
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields=('name',)
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProjectForm, self).__init__(*args, **kwargs)
    def save(self, commit=True):
        model = super(ProjectForm, self).save(commit=False)
        model.owner = self.user
        if commit: model.save()
        return model
class UserModeForm(Form):
    mode = IntegerField(min_value=1, max_value=3)
    next = CharField(max_length=128, required=False)
