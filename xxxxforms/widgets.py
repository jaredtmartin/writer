from  django.forms import widgets
from django.utils.safestring import mark_safe

class SubmitWidget(widgets.Widget):
    def render(self, name, value, attrs=None):
        return u'<input type="submit" value="%s">' % name

class HeaderWidget(widgets.Widget):
    def render(self, name, value, attrs=None):
        return mark_safe('<h1>%s</h1>' % name)

class LabelWidget(widgets.Widget):
    def __init__(self, text, attrs=None):
        self.text=text
        super(LabelWidget,self).__init__(attrs)
    def render(self, name, value, attrs=None):
        return mark_safe('<p>%s</p>' % self.text)
        
class ImageWidget(widgets.Widget):
    def __init__(self,filename, label_position=None, attrs=None):
        self.label_position=label_position
        self.filename=filename
        super(ImageWidget,self).__init__(attrs)
        
    def render(self, name, value, attrs=None):
        html='<img src="%s" alt="%s">' % (self.filename, name)
        if self.label_position=='left': html=name+html
        if self.label_position=='right': html+=name
        return mark_safe(html)

class jEditableWidget(widgets.Widget):
    def render(self, name, value, attrs=None):
        element_id=attrs.get('id','XXX')
        print "attrs: " + str(attrs) 
        return mark_safe('<div class="jEditable" id="%s">%s</div>' % (element_id, name))


