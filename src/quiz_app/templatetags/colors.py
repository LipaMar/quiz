from django import template

register = template.Library()

colors = ["primary", "secondary", "success", "danger", "warning", "info", "dark"]


@register.simple_tag
def color(a):
    return colors[a % 7]
