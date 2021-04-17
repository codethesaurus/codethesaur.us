from django import template
register = template.Library()

@register.inclusion_tag('comparecard.html')
def comparecard(code, comment):
    return {
        'code': code,
        'comment': comment
    }