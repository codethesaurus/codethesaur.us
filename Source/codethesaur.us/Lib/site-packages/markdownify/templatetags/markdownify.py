import warnings

from functools import partial

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

import markdown
import bleach


register = template.Library()


def legacy():
    """
    Function used to transform old style settings to new style settings
    """

    # Bleach settings
    whitelist_tags = getattr(settings, 'MARKDOWNIFY_WHITELIST_TAGS', bleach.sanitizer.ALLOWED_TAGS)
    whitelist_attrs = getattr(settings, 'MARKDOWNIFY_WHITELIST_ATTRS', bleach.sanitizer.ALLOWED_ATTRIBUTES)
    whitelist_styles = getattr(settings, 'MARKDOWNIFY_WHITELIST_STYLES', bleach.sanitizer.ALLOWED_STYLES)
    whitelist_protocols = getattr(settings, 'MARKDOWNIFY_WHITELIST_PROTOCOLS', bleach.sanitizer.ALLOWED_PROTOCOLS)

    # Markdown settings
    strip = getattr(settings, 'MARKDOWNIFY_STRIP', True)
    extensions = getattr(settings, 'MARKDOWNIFY_MARKDOWN_EXTENSIONS', [])

    # Bleach Linkify
    values = {}
    linkify_text = getattr(settings, 'MARKDOWNIFY_LINKIFY_TEXT', True)

    if linkify_text:
        values = {
            "PARSE_URLS": True,
            "PARSE_EMAIL": getattr(settings, 'MARKDOWNIFY_LINKIFY_PARSE_EMAIL', False),
            "CALLBACKS": getattr(settings, 'MARKDOWNIFY_LINKIFY_CALLBACKS', None),
            "SKIP_TAGS": getattr(settings, 'MARKDOWNIFY_LINKIFY_SKIP_TAGS', None)
        }

    return {
        "STRIP": strip,
        "MARKDOWN_EXTENSIONS": extensions,
        "WHITELIST_TAGS": whitelist_tags,
        "WHITELIST_ATTRS": whitelist_attrs,
        "WHITELIST_STYLES": whitelist_styles,
        "WHITELIST_PROTOCOLS": whitelist_protocols,
        "LINKIFY_TEXT": values,
        "BLEACH": getattr(settings, 'MARKDOWNIFY_BLEACH', True)
    }


@register.filter
def markdownify(text, custom_settings="default"):

    # Check for legacy settings
    setting_keys = [
        'WHITELIST_TAGS',
        'WHITELIST_ATTRS',
        'WHITELIST_STYLES',
        'WHITELIST_PROTOCOLS',
        'STRIP',
        'MARKDOWN_EXTENSIONS',
        'LINKIFY_TEXT',
        'BLEACH',
    ]
    has_settings_old_style = False
    for key in setting_keys:
        if getattr(settings, f"MARKDOWNIFY_{key}", None):
            has_settings_old_style = True
            break

    if has_settings_old_style:
        markdownify_settings = legacy()
    else:
        try:
            markdownify_settings = settings.MARKDOWNIFY[custom_settings]
        except (AttributeError, KeyError):
            markdownify_settings = {}

    # Bleach settings
    whitelist_tags = markdownify_settings.get('WHITELIST_TAGS', bleach.sanitizer.ALLOWED_TAGS)
    whitelist_attrs = markdownify_settings.get('WHITELIST_ATTRS', bleach.sanitizer.ALLOWED_ATTRIBUTES)
    whitelist_styles = markdownify_settings.get('WHITELIST_STYLES', bleach.sanitizer.ALLOWED_STYLES)
    whitelist_protocols = markdownify_settings.get('WHITELIST_PROTOCOLS', bleach.sanitizer.ALLOWED_PROTOCOLS)

    # Markdown settings
    strip = markdownify_settings.get('STRIP', True)
    extensions = markdownify_settings.get('MARKDOWN_EXTENSIONS', [])

    # Bleach Linkify
    linkify = None
    linkify_text = markdownify_settings.get('LINKIFY_TEXT', {"PARSE_URLS": True})
    if linkify_text.get("PARSE_URLS"):
        linkify_parse_email = linkify_text.get('PARSE_EMAIL', False)
        linkify_callbacks = linkify_text.get('CALLBACKS', [])
        linkify_skip_tags = linkify_text.get('SKIP_TAGS', [])
        linkifyfilter = bleach.linkifier.LinkifyFilter

        linkify = [partial(linkifyfilter,
                           callbacks=linkify_callbacks,
                           skip_tags=linkify_skip_tags,
                           parse_email=linkify_parse_email
                           )]

    # Convert markdown to html
    html = markdown.markdown(text or "", extensions=extensions)

    # Sanitize html if wanted
    if markdownify_settings.get("BLEACH", True):
        cleaner = bleach.Cleaner(tags=whitelist_tags,
                                 attributes=whitelist_attrs,
                                 styles=whitelist_styles,
                                 protocols=whitelist_protocols,
                                 strip=strip,
                                 filters=linkify,
                                 )

        html = cleaner.clean(html)

    return mark_safe(html)
