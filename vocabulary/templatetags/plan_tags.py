from django import template

from boostingscore.plan_limits import user_can as check_user_can

register = template.Library()


@register.filter
def user_can(user, feature):
    return check_user_can(user, feature)
