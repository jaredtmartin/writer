from django.forms.formsets import formset_factory
from django.forms import ModelForm, BaseForm
from django.forms.fields import *
from django.forms.widgets import *
from models import *
from django.template.defaultfilters import slugify
from django.forms.forms import BoundField
from widgets import SubmitWidget
from django.core.validators import URLValidator


class ElementForm(ModelForm):
    class Meta:
        model = Element

ElementFormSet = formset_factory(ElementForm)

def string_to_choices(s):
    l=s.split(",")
    choices=()
    for choice in l:
        c=(slugify(choice), choice)
        choices += (c,)
    return choices

from django.core.exceptions import ValidationError

class UniqueValidatorBase(object):
    def __init__(self, value):
        if Value.objects.filter(element=self.element, value=value).count() > 0:
            raise ValidationError(u'%s has already been used. Please use a unique %s.' % (value,self.element.name.lower()))
        else: return None
            
def UniqueValidatorCreator(element):
    return type(str(slugify('unique_'+element.form.name+"_"+element.name)), (UniqueValidatorBase,), {'element':element})

def make_form_class(form_instance):
    fields={}
    for element in form_instance.elements.all():
        if element.unique: unique_validator=[UniqueValidatorCreator(element),]
        else: unique_validator=[]
        if element.klass == Element.TEXTBOX: 
            fields[element.name] = CharField(
                max_length = 128, 
                required = element.required,
                validators=unique_validator,
            )
        elif element.klass == Element.URL: 
            validate_url = URLValidator()
            validate_url.message='Please enter a valid URL ie:"http://www.mysite.com/"'
            fields[element.name] = CharField(
                max_length = 128, 
                required = element.required, 
                validators=unique_validator+[validate_url]
            )
        elif element.klass == Element.TEXTAREA: 
            fields[element.name] = CharField(
                max_length = 128, 
                required = element.required, 
                widget=Textarea,
                validators=unique_validator,
            )
        elif element.klass == Element.PASSWORD: 
            fields[element.name] = CharField(
                max_length = 128, 
                required = element.required, 
                widget=PasswordInput,
                validators=unique_validator,
            )
        elif element.klass == Element.DROPDOWN: 
            fields[element.name] = ChoiceField(
                required = element.required, 
                choices=string_to_choices(element.details),
                validators=unique_validator,
            )
        elif element.klass == Element.RADIO: 
            fields[element.name] = ChoiceField(
                required = element.required, 
                choices=string_to_choices(element.details),
                widget=RadioSelect,
                validators=unique_validator,
            )
        elif element.klass == Element.CHECKBOX: 
            fields[element.name] = BooleanField(
                required = element.required,
                validators=unique_validator,
            )
        elif element.klass == Element.SUBMIT: 
            fields[element.name] = CharField(
                required = False,
                widget = SubmitWidget,
                validators=unique_validator,
            )
        elif element.klass == Element.HEADER: 
            fields[element.name] = CharField(
                required = False,
                widget = LabelWidget,
                validators=unique_validator,
            )
    return type(str(slugify(form_instance.name)), (BaseForm,), {'base_fields':fields})
    
def make_form(form_instance, data=None):
    form = make_form_class(form_instance)(data)
    return form

