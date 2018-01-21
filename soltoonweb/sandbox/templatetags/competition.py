from django import template

register = template.Library()


@register.simple_tag
def get_opponent(value, me):
    for c in value:
        if not (c.user == me):
            return c
    return c

# register.tag('get_opponent', get_opponent)
