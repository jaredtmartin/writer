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

	if 'btn_size' in context: btn_size=context['btn_size']
	else: btn_size=""
	return {'actions':actions, 'article':article, 'user':user,'STATIC_URL':context['STATIC_URL'],'btn_size':btn_size}
@register.inclusion_tag('articles/actions.html', takes_context = True)
def all_actions(context):
	context = show_actions(context)
	context.update('actions', ['claim','assign','submit','release','approve','reject','tag','delete'])
	return context