from django import template
from django.utils.translation import gettext_lazy as _


register = template.Library()

# Attributes can only be added once therefore css and placeholder are set together

@register.filter(name='addclass')
def addclass(value, args):
    if args is None:
        return False
    arg_list = [arg.strip() for arg in args.split(';')]
    return value.as_widget(attrs={'class': arg_list[0], 'placeholder': eval(arg_list[1])})
