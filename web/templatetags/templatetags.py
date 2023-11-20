"""templatetags of codethesaur.us"""
from django import template
register = template.Library()


@register.inclusion_tag('concept_card.html')
def concept_card(code, comment):
    """tag for a single concept"""
    return {
        'code': code,
        'comment': str(comment)
    }
