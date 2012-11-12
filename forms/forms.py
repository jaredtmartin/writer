from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from django.forms import ModelForm, BaseForm
from django.forms import Form as djForm
from django.forms.fields import *
from django.forms.widgets import *
from models import *
from django.template.defaultfilters import slugify
from django.forms.forms import BoundField
from widgets import SubmitWidget, LabelWidget, HeaderWidget
from django.core.validators import URLValidator, validate_email
from django.utils.datastructures import SortedDict
from countries import COUNTRIES
from django.core.exceptions import ValidationError
from extra_views import InlineFormSet

FormInlineFormSet = inlineformset_factory(Form, Element)

class FormModelForm(ModelForm):
    class Meta:
        model=Form
        exclude=('created_by',)
    def save(self, commit=True):
        obj = super(FormModelForm, self).save(commit=False)
        if self.request:
            r=self.request
            u=self.request.user
            a=self.request.user.is_anonymous()
            obj.created_by = self.request.user
        obj.save()
        return obj
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super(FormModelForm, self).__init__(*args, **kwargs)


def string_to_choices(s):
    l=s.split(",")
    choices=()
    for choice in l:
        c=(slugify(choice), choice)
        choices += (c,)
    return choices

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
    field.required_group=element.required_group
    return field
    
class BaseFormWithRequiredGroups(BaseForm):
    def clean(self):
        required_groups={}
        for key, field in self.fields.items():
            if field.required_group:
                if not field.required_group in required_groups.keys(): required_groups[field.required_group]=0
                if key in self.cleaned_data.keys() and self.cleaned_data[key]: required_groups[field.required_group]+=1
        for k,v in required_groups.items():
            if v==0: raise ValidationError(k)
        return self.cleaned_data
def make_form_class(form_instance):
    fields=SortedDict()
    hide_labels=[]
    for element in form_instance.elements.order_by('order'):
        fields[element.name] = get_field(element)
    form_class = type(str(slugify(form_instance.name)), (BaseFormWithRequiredGroups,), {'base_fields':fields})
    form_class.hide_labels = hide_labels
    return form_class
    
def make_form(form_instance, data=None):
    form = make_form_class(form_instance)(data)
    return form

class ElementForm(ModelForm):
    class Meta:
        model = Element
    order = CharField(widget=HiddenInput)
    
class ElementInline(InlineFormSet):
    model = Element
    form_class=ElementForm

