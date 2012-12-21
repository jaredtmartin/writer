from django.forms.widgets import Select
from django.utils.encoding import force_unicode
from itertools import chain
class SelectWithFlexibleOptionLabels(Select):
    def __init__(self, attrs=None, choices=(), **kwargs):
        self.pre_label= kwargs.get('pre_label', '')
        self.post_label= kwargs.get('post_label', '')
        super(SelectWithFlexibleOptionLabels, self).__init__(attrs)
        print "self.choices: " + str(self.choices) 
    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set(force_unicode(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append(u'</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return u'\n'.join(output)
