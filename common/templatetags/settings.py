from django import template

from core.settings import MY_TEMPLATES_SETTINGS

register = template.Library()


@register.filter(name='settings')
def setting(value):
    return MY_TEMPLATES_SETTINGS.get(value)
