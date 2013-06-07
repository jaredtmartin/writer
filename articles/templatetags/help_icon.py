import datetime
from django import template

register = template.Library()

def help_icon(text):
    return '<a class="help" title="" data-toggle="tooltip" href="#" data-original-title="%s"><i class="icon-question-sign"></i></a>' % text

register.simple_tag(help_icon)