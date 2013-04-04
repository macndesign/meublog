from django import template

register = template.Library()

@register.filter
def list_count(value, arg):
    return value.count(arg)
