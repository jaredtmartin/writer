from articles.models import *
from django.forms import ModelForm, DateField, IntegerField, Form, ModelChoiceField, CharField
from extra_views import InlineFormSet
from articles.widgets import SelectWithFlexibleOptionLabels
from django.utils.encoding import smart_unicode


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ('minimum','maximum','article_type','project','title','body', 'owner')
#        ['minimum', 'maximum', 'body', 'title', 'article_type', 'project', 'tags', 'owner', 'last_action', 'published', 'approved', 'submitted', 'assigned', 'rejected', 'released']
        
class KeywordInlineFormSet(InlineFormSet):
    model = Keyword
    extra=0

class KeywordInlineForm(Form):
    num = IntegerField(min_value=0)

class ActionUserID(Form):
    user = ModelChoiceField(queryset=User.objects.all())

class TagForm(Form):
    tag = CharField(max_length=128)

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
    assign_to_user = ModelChoiceFieldTitleLabels(queryset=User.objects.all(), empty_label="Assign select articles to:")

    
