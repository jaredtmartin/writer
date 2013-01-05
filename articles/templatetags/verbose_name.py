from django import template
register = template.Library()

@register.filter(is_safe=True)
def verbose_name(obj):
    return obj._meta.verbose_name
