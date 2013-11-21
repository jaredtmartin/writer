from django.forms.widgets import Select
from django.utils.encoding import force_unicode
from itertools import chain
from django.forms.util import flatatt
from django.utils.html import escape, conditional_escape
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe 

class BootstrapDropdown(Select):
  select_option_template = """<option id="%(name)s-option-%(value)s" value="%(value)s" %(option_selected_html)s>%(label)s</option>"""
  list_item_template = """<li id="%(name)s-list-item-%(value)s" name="%(name)s" data-label="%(label)s" rel="%(value)s" class="select-list-item %(list_selected_html)s"><a class="" tabindex="-1"><span class="pull-left">%(label)s</span></a></li>"""
  html_template = ("""
      <select%(attrs)s style="display: none;">
        %(select_options)s
      </select>
      <div class="btn-group select">
        <button id="%(name)s-button" data-toggle="dropdown" class="btn dropdown-toggle clearfix btn-small btn-primary">
          <span id="select-label-%(name)s" class="filter-option pull-left">%(label)s</span>&nbsp;<span class="caret"></span>
        </button>
        <i class="dropdown-arrow dropdown-arrow-inverse"></i>
        <ul id="%(name)s-dropdown-menu" role="menu" class="dropdown-menu dropdown-inverse" style="overflow-y: auto; min-height: 108px;">
          %(list_items)s
        </ul>
      </div>
    
    """)
  attrs = {}
  label=None
  selected_label = None
  def get_help_text(self, str): pass
  #   if not str: return ""
  #   return ' data-original-title="%s" title="%s"' % (str,str)
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
    # print "kwargs = %s" % str(kwargs)
    label = kwargs.pop('label', None)
    help_text = self.get_help_text(kwargs.pop('help_text',None))
    # self.btn_size = kwargs.pop('btn_size',None)
    attrs = self.add_attrs(attrs)
    choices = kwargs.pop('choices',())
    self.noscript_widget = Select(attrs={}, choices=choices)
    super(BootstrapDropdown, self).__init__(attrs, choices)
    self.help_text = help_text
    # print "label = %s" % str(label)
    self.label=label
    # print "self.label = %s" % str(self.label)
    # print "self.help_text = %s" % str(self.help_text)
    
  def __setattr__(self, k, value):
    super(BootstrapDropdown, self).__setattr__(k, value)
    if k != 'attrs':
        self.noscript_widget.__setattr__(k, value)
  def get_label(self):
    # print "self.label = %s" % str(self.label)
    if self.label: label = self.label
    elif self.name: label = self.name.title()
    if label:

      if self.value and self.selected_label: label+= ': %s' % self.selected_label
      return label
    else:
      return _(u'Select an option')
  def get_context(self, final_attrs, choices, value, name):
    # print "====================self.label = %s" % str(self.label)
    # print "self.get_label() = %s" % str(self.get_label())
    self.value=value
    options=self.render_options(choices, [value])
    return {
      'attrs': flatatt(final_attrs),
      'select_options':options['select'],
      'list_items':options['list'],
      'label': self.get_label(),
      'name': name,
      'help_text':self.help_text,
      'noscript': self.noscript_widget.render(name, value, {}, choices)
      }
  def render(self, name, value, attrs=None, choices=()):
    self.name = name
    # print "attrs = %s" % str(attrs)
    attrs = self.add_attrs(attrs)
    # print "self.help_text = %s" % str(self.help_text)
    # print "attrs = %s" % str(attrs)
    # print "value = %s" % str(value)

    if value is None: value = ''
    final_attrs = self.build_attrs(attrs, name=name)
    output = [self.html_template % self.get_context(final_attrs, choices, value, name)]
    return mark_safe(u'\n'.join(output))
  def get_option_context(self, option_value, selected_html, option_label):
    label = conditional_escape(force_unicode(option_label)) or "None"
    if selected_html: 
      list_selected='selected'
      self.selected_label=label
    else: list_selected = ""
    return {
      'value':escape(option_value),
      'option_selected_html': selected_html,
      'list_selected_html':list_selected,
      'name':self.name,
      'label':label
      }
  def render_option(self, selected_choices, option_value, option_label):
    option_value = force_unicode(option_value)
    selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
    context = self.get_option_context(option_value, selected_html, option_label)
    select_option_output = self.select_option_template % context
    list_item_output = self.list_item_template % context
    return {'list_item':list_item_output, 'select_option':select_option_output}

  def render_options(self, choices, selected_choices):
    # Normalize to strings.
    selected_choices = set([force_unicode(v) for v in selected_choices])
    output = {'list':[],'select':[]}
    for option_value, option_label in chain(self.choices, choices):
      if isinstance(option_label, (list, tuple)):
        for option in option_label:
          output.append(self.render_option(selected_choices, *option))
      else:
        o = self.render_option(selected_choices, option_value, option_label)
        output['list'].append(o['list_item'])
        output['select'].append(o['select_option'])
    output['list'] = u'\n'.join(output['list'])
    output['select'] = u'\n'.join(output['select'])
    return output

class BootstrapDropdownPlus(BootstrapDropdown):
    list_item_template = """<li id="%(name)s-list-item-%(value)s" name="%(name)s" data-label="%(label)s" rel="%(value)s" class="select-list-item %(list_selected_html)s"><a class="" tabindex="-1"><span class="pull-left">%(label)s</span></a></li>"""
    html_template = ("""
        <select%(attrs)s style="display: none;">
          %(select_options)s
        </select>
      <div class="btn-group">
        <div class="btn-group select">
          <button data-toggle="dropdown" class="btn dropdown-toggle clearfix btn-small btn-primary">
            <span id="select-label-%(name)s" class="filter-option pull-left">%(label)s</span>&nbsp;<span class="caret"></span>
          </button>
          <i class="dropdown-arrow dropdown-arrow-inverse"></i>          
          <ul id="%(name)s-dropdown-menu" role="menu" class="dropdown-menu dropdown-inverse" style="overflow-y: auto; min-height: 108px;">
            %(list_items)s
          </ul>
        </div>
        <button type="button" id="%(name)s-button" data-toggle="modal" data-target="#%(name)s-modal" class="btn btn-primary btn-small btn-select-plus"><i class="fui-plus"></i></button>
      </div>
      """)
class BootstrapDropdownPlusMultiple(BootstrapDropdown):
    attrs = {
        'class':" selectpicker",
        'multiple':""
    }