from django import template

register = template.Library()

def get_available_list(group):
	return list(set([c.name for c in group]))
def get_assignee_list(group):
	return list(set([contact.worker for contact in group]))
@register.inclusion_tag('articles/assignment_widget.html', takes_context = True)
def assignment_widget(context, group):
	user = context['request'].user
	if 'article' in context:
		as_list=False
		article = context['article']
	else: 
		as_list=True
		article=None
	if group == 'writer':
		assignee_list = get_assignee_list(user.writer_contacts)
		available_list = get_available_list(user.writer_contacts)
		if article:
			assigned_to = article.writer
			available_to = article.writer_availability
			status = article.writer_status
		else:
			status = "Unavailable"
			assigned_to = None
			available_to = "Nobody"
	else:
		assignee_list = get_assignee_list(user.reviewer_contacts)
		available_list = get_available_list(user.reviewer_contacts)
		if article:
			assigned_to = article.reviewer
			available_to = article.reviewer_availability
			print "available_to(1) = %s" % str(available_to)
			status = article.reviewer_status
		else:
			status = "Unavailable"
			assigned_to = None
			available_to = "Nobody"
			print "available_to(2) = %s" % str(available_to)
	if as_list: status=group.title()
	print "available_to = %s" % str(available_to)
	return {
		'assignee_list':assignee_list, 
		'user':user, 
		'group':group, 
		'assigned_to':assigned_to, 
		'available_to':available_to,
		'available_list':available_list,
		'status':status,
	}

@register.inclusion_tag('articles/assignment_edit_widget.html', takes_context = True)
def assignment_list_widget(context, group):
	user = context['request'].user
	if group == 'writer':
		assignee_list = get_assignee_list(user.writer_contacts)
		available_list = get_available_list(user.writer_contacts)
		if article:
			assigned_to = article.writer
			available_to = article.writer_availability
			status = article.writer_status
		else:
			status = "Unavailable"
			assigned_to = None
			available_to = ""
	else:
		assignee_list = get_assignee_list(user.reviewer_contacts)
		available_list = get_available_list(user.reviewer_contacts)
		if article:
			assigned_to = article.reviewer
			available_to = article.reviewer_availability
			status = article.reviewer_status
		else:
			status = "Unavailable"
			assigned_to = None
			available_to = ""
	return {
		'assignee_list':assignee_list, 
		'user':user, 
		'group':group, 
		'assigned_to':assigned_to, 
		'available_to':available_to,
		'available_list':available_list,
		'status':status,
	}

