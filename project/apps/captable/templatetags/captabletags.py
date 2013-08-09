from django import template

register = template.Library()


@register.filter(name='percentage')
def percentage(value):
    """Returns the number as percentage with two-digit precision"""
    try:
        value = float(value)
    except (ValueError, TypeError, UnicodeEncodeError):
        return ''
    return '{0:.2%}'.format(value)


@register.filter(name='currency')
def currency(dollars):
    """Returns in US-Currency notation, with two-digit precision"""
    try:
        dollars = round(float(dollars), 2)
    except (ValueError, TypeError, UnicodeEncodeError):
        return ''
    return '${0:,.2f}'.format(dollars)


@register.filter(name='shares')
def shares(shares):
    """Returns integer with comma notation"""
    try:
        shares = int(shares)
    except (ValueError, TypeError, UnicodeEncodeError):
        return ''
    return '{0:,}'.format(shares)


@register.filter(name='price')
def price(value):
    """Returns the number as decimal with 5-digit precision"""
    try:
        value = round(float(value), 5)
    except (ValueError, TypeError, UnicodeEncodeError):
        return ''
    return '${0:0.5f}'.format(value)


@register.filter(name='mils')
def mils(value):
    """Returns number in millions of dollars"""
    try:
        value = float(value) / 1000000
    except (ValueError, TypeError, UnicodeEncodeError):
        return ''
    return '${0:,}M'.format(value)


@register.filter(name='ratio')
def ratio(value):
    """Returns single-digit ratio"""
    try:
        value = float(value)
    except (ValueError, TypeError, UnicodeEncodeError):
        return ''
    return '{0:0.1f}'.format(value)

