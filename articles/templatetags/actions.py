from django import template
register = template.Library()

@register.inclusion_tag('articles/actions.html', takes_context = True)
def show_actions(context):
	user = context['request'].user
	article = context['article']
	try:
		actions = article.get_available_actions(user)
	except: actions=[]
	if 'btn_size' in context: btn_size=context['btn_size']
	else: btn_size=""
	return {'actions':actions, 'article':article, 'user':user,'STATIC_URL':context['STATIC_URL'],'btn_size':btn_size}
