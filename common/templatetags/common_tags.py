from django.template import Library, Node, resolve_variable, TemplateSyntaxError

register = Library()

class AddParameter(Node):
  def __init__(self, varname, value):
    self.varname = varname
    self.value = value

  def render(self, context):
    req = resolve_variable('request',context)
    params = req.GET.copy()
    params[self.varname] = self.value
    return '%s?%s' % (req.path, params.urlencode())

def addparam(parser, token):
  from re import split
  bits = split(r'\s+', token.contents, 2)
  if len(bits) < 2:
    raise TemplateSyntaxError, "'%s' tag requires two arguments" % bits[0]
  return AddParameter(bits[1],bits[2])

register.tag('addparam', addparam)
