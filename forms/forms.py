from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from django.forms import ModelForm, BaseForm
from django.forms import Form as djForm
from django.forms.fields import *
from django.forms.widgets import *
from models import *
from django.template.defaultfilters import slugify
from django.forms.forms import BoundField
from widgets import SubmitWidget, LabelWidget, HeaderWidget, ImageWidget
from django.core import validators
from django.utils.datastructures import SortedDict
from countries import COUNTRIES
from django.core.exceptions import ValidationError
from extra_views import InlineFormSet
import re
from django.utils.translation import ugettext_lazy as _

FormInlineFormSet = inlineformset_factory(Form, Element)
        
class BareFormModelForm(ModelForm):
    class Meta:
        model=Form
        fields=('id',)

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
        field = URLField(
            max_length = 128, 
            required = element.required, 
            validators=unique_validator, 
            widget = TextInput(attrs={'title':element.tooltip}),
            
        )
    elif element.klass == Element.EMAIL: 
        field = CharField(
            max_length = 128, 
            required = element.required, 
            validators=unique_validator+[validators.validate_email],
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
    elif element.klass == Element.TEXT: 
        field = CharField(
            required = False,
            widget = LabelWidget(text=element.details),
        )
    elif element.klass == Element.IMAGE: 
        if element.image: filename=element.image.url 
        else: filename=''
        field = CharField(
            required = False,
            widget = ImageWidget(filename=filename, label_position=''),
        )
    elif element.klass == Element.IMAGELEFT: 
        if element.image: filename=element.image.url 
        else: filename=''
        field = CharField(
            required = False,
            widget = ImageWidget(filename=filename, label_position='right'),
        )
    elif element.klass == Element.IMAGERIGHT: 
        if element.image: filename=element.image.url 
        else: filename=''
        field = CharField(
            required = False,
            widget = ImageWidget(filename=filename, label_position='left'),
        )
    field.klass=element.klass
    if element.klass in [Element.HEADER, Element.SUBMIT, Element.TEXT, Element.IMAGE, Element.IMAGERIGHT, Element.IMAGELEFT]: field.show_label=False
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
        exclude=('description','required_group')
#    order = CharField(widget=HiddenInput)
#    klass = ChoiceField(widget=HiddenInput)
#    required = BooleanField(widget=HiddenInput)
#    unique = BooleanField(widget=HiddenInput)
#    name = CharField(widget=TextInput(attrs={'class':'hintTextbox'}))
    
class ElementInline(InlineFormSet):
    model = Element
    form_class=ElementForm
    extra=0
    
class NameAndThemeForm(ModelForm):
    class Meta:
        model=Form
        fields=('name', 'theme')
    theme = CharField(widget=HiddenInput)
    def save(self, commit=True):
        obj = super(NameAndThemeForm, self).save(commit=False)
        if self.request:
            r=self.request
            u=self.request.user
            a=self.request.user.is_anonymous()
            obj.created_by = self.request.user
        obj.save()
        return obj
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super(NameAndThemeForm, self).__init__(*args, **kwargs)
class ShareForm(ModelForm):
    class Meta:
        model=Form
        fields=('email',)
