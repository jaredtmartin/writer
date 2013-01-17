from django import template

register = template.Library()

def list_block(context, title, 
    headings, 
    object_list, 
    row_template, 
    table_id, 
    row_id, 
    searchbar=False, 
    checkboxes=False, 
    row_actions=False,
    form_id=None,
    form_method="post",
    form_action="",
    action_bar_actions=[],
    action_bar_template="",
    ):
    return {
        'title': title,
        'headings': headings.split(', '),
        'object_list': object_list,
        'row_template': row_template,
        'searchbar': searchbar,
        'checkboxes': checkboxes,
        'row_actions': row_actions,
        'table_id': table_id,
        'row_id':row_id,
        'form_id': form_id,
        'form_method': form_method,
        'form_action': form_action,
        'action_bar_actions':action_bar_actions,
        'action_bar_template':action_bar_template,
        'user':context['user']
    }
register.inclusion_tag('articles/list_block.html', takes_context=True)(list_block)
