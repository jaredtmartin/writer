from  django.forms import widgets

class SubmitWidget(widgets.Widget):
    def render(self, name, value, attrs=None):
#        print "name: " + str(name) 
#        print "value: " + str(value) 
#        print "attrs: " + str(attrs) 
        return u'<input type="submit" value="%s">' % name

class LabelWidget(widgets.Widget):
    def render(self, name, value, attrs=None):
#        print "name: " + str(name) 
#        print "value: " + str(value) 
#        print "attrs: " + str(attrs) 
        return u'<h1>%s</h1>' % name
