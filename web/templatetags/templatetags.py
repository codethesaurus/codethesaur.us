"""templatetags of codethesaur.us"""
from django import template

register = template.Library()

NAV_ITEMS = [
    {"label": "Home", "url": "/"},
    {"label": "About", "url": "/about/"},
    {"label": "Statistics", "url": "/statistics/"},
    {"label": "Docs", "url": "https://docs.codethesaur.us", "external": True},
    {"label": "Contribute", "url": "https://docs.codethesaur.us/contributing/", "external": True},
]


@register.simple_tag(takes_context=True)
def nav_items(context):
    """the primary navigation, with the current page marked

    Deriving `is_active` from the request keeps the highlighted item correct on every
    page; hardcoding it marked Home as current no matter where you were.

    :param context: the template context, used for the current request path
    :return: list of nav item dicts, each with label, url, is_active and external
    """
    request = context.get('request')
    current = request.path if request else None
    return [
        dict(item, is_active=item['url'] == current)
        for item in NAV_ITEMS
    ]


@register.inclusion_tag('concept_card.html')
def concept_card(code, comment, placeholder=None, language=None):
    """tag for a single concept"""
    return {
        'code': code,
        'comment': comment,
        'placeholder': placeholder,
        'language': language
    }
