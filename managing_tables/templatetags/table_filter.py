from django import template

register = template.Library()


@register.filter
def length(values):
    return len(values)


@register.filter
def mod(value):
    return value % 2


def count(values, i):
    new_values = []
    for value in values:
        if value.wins > i:
            new_values.append(value)
    return new_values


@register.filter
def count_wins1(values):
    return count(values, 0)


@register.filter
def count_wins2(values):
    return count(values, 1)


@register.filter
def count_wins3(values):
    return count(values, 2)


@register.filter
def count_wins4(values):
    return count(values, 3)


@register.filter
def count_wins5(values):
    return count(values, 4)


@register.filter
def count_wins6(values):
    return count(values, 5)


@register.filter
def count_wins7(values):
    return count(values, 6)


@register.filter
def count_wins21(values):
    return count(values, 0)


@register.filter
def count_wins22(values):
    return count(values, 2)


@register.filter
def count_wins23(values):
    return count(values, 4)


@register.filter
def count_wins24(values):
    return count(values, 6)


@register.filter
def count_wins25(values):
    return count(values, 8)


@register.filter
def count_wins26(values):
    return count(values, 10)


@register.filter
def count_wins27(values):
    return count(values, 12)
