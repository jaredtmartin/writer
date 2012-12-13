from articles.models import *
from django.forms import ModelForm, DateField, IntegerField, Form
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
