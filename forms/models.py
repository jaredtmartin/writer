from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Theme(models.Model):
    name = models.CharField('Name', max_length=32)
    code = models.TextField()
    def __unicode__(self): return self.name
    
class Form(models.Model):
    name = models.CharField('Name', max_length=32)
    success_url = models.CharField('Success URL', max_length=64, default='thankyou/')
    submit_label = models.CharField('Submit Label', max_length=32, default='Submit')
    created_by = models.ForeignKey(User)
    theme = models.ForeignKey(Theme)
    def __unicode__(self): return self.name
    @models.permalink
    def get_absolute_url(self):
        return ('form', [self.id, slugify(self.name)])
    @models.permalink
    def get_edit_url(self):
        return ('edit', [self.id, slugify(self.name)])
    
class Element(models.Model):
    HEADER = 'HD'
    TEXT = 'TX'
    IMAGE = 'IM'
    IMAGERIGHT = "IR"
    IMAGELEFT = "IL"
    TEXTBOX = 'TB'
    PASSWORD = "PB"
    TEXTAREA = 'TA'
    DROPDOWN = 'DD'
    RADIO = 'RD'
    CHECKBOX = "CB"
    FILEUPLOAD = 'FU'
    SUBMIT = 'SB'
    URL = 'UL'
    COUNTRY ='CT'
    EMAIL = 'EM'
    ELEMENT_TYPE_CHOICES = (
        (HEADER, 'Header'),
        (TEXTBOX, 'Text Box'),
        (PASSWORD, 'Password Box'),
        (TEXTAREA, 'Text Area'),
        (DROPDOWN, 'Drop-down box'),
        (RADIO, 'Radio Buttons'),
        (CHECKBOX, 'Checkbox'),
        (FILEUPLOAD, 'File Upload'),
#        (SUBMIT, 'Submit'),
        (URL, 'URL'),
        (COUNTRY,'Country'),
        (EMAIL,'Email Address'),
        (TEXT, 'Text'),
        (IMAGE,'Image'),
        (IMAGELEFT,'Image on Left with Text on Right'),
        (IMAGERIGHT,'Image on Right with Text on Left'),
    )
    name = models.CharField('Name', max_length=32)
    klass = models.CharField('Type', max_length=2, choices = ELEMENT_TYPE_CHOICES, default=TEXTBOX)
    required = models.BooleanField(default=False, blank=True)
    unique = models.BooleanField(default=False, blank=True)
    description = models.CharField('Description', max_length=64, default="", blank=True)
    tooltip = models.CharField('Tooltip', max_length=64, default="", blank=True)
    order = models.IntegerField(blank=True, default=1)
    image = models.ImageField(upload_to='forms/images/', blank=True)
    details = models.CharField('Choices', max_length=128, blank=True, default="")
    form = models.ForeignKey(Form, related_name='elements')
    required_group = models.CharField(blank=True, default=None, null=True, max_length=64)
    class Meta:
        ordering = ('order', '-id', )
    def __unicode__(self): return self.name
    @property
    def uses_image(self):
        return self.klass[0]=="I"

class Result(models.Model):
    form = models.ForeignKey(Form, related_name='results')
    created_at = models.DateTimeField(auto_now_add=True)
    @models.permalink
    def get_absolute_url(self):
        return ('result', [self.id, slugify(self.name)])
        
class Value(models.Model):
    element = models.ForeignKey(Element, related_name="values")
    value = models.CharField('value', max_length=128)
    result = models.ForeignKey(Result, related_name="values")
