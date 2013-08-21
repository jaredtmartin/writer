from django import template
from articles.models import STATUS_ASSIGNED
register = template.Library()

def can_edit(user, article):
    if not article: return False
    if (user.is_staff or user == article.owner) and not article.submitted: return True
    if user == article.writer and not article.approved and not article.rejected: return True
    if user == article.reviewer and article.submitted: return True
    return False

register.filter('can_edit', can_edit)

def can_claim_to_write(user, article):
    if not article: return False
    if article.writer: return False
    # if (user.is_staff or user == article.owner) and not article.submitted: return True
    if article.writer_availability == "": return True
    try:
      if article.writer_availability in user.writing_contacts: return True
    except AttributeError: pass # If the user's not logged in, he wont have the writing contacts attribute
    return False
register.filter('can_claim_to_write', can_claim_to_write)

def can_claim_to_review(user, article):
    if not article: return False
    if article.reviewer: return False
    # if (user.is_staff or user == article.owner) and not article.submitted: return True
    if article.reviewer_availability == "": return True
    try:
      if article.reviewer_availability in user.reviewing_contacts: return True
    except AttributeError: pass # If the user's not logged in, he wont have the reviewing_contacts attribute
    return False
register.filter('can_claim_to_review', can_claim_to_review)

def writing_availability(article, user):
  if article.writer == user: 
    # if article.status == STATUS_REJECTED and article.rejected.author == user: return "Rejected"
    return "Me"
  if (can_claim_to_write(user, article)): return "Available"
  else: return "Unavailable"
register.filter('writing_availability', writing_availability)
def reviewing_availability(article, user):
  if article.reviewer == user: return "Me"
  if can_claim_to_review(user, article): return "Available"
  else: return "Unavailable"
register.filter('reviewing_availability', reviewing_availability)