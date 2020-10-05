from django import template
register = template.Library()

@register.inclusion_tag('comparecard.html')
def comparecard(code):
    return {'code': code}