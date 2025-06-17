from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def has_group(context, group_name):
    user = context['user']
    return user.groups.filter(name=group_name).exists()

@register.simple_tag(takes_context=True)
def has_perm(context, perm_name):
    user = context['user']
    return user.has_perm(perm_name)
