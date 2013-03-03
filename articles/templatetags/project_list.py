from django.template import Library, Node, resolve_variable
from articles.models import Project
import json
register = Library()


class ProjectList(Node):
  def render(self, context):
    req = resolve_variable('request',context)
    projects = Project.objects.filter(owner=req.user).values_list('name', flat=True)
    return json.dumps([unicode(t) for t in projects]) # Convert to js compatible list
def project_list(parser, token):
  return ProjectList()
register.tag('project_list', project_list)