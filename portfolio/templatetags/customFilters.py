from django.template.defaultfilters import register
from datetime import datetime, date 


# register = template.Library()

@register.filter
def djangoDataToJs(value):
    if isinstance(value, datetime) or isinstance(value, date):
        return_value = 'new Date(\''+value.strftime('%Y-%m-%d')+'\')'
    elif isinstance(value, str):
        return_value = '\''+value +'\''
    else:
        return_value = value
    return return_value
