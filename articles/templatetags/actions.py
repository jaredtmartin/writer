from django import template
from articles.models import Contact, WRITER_MODE, REVIEWER_MODE
register = template.Library()

@register.inclusion_tag('articles/actions.html', takes_context = True)
def show_actions(context):
	user = context['request'].user
	if 'article' in context:
		obj = context['article']
	elif 'object' in context:
		obj = context['object']
	else:pass
		# article = Article()
	if obj: actions = obj.get_available_actions(user)
	else: actions=[]
	if 'btn_size' in context: btn_size=context['btn_size']
	else: btn_size=""
	return {'request':context['request'], 'actions':actions, 'object':obj, 'article':obj, 'user':user,'STATIC_URL':context['STATIC_URL'],'btn_size':btn_size}

def get_contact(position, me, user):
	# Returns contact of the given type between the users or None is there is none.
	# If position is Requester, it returns a tuple of contacts, the first for writer, second for reviewer
	if position == 'Writer': 
		try: return me.writer_contacts.filter(worker=user)[0]
		except IndexError: return None
	elif position == 'Reviewer':
		try: return me.reviewer_contacts.filter(worker=user)[0]
		except IndexError: return None
	elif position == 'Requester':
		if me.mode == WRITER_MODE:
			try: return me.writes_for.filter(requester=user)[0]
			except IndexError: return None
		elif me.mode == REVIEWER_MODE:
			try: return me.reviews_for.filter(requester=user)[0]
			except IndexError: return None

def get_action_string(contact, me, obj, request_str='hire_user', remove_str='remove_user', accept_str='accept_user', reject_str='reject_user'):
	if not contact: 				return [request_str]
	elif contact.confirmation: 		return [remove_str]
	elif contact.user == me: return [remove_str]
	elif contact.user_asked == me:return [accept_str,reject_str]
	else: raise NotImplemented


@register.inclusion_tag('articles/user_actions.html', takes_context = True)
def show_user_actions(context):
	me = context['request'].user
	user_group = context.get('user_group',None)
	if 'object' in context:
		user = context['object']
	else:user = None
	try:
		status = context['status'] or 'all'
	except: status = 'all'
	print "status = %s" % str(status)
	if status == 'mine' or status == 'unconfirmed': actions = ['remove_user']
	elif status == 'other': actions = ['hire_user']
	elif status == 'requested': actions = ['accept_user','reject_user']
	else: 
		print "status = %s" % str(status)
		r = get_contact(user_group, me, user)
		if user_group == 'Requester':
			if me.mode == WRITER_MODE:
				actions = get_action_string(r, me, user, 'request_to_write','stop_writing','accept_writing','reject_writing')
			elif me.mode == REVIEWER_MODE:
				actions = get_action_string(r, me, user, 'request_to_review','stop_reviewing','accept_reviewing','reject_reviewing')
		else:
			actions = get_action_string(r, me, user)

	if 'btn_size' in context: btn_size=context['btn_size']
	else: btn_size=""
	return {
		'request':context['request'], 
		'actions':actions, 'object':user, 
		'user':me,
		'STATIC_URL':context['STATIC_URL'],
		'btn_size':btn_size, 
		'user_group':user_group,
		}

@register.inclusion_tag('articles/actions.html', takes_context = True)
def show_edit_page_actions(context):
	context = show_actions(context)
	if 'Submitted' in context['actions']:
		context['actions'].remove('Submitted')
		context['actions'] += ['Submit&Save']
	if 'Approved' in context['actions']:
		context['actions'].remove('Approved')
		context['actions'] += ['Approve&Save']
	if 'article' in context and context['article']:
		if context['request'].user in [context['article'].owner, context['article'].writer, context['article'].reviewer]:
			context['actions'] += ['Save']
	else:context['actions'] += ['Save']
	context['btn_size'] = 'btn-small'
	context['outlets'] = context['request'].user.publishing_outlets.all()
	return context

@register.inclusion_tag('articles/actions.html', takes_context = True)
def all_actions(context):
	context = show_actions(context)
	context.update('actions', ['claim','assign','submit','release','approve','reject','tag','delete'])
	return context