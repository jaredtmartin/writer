from articles.models import *
from django.forms import ModelForm, DateField, IntegerField, Form, ModelChoiceField, CharField
from extra_views import InlineFormSet

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ('body',)
        
class ArticleEmployerForm(ModelForm):
    class Meta:
        model = Article
        
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
