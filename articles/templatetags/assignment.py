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
		assignee_list = get_assignee_list(user.writers)
		available_list = get_available_list(user.writers)
		if article:
			assigned_to = article.writer
			available_to = article.writer_availability
			status = article.writer_status
		else:
			status = "Unavailable"
			assigned_to = None
			available_to = ""
	else:
		assignee_list = get_assignee_list(user.reviewers)
		available_list = get_available_list(user.reviewers)
		if article:
			assigned_to = article.reviewer
			available_to = article.reviewer_availability
			status = article.reviewer_status
		else:
			status = "Unavailable"
			assigned_to = None
			available_to = ""
	if as_list: status=group.title()
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
		assignee_list = get_assignee_list(user.writers)
		available_list = get_available_list(user.writers)
		if article:
			assigned_to = article.writer
			available_to = article.writer_availability
			status = article.writer_status
		else:
			status = "Unavailable"
			assigned_to = None
			available_to = ""
	else:
		assignee_list = get_assignee_list(user.reviewers)
		available_list = get_available_list(user.reviewers)
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

