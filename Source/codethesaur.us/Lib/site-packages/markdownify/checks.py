from django.core.checks import register, Warning
from django.conf import settings


@register()
def settings_check(app_configs, **kwargs):

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
        return [Warning(
            msg="Old style settings are being deprecated in version 1.0",
            hint="See https://django-markdownify.readthedocs.io/en/latest/ for instructions on upgrading your settings",
            obj="Markdownify"
        )]

    return []
