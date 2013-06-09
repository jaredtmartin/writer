from django import template
from articles.models import STATUS_ASSIGNED
register = template.Library()

def can_edit(user, article):
    """Removes all values of arg from the given string"""
    if not article: return False
    if (user.is_staff or user == article.owner) and not article.submitted: return True
    if user == article.writer and not article.approved and not article.rejected: return True
    if user == article.reviewer and article.submitted: return True
    return False

register.filter('can_edit', can_edit)