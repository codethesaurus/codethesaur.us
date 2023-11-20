"""templatetags of codethesaur.us"""
from django import template
register = template.Library()


@register.inclusion_tag('concept_card.html')
def concept_card(code, comment):
    """tag for a single concept"""
    if isinstance(comment, list):
        comment = "\n".join(comment)

    return {
        'code': code,
        'comment': comment
    }
