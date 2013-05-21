from django.forms.widgets import Select
from django.utils.encoding import force_unicode
from itertools import chain
from django.forms.util import flatatt
from django.utils.html import escape, conditional_escape
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe 
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
class BootstrapDropdownWidget(Select):
    """
    http://twitter.github.com/bootstrap/components.html#buttonDropdowns
    Needs bootstrap and jquery
    """
    js = ("""
    <script type="text/javascript">
        function setBtnGroupVal(elem) {
            btngroup = $(elem).parents('.btn-group');
            selected_a = btngroup.find('a[selected]');
            if (selected_a.length > 0) {
                val = selected_a.attr('data-value');
                label = selected_a.html();
            } else {
                btngroup.find('a').first().attr('selected', 'selected');
                setBtnGroupVal(elem);
            }
            btngroup.find('input').val(val);
            btngroup.find('.btn-group-label').html(label);
        }
        $(document).ready(function() {
            $('.btn-group-form input').each(function() {
                setBtnGroupVal(this);
            });
            $('.btn-group-form li a').click(function() {
                $(this).parent().siblings().find('a').attr('selected', false);
                $(this).attr('selected', true);
                setBtnGroupVal(this);
            });
        })
    </script>
    """)
    html_template = ("""<div%(attrs)s>
            <button class="btn btn-small dropdown-toggle" type="button" data-toggle="dropdown">
                <span class="btn-group-label">%(label)s </span> <span class="caret"></span>
            </button>
            <ul class="dropdown-menu">
                %(options)s
            </ul>
            <input type="hidden" name="%(name)s" value="" class="btn-group-value" />
        </div>
        %(js)s
        <noscript>%(noscript)s</noscript>""")
    def __init__(self, attrs={'class': 'btn-group pull-left btn-group-form'}, choices=()):
        self.noscript_widget = Select(attrs={}, choices=choices)
        super(BootstrapDropdownWidget, self).__init__(attrs, choices)
    
    def __setattr__(self, k, value):
        super(BootstrapDropdownWidget, self).__setattr__(k, value)
        if k != 'attrs':
            self.noscript_widget.__setattr__(k, value)
    
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [self.html_template
                   % {'attrs': flatatt(final_attrs),
                      'options':self.render_options(choices, [value]),
                      'label': _(u'Select an option'),
                      'name': name,
                      'js': BootstrapDropdownWidget.js,
                      'noscript': self.noscript_widget.render(name, value, {}, choices)} ]
        return mark_safe(u'\n'.join(output))

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_unicode(option_value)
        selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
        return u'<li><a href="javascript:void(0)" data-value="%s"%s>%s</a></li>' % (
            escape(option_value), selected_html,
            conditional_escape(force_unicode(option_label)))

    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set([force_unicode(v) for v in selected_choices])
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<li class="divider" label="%s"></li>' % escape(force_unicode(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return u'\n'.join(output)
class BootstrapDropdownWidgetWithPlus(BootstrapDropdownWidget):
    html_template = ("""<div%(attrs)s>
            <button class="btn btn-small" type="button"><span class="icon-plus"></span></button>
            <button class="btn btn-small dropdown-toggle" type="button" data-toggle="dropdown">
                <span class="btn-group-label">%(label)s </span> <span class="caret"></span>
            </button>
            <ul class="dropdown-menu">
                %(options)s
            </ul>
            <input type="hidden" name="%(name)s" value="" class="btn-group-value" />
        </div>
        %(js)s
        <noscript>%(noscript)s</noscript>""")
class BootstrapSplitDropdownWidget(BootstrapDropdownWidget):
    html_template = """<div%(attrs)s>
            <button class="btn btn-small btn-group-label" type="button">%(label)s</button>
            <button class="btn btn-small dropdown-toggle" type="button" data-toggle="dropdown">
                <span class="caret"></span>
            </button>
            <ul class="dropdown-menu">
                %(options)s
            </ul>
            <input type="hidden" name="%(name)s" value="" class="btn-group-value" />
        </div>
        %(js)s
        <noscript>%(noscript)s</noscript>"""
class BootstrapSplitDropdownWidgetWithPlus(BootstrapSplitDropdownWidget):
    html_template = """<div%(attrs)s>
            <button class="btn btn-small" type="button"><span class="icon-plus"></span></button>
            <button class="btn btn-small btn-group-label" type="button">%(label)s</button>
            <button class="btn btn-small dropdown-toggle" type="button" data-toggle="dropdown">
                <span class="caret"></span>
            </button>
            <ul class="dropdown-menu">
                %(options)s
            </ul>
            <input type="hidden" name="%(name)s" value="" class="btn-group-value" />
        </div>
        %(js)s
        <noscript>%(noscript)s</noscript>"""