from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def strip_error_msg(arg):
    if arg:
        return arg[0][0]
    else:
        return ""


@register.simple_tag
def show_error_msg(arg):
    if arg:
        # ValidationError object does not support indexing,需要转一下格式
        error_msg = tuple(arg[0])[0]
        result = '<div class="my-alert alert-danger" role="alert">{}</div>'.format(error_msg)
        return mark_safe(result)
    else:
        return ""
