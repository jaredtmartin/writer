from django.forms.formsets import formset_factory
from django.forms import ModelForm, BaseForm
from django.forms import Form as djForm
from django.forms.fields import *
from django.forms.widgets import *
from models import *
from django.template.defaultfilters import slugify
from django.forms.forms import BoundField
from widgets import SubmitWidget, LabelWidget, HeaderWidget
from django.core.validators import URLValidator, validate_email
from countries import COUNTRIES

class SimpleForm(djForm):
    name=CharField(max_length=64)
    
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

def get_field(element):
    if element.unique: unique_validator=[UniqueValidatorCreator(element),]
    else: unique_validator=[]
    if element.klass == Element.TEXTBOX: 
        field = CharField(
            max_length = 128, 
            required = element.required,
            validators=unique_validator,
            widget = TextInput(attrs={'title':element.tooltip}),
        )
    elif element.klass == Element.URL: 
        validate_url = URLValidator()
        field = CharField(
            max_length = 128, 
            required = element.required, 
            validators=unique_validator+[validate_url],
            widget = TextInput(attrs={'title':element.tooltip}),
            
        )
    elif element.klass == Element.EMAIL: 
        field = CharField(
            max_length = 128, 
            required = element.required, 
            validators=unique_validator+[validate_email],
            widget = TextInput(attrs={'title':element.tooltip}),
        )
    elif element.klass == Element.TEXTAREA: 
        field = CharField(
            max_length = 128, 
            required = element.required, 
            widget=Textarea(attrs={'title':element.tooltip}),
            validators=unique_validator,
        )
    elif element.klass == Element.PASSWORD: 
        field = CharField(
            max_length = 128, 
            required = element.required, 
            widget=PasswordInput(attrs={'title':element.tooltip}),
            validators=unique_validator,
        )
    elif element.klass == Element.DROPDOWN: 
        field = ChoiceField(
            required = element.required, 
            choices=string_to_choices(element.details),
            validators=unique_validator,
        )
    elif element.klass == Element.RADIO: 
        field = ChoiceField(
            required = element.required, 
            choices=string_to_choices(element.details),
            widget=RadioSelect(attrs={'title':element.tooltip}),
            validators=unique_validator,
        )
    elif element.klass == Element.CHECKBOX: 
        field = BooleanField(
            required = element.required,
            validators=unique_validator,
        )
    elif element.klass == Element.SUBMIT: 
        field = CharField(
            required = False,
            widget = SubmitWidget,
            validators=unique_validator,
        )
    elif element.klass == Element.HEADER: 
        field = CharField(
            required = False,
            widget = HeaderWidget,
            validators=unique_validator,
        )
    elif element.klass == Element.COUNTRY: 
        field = ChoiceField(
            required = element.required, 
            choices=COUNTRIES,
            validators=unique_validator,
        )
    field.klass=element.klass
    if element.klass in [Element.HEADER, Element.SUBMIT]: field.show_label=False
    else: field.show_label=True
    field.description=element.description
    return field
def make_form_class(form_instance):
    fields={}
    hide_labels=[]
    for element in form_instance.elements.all():
        fields[element.name] = get_field(element)
#        if element.klass in [Element.HEADER, Element.SUBMIT]: hide_labels.append(fields[element.name].label_tag)
    form = type(str(slugify(form_instance.name)), (BaseForm,), {'base_fields':fields})
    form.hide_labels = hide_labels
    return form
    
def make_form(form_instance, data=None):
    form = make_form_class(form_instance)(data)
    return form

