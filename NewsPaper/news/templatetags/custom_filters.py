from django import template


register = template.Library()

censor_list = ['Abracadabra', 'From']

@register.filter()
def censor(value: str) -> str:
    for i in censor_list:
        value = value.replace(i, f'{i[0]}***{i[-1]}')
        value = value.replace(i.lower(), f'{i[0].lower()}***{i[-1]}')
    return f'{value}'

CURRENCIES_SYMBOLS = {
   'rub': 'Р',
   'usd': '$',
}


@register.filter()
def currency(value, code='rub'):
   """
   value: значение, к которому нужно применить фильтр
   code: код валюты
   """
   postfix = CURRENCIES_SYMBOLS[code]

   return f'{value} {postfix}'