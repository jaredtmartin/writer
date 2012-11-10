from django import template
from django.utils.safestring import mark_safe
from forms.widgets import SubmitWidget
from forms import forms
from django.forms.forms import BoundField
from django.forms.widgets import *
register = template.Library()

#def element(e):
#    if e.klass = Element.HEADER:
#        return u"<h1>%s</h1>"
#    elif e.klass = Element.TEXTBOX:
#        return u'%s: <input type="text" name="%s">' % (e.name, e.name)
#    elif e.klass = Element.PASSWORD:
#        return u'%s: <input type="password" name="%s">' % (e.name, e.name)
#    elif e.klass = Element.RADIO:
#        s=u"<form>"
#        for opt in e.details.split(","):
#            s+=u'<input type="radio" value="%s">' % (opt, opt)
#        s+=u'</form>'
#        return s

@register.filter(is_safe=True)
def as_element(element):
    return mark_safe(element.as_unicode())
    
@register.filter(is_safe=True)    
def as_form(f): return forms.make_form(f).as_p()

@register.filter(is_safe=True)   
def formfield(form, key):
    s=''
    if key in form.errors:
        s+='<ul class="errorlist">'
        for error in form.errors[key]:
            s+='<li>%s</li>' % error
        s+='</ul>'
    if not form.fields[key].widget.__class__ is SubmitWidget: 
        s+=u'<label for="id_%s">%s:</label>' % (key,key)
    if form.fields[key].widget.__class__ is Textarea: s+="<br>" 
    s+=unicode(BoundField(form, form.fields[key], key)) + "<br>"
    return mark_safe(s)


