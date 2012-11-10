from knowledge.models import Question, Response, Category, Article
from django.forms import ModelForm

#class ModelFormWithRequest(ModelForm):
#    def __init__(self, *args, **kwargs):
#        self.request=kwargs.pop('request',None)
#        super(ModelFormWithRequest, self).__init__(*args, **kwargs)
#        return form

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        exclude=('user',)
        
    def remove_fields(self, list_to_remove):
        for k in self.fields.keys(): 
            if k in list_to_remove: 
                del self.fields[k]
                
    def __init__(self, *args, **kwargs):
        self.request=kwargs.pop('request',None) 
        print "self.request" + str(self.request)        
        self.user = getattr(self.request, 'user',None)
        super(QuestionForm, self).__init__(*args, **kwargs)
        if getattr(self.user,'is_anonymous',False):
            self.remove_fields(['locked','status'])
        else:
            if getattr(self.user,'is_staff',False):
                self.remove_fields(['name','email'])
            else:
                self.remove_fields(['name','email','locked','status'])
        
class QuestionFormUnAuth(ModelForm):
    class Meta:
        model = Question
        exclude = ('status','locked','user')
        
class QuestionFormUser(ModelForm):
    class Meta:
        model = Question
        exclude = ('status','locked','user','email','name')
        
class QuestionFormAdmin(ModelForm):
    class Meta:
        model = Question
        exclude = ('user','email','name')

class ResponseForm(ModelForm):
    class Meta:
        model = Response
    
