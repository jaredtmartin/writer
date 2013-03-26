from django import template
from articles.models import Relationship, WRITER_MODE, REVIEWER_MODE
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

def get_relationship(user_group, me, user):
	# Returns relationship of the given type between the users or None is there is none.
	# If user_group is Requester, it returns a tuple of relationships, the first for writer, second for reviewer
	if user_group == 'Writer': 
		try: return Relationship.objects.filter(requester=me, writer=user)[0]
		except IndexError: return None
	elif user_group == 'Reviewer':
		try: return Relationship.objects.filter(requester=me, reviewer=user)[0]
		except IndexError: return None
	elif user_group == 'Requester':
		if me.mode == WRITER_MODE:
			try: return Relationship.objects.filter(requester=user, writer=me)[0]
			except IndexError: return None
		elif me.mode == REVIEWER_MODE:
			try: return Relationship.objects.filter(requester=user, reviewer=me)[0]
			except IndexError: return None

def get_action_string(relationship, me, obj, request_str='hire_user', remove_str='remove_user', accept_str='accept_user', reject_str='reject_user'):
	if not relationship: 				return [request_str]
	elif relationship.confirmed: 		return [remove_str]
	elif relationship.created_by == me: return [remove_str]
	elif relationship.created_by == obj:return [accept_str,reject_str]
	else:
		print "relationship = %s" % str(relationship)
		print "relationship.confirmed = %s" % str(relationship.confirmed)
		print "relationship.created_by = %s" % str(relationship.created_by)
		print "me = %s" % str(me)
		print "obj = %s" % str(obj)
		raise NotImplemented
@register.inclusion_tag('articles/user_actions.html', takes_context = True)
def show_user_actions(context):
	me = context['request'].user
	user_group = context['user_group']
	print "me = %s" % str(me)
	print "user_group = %s" % str(user_group)
	if 'object' in context:
		user = context['object']
	else:user = None
	print "user = %s" % str(user)
	try:
		status = context['status'] or 'all'
	except: status = 'all'
	print "status = %s" % str(status)
	if status == 'mine' or status == 'unconfirmed': actions = ['remove_user']
	elif status == 'other': actions = ['hire_user']
	elif status == 'requested': actions = ['accept_user','reject_user']
	else: 
		print "status = %s" % str(status)
		r = get_relationship(user_group, me, user)
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
	print "context = %s" % str(context)
	return context

@register.inclusion_tag('articles/actions.html', takes_context = True)
def all_actions(context):
	context = show_actions(context)
	context.update('actions', ['claim','assign','submit','release','approve','reject','tag','delete'])
	return context