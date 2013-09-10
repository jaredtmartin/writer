from django.forms.widgets import Select
from django.utils.encoding import force_unicode
from itertools import chain
from django.forms.util import flatatt
from django.utils.html import escape, conditional_escape
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe 
# class SelectWithFlexibleOptionLabels(Select):
#   def __init__(self, attrs=None, choices=(), **kwargs):
#     self.pre_label= kwargs.get('pre_label', '')
#     self.post_label= kwargs.get('post_label', '')
#     super(SelectWithFlexibleOptionLabels, self).__init__(attrs)
#   def render_options(self, choices, selected_choices):
#     # Normalize to strings.
#     selected_choices = set(force_unicode(v) for v in selected_choices)
#     output = []
#     for option_value, option_label in chain(self.choices, choices):
#       if isinstance(option_label, (list, tuple)):
#         output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
#         for option in option_label:
#           output.append(self.render_option(selected_choices, *option))
#         output.append(u'</optgroup>')
#       else:
#         output.append(self.render_option(selected_choices, option_value, option_label))
#     return u'\n'.join(output)
class BootstrapDropdown(Select):
  js=""
  option_template = """<option value="%(value)s" %(selected_html)s>%(label)s</option>"""
  options_template = u''
  html_template = ("""
    <div class="help" %(help_text)s >
      <select%(attrs)s>
          %(options)s
      </select>
    </div>
      """)
  attrs = {
    'class':" selectpicker help"
  }

  def get_help_text(self, str):
    if not str: return ""
    return ' data-original-title="%s" title="%s"' % (str,str)
  def add_attrs(self, attrs):
    # merges attributes passed into init with those included with class definition
    if not attrs: return self.attrs
    for key, value in self.attrs.items():
        if key in attrs: attrs[key]+=" "+value
        else: attrs[key]=value
    # Add in btn-size if set
    # if self.btn_size:
    #     if 'class' in attrs: attrs['class']+='btn-'+self.btn_size
    #     else: attrs['class']='btn-'+self.btn_size
    return attrs
  def __init__(self, *args, **kwargs):

    attrs = kwargs.pop('attrs',{})
    help_text = self.get_help_text(kwargs.pop('help_text',None))
    # self.btn_size = kwargs.pop('btn_size',None)
    attrs = self.add_attrs(attrs)
    choices = kwargs.pop('choices',())
    self.noscript_widget = Select(attrs={}, choices=choices)
    super(BootstrapDropdown, self).__init__(attrs, choices)
    self.help_text = help_text
    print "self.help_text = %s" % str(self.help_text)
    
  def __setattr__(self, k, value):
    super(BootstrapDropdown, self).__setattr__(k, value)
    if k != 'attrs':
        self.noscript_widget.__setattr__(k, value)
  def get_label(self):
    return _(u'Select an option')
  def get_context(self, final_attrs, choices, value, name):
    print "get_context: self.help_text = %s" % str(self.help_text)
    return {'attrs': flatatt(final_attrs),
      'options':self.render_options(choices, [value]),
      'label': self.get_label(),
      'name': name,
      'help_text':self.help_text,
      'noscript': self.noscript_widget.render(name, value, {}, choices)
      }
  def render(self, name, value, attrs=None, choices=()):
    print "attrs = %s" % str(attrs)
    attrs = self.add_attrs(attrs)
    print "self.help_text = %s" % str(self.help_text)
    print "attrs = %s" % str(attrs)

    if value is None: value = ''
    final_attrs = self.build_attrs(attrs, name=name)
    output = [self.html_template % self.get_context(final_attrs, choices, value, name)]
    return mark_safe(u'\n'.join(output))
  def get_option_context(self, option_value, selected_html, option_label):
    return {
      'value':escape(option_value), 
      'selected_html': selected_html,
      'label':conditional_escape(force_unicode(option_label))
      }
  def render_option(self, selected_choices, option_value, option_label):
    option_value = force_unicode(option_value)
    selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
    output = self.option_template % self.get_option_context(option_value, selected_html, option_label)
    return output

  def render_options(self, choices, selected_choices):
    # Normalize to strings.
    selected_choices = set([force_unicode(v) for v in selected_choices])
    output = []
    for option_value, option_label in chain(self.choices, choices):
      if isinstance(option_label, (list, tuple)):
        output.append(self.options_template % escape(force_unicode(option_value)))
        for option in option_label:
          output.append(self.render_option(selected_choices, *option))
      else:
        output.append(self.render_option(selected_choices, option_value, option_label))
    return u'\n'.join(output)
# class BootstrapDropdown(BootstrapDropdownWidget):
#     def __init__(self, attrs=None, choices=(), **kwargs):
        
#         super(BootstrapDropdown, self).__init__(attrs, choices)
#     attrs = {
#         'class':" selectpicker"
#     }
#     js=""
#     option_template = """<option value="%(value)s" %(selected_html)s>%(label)s</option>"""
#     options_template = u''
#     html_template = ("""
#         <select%(attrs)s>
#             %(options)s
#         </select>
#         <noscript>%(noscript)s</noscript>""")

class BootstrapDropdownPlus(BootstrapDropdown):
    attrs = {
        'class':" selectpicker"
    }
    def __init__(self, *args, **kwargs):
      plus_url = kwargs.pop('plus_url','')
      super(BootstrapDropdownPlus, self).__init__(*args, **kwargs)
      self.plus_url=plus_url
      # self.label = kwargs.pop('label')

    def get_label(self):
        return None
    def get_context(self, final_attrs, choices, value, name):
        context = super(BootstrapDropdownPlus, self).get_context(final_attrs, choices, value, name)
        context['plus_url'] = self.plus_url
        return context
    js=""
    option_template = """<option value="%(value)s" %(selected_html)s>%(label)s</option>"""
    options_template = u''
    html_template = ("""
        <div class="btn-group selectplus help" %(help_text)s >
            <select%(attrs)s>
                %(options)s
            </select>
            <button class="btn btn-primary" type="button"><i class="fui-plus"></i></button>
            
        </div>
        <noscript>%(noscript)s</noscript>""")
class BootstrapDropdownPlusMultiple(BootstrapDropdown):
    attrs = {
        'class':" selectpicker",
        'multiple':""
    }