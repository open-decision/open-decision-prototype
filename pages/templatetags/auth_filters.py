from django import template

register = template.Library()

# Attributes can only be added once therefore css and placeholder are set together

@register.filter(name='addclass')
def addclass(value, args):
    if args is None:
        return False
    print (args)
    arg_list = [arg.strip() for arg in args.split(';')]
    print (arg_list[1])
    return value.as_widget(attrs={'class': arg_list[0], 'placeholder': arg_list[1]})
