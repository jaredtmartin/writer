from articles.models import *
from django.forms import ModelForm, DateField

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ('body',)
class ArticleEmployerForm(ModelForm):
    class Meta:
        model = Article
#        fields = ('body',)
