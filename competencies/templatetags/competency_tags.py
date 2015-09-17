from django import template

register = template.Library()

@register.filter
def is_list(object):
    return isinstance(object, list)
