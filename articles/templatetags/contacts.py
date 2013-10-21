from django import template
register = template.Library()

def get_contact(me, user, position):
  try:
    if position in [1,2]: return Contact.objects.get(requester=me, worker=user, position=position)
    else: return Contact.objects.get(requester=user, worker=me, position=position)
  except: return None
def contact_status(me, user, position):
  contact = get_contact(user, me, position)
  if not contact: return "No Contact"
  if not contact.confirmation:
    if contact.user_asked == me: return "Requesting work"
    else: return "Awaiting Approval"
  if contact.requester == me: return "Hired"

register.filter('contact_status', contact_status)