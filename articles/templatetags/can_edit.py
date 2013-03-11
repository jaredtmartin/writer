from django import template

register = template.Library()

def can_edit(user, article):
    """Removes all values of arg from the given string"""
    if (user.is_staff) or (user == article.owner) or\
    	(user == article.writer and not article.accepted and not article.rejected) or \
    	(user == article.reviewer and article.submitted):
    	return True
    else: return False

register.filter('can_edit', can_edit)