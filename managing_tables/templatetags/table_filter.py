from django import template

register = template.Library()


@register.filter
def length(values):
    return len(values)


@register.filter
def mod(value):
    return value % 2


@register.filter
def count_wins(values, i):
    new_values = []
    for value in values:
        if value.wins > i:
            new_values.append(value)
    return new_values
