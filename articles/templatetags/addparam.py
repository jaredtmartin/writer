from django.template import Library, Node, resolve_variable, TemplateSyntaxError, Variable
from django import template
register = Library()

class AddParameter(Node):
  def __init__(self, varname, value):
    if self.quoted(varname): self.varname = varname[1:-1]
    else: self.varname = template.Variable(varname)
    if self.quoted(value): self.value = value[1:-1]
    else: self.value = template.Variable(value)
    
  def quoted(self, string):
    return (string[0] == string[-1] and string[0] in ('"', "'"))
  def render(self, context):
    try: varname = self.varname.resolve(context)
    except:pass
    try: value = self.value.resolve(context)
    except:pass
    req = resolve_variable('request',context)
    params = req.GET.copy()
    params[varname] = value
    return '%s?%s' % (req.path, params.urlencode())

def addurlparameter(parser, token):
  from re import split
  bits = split(r'\s+', token.contents, 2)
  if len(bits) < 2:
    raise TemplateSyntaxError, "'%s' tag requires two arguments" % bits[0]
  return AddParameter(bits[1],bits[2])

register.tag('addurlparameter', addurlparameter)

class RemoveParameter(Node):
  def __init__(self, varname):
    if self.quoted(varname): self.varname = varname
    else: self.varname = template.Variable(varname)
  def quoted(self, string):
    return (string[0] == string[-1] and string[0] in ('"', "'"))
  def render(self, context):
    try: varname = self.varname.resolve(context)
    except:pass
    req = resolve_variable('request',context)
    params = req.GET.copy()
    try: del params[varname]
    except: pass
    return '%s?%s' % (req.path, params.urlencode())

def removeurlparameter(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tagname, varname = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError("%r tag requires exactly one argument" % token.contents.split()[0])
    return RemoveParameter(varname)
    
#def removeurlparameter(parser, token):
#  from re import split
#  bits = split(r'\s+', token.contents, 2)
#  if not len(bits) == 1:
#    raise TemplateSyntaxError, "'%s' tag requires exactly one argument" % bits[0]
#  return RemoveParameter(bits[1])  

register.tag('removeurlparameter', removeurlparameter)
