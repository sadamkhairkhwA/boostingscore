from django import template
from django.utils.safestring import mark_safe

from vocabulary.icon_registry import icon_html, resolve_icon, topic_icon_html

register = template.Library()


@register.simple_tag
def bs_icon(name, variant=None, size="md", extra_class=""):
    return mark_safe(icon_html(name, variant, size=size, extra_class=extra_class))


@register.simple_tag
def bs_topic_icon(topic, size="md"):
    return mark_safe(topic_icon_html(topic, size=size))


@register.filter
def icon_slug(value):
    return resolve_icon(value)
