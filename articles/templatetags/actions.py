from django import template

register = template.Library()

@register.inclusion_tag('articles/actions.html', takes_context = True)
def show_actions(context):
    user = context['request'].user
    article = context['article']
    actions = article.get_available_actions(user)
    return {'actions':actions, 'article':article, 'user':user}
