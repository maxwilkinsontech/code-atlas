import markdown as md

from django.template.defaultfilters import stringfilter
from django import template


register = template.Library()

@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['fenced_code', 'codehilite'])