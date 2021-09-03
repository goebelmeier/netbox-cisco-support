from datetime import datetime, date
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def is_expired(value):
    return value < datetime.now().date()


def expires_next_year(value):
    return value < date(date.today().year + 1, 12, 31)


@register.filter(is_safe=True)
def expiration_class(value):
    if is_expired(value):
        return mark_safe('class="danger"')
    elif expires_next_year(value):
        return mark_safe('class="warning"')
    else:
        return


@register.filter(is_safe=True)
def coverage_class(value):
    print(value)

    if not value:
        return mark_safe('class="danger"')
