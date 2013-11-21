from django import template
from articles.models import STATUS_ASSIGNED, WRITER_POSITION, REVIEWER_POSITION
register = template.Library()

def can_edit(user, article):
    if not article: return False
    if (user.is_staff or user == article.owner) and not article.submitted: return True
    if user == article.writer.writer and not article.submitted: return True
    if user == article.reviewer.reviewer and article.submitted: return True
    return False

register.filter('can_edit', can_edit)

def can_review(article, user):
    if not article: return False
    if (user.is_staff or user == article.owner): return True
    if user == article.writer.writer and not article.submitted: return True
    if user == article.reviewer.reviewer and article.submitted: return True
    return False

register.filter('can_edit', can_edit)

def can_claim_to_write(user, article):
    if not article: return False
    if article.writer: return False
    if not user.is_authenticated(): return False
    if article.available_to_all_writers: return True
    try: contact = Contact.objects.get(requester=article.owner, worker=user, position=WRITER_POSITION)
    except: return False
    if article.available_to_all_writers and contact: return True
    if contact in article.available_to_contacts.all(): return True
    for group in contact.contactgroup_set.all():
      if group in article.available_to_groups.all(): return True
    # if article.writer_availability == "": return True
    return False
register.filter('can_claim_to_write', can_claim_to_write)

def can_claim_to_review(user, article):
    if not article: return False
    if article.reviewer: return False
    if not user.is_authenticated(): return False
    if article.available_to_all_reviewers: return True
    try: contact = Contact.objects.get(requester=article.owner, worker=user, position=REVIEWER_POSITION)
    except: return False
    if article.available_to_all_reviewers and contact: return True
    if contact in article.available_to_contacts.all(): return True
    for group in contact.contactgroup_set.all():
      if group in article.available_to_groups.all(): return True
    # if article.reviewer_availability == "": return True
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