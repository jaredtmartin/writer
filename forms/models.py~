from django.db import models
from django.template.defaultfilters import slugify

class Form(models.Model):
    name = models.CharField('Name', max_length=32)
    success_url = models.CharField('Success URL', max_length=64, default='thankyou/')
    submit_label = models.CharField('Submit Label', max_length=32, default='Submit')
    def __unicode__(self): return self.name
    @models.permalink
    def get_absolute_url(self):
        return ('form', [self.id, slugify(self.name)])
    @models.permalink
    def get_action_url(self):
        return ('submit', [self.id, slugify(self.name)])
    
class Element(models.Model):
    HEADER = 'HD'
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
        (EMAIL,'Email Address')
    )
    name = models.CharField('Name', max_length=32)
    klass = models.CharField('Type', max_length=2, choices = ELEMENT_TYPE_CHOICES, default=TEXTBOX)
    required = models.BooleanField(default=False, blank=True)
    unique = models.BooleanField(default=False, blank=True)
    description = models.CharField('Description', max_length=64, default="", blank=True)
    tooltip = models.CharField('Tooltip', max_length=32, default="", blank=True)
    order = models.IntegerField(blank=True, default=1)
    details = models.CharField('Choices', max_length=128, blank=True, default="")
    form = models.ForeignKey(Form, related_name='elements')
    class Meta:
        ordering = ('order', '-id', )
    def __unicode__(self): return self.name
#    def as_unicode(self):
#        if self.klass == Element.HEADER:
#            return u"<h1>%s</h1>" % self.name
#        elif self.klass == Element.TEXTBOX:
#            return u'<label for="%s">%s</label>: <input type="text" name="%s"><br>' % (self.name.lower(), self.name, self.name.lower())
#        elif self.klass == Element.PASSWORD:
#            return u'<label for="%s">%s</label>: <input type="password" name="%s"><br>' % (self.name.lower(), self.name, self.name.lower())
#        elif self.klass == Element.TEXTAREA:
#            return u'<label for="%s">%s</label>:<br><textarea name="%s"></textarea><br>' % (self.name.lower(), self.name, self.name.lower())
#        elif self.klass == Element.DROPDOWN:
#            s=u'<label for="%s">%s</label>:<select name="%s">' % (self.name.lower(), self.name, self.name.lower())
#            for opt in self.details.split(","):
#                s+=u'<option value="%s">%s</option>' % (opt.lower(), opt)
#            s+=u'</select><br>'
#            return s
#        elif self.klass == Element.CHECKBOX:
#            return u'<input type="checkbox" name="%s" value="%s"><label for="%s">%s</label><br>' % (self.name.lower(), self.name.lower(), self.name.lower(), self.name)
#        elif self.klass == Element.SUBMIT:
#            return u'<input type="submit" value="%s">' % (self.name)
#        elif self.klass == Element.RADIO:
#            return u'<input type="radio" name="%s" value="%s"> <label for="%s">%s</label> <br>' % (self.details.lower(), self.name.lower(), self.name.lower(), self.name)

class Result(models.Model):
    form = models.ForeignKey(Form, related_name='results')
    created_at = models.DateTimeField(auto_now_add=True)
    @models.permalink
    def get_absolute_url(self):
        return ('result', [self.id, slugify(self.name)])
        
class Value(models.Model):
    element = models.ForeignKey(Element, related_name="element_values")
    value = models.CharField('value', max_length=128)
    result = models.ForeignKey(Result)
