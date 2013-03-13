from django import template
register = template.Library()

@register.inclusion_tag('articles/actions.html', takes_context = True)
def show_actions(context):
	user = context['request'].user
	if 'article' in context:
		article = context['article']
	else:pass
		# article = Article()
	if article: actions = article.get_available_actions(user)
	else: actions=[]
	if 'btn_size' in context: btn_size=context['btn_size']
	else: btn_size=""
	return {'request':context['request'], 'actions':actions, 'article':article, 'user':user,'STATIC_URL':context['STATIC_URL'],'btn_size':btn_size}


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