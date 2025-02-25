from django import template
from markdown import markdown

register = template.Library()

@register.filter(is_safe=True)
def md(value):
    """Converts a markdown string into html"""
    return markdown(value)
