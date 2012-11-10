from  django.forms import widgets
from django.utils.safestring import mark_safe

class SubmitWidget(widgets.Widget):
    def render(self, name, value, attrs=None):
        return u'<input type="submit" value="%s">' % name

class HeaderWidget(widgets.Widget):
    def render(self, name, value, attrs=None):
        return mark_safe('<h1>%s</h1>' % name)

class LabelWidget(widgets.Widget):
    def render(self, name, value, attrs=None):
        return mark_safe('<p>%s</p>' % name)
