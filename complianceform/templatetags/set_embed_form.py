from django import template
register = template.Library()

@register.simple_tag
def set_url(principle = None):
    url = principle
    return url