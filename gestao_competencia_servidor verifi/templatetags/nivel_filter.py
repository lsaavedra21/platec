from django import template

register = template.Library()

@register.filter
def nivel_texto(nivel):
    niveis = {
        '1': 'NA',
        '2': '0',
        '3': 'I',
        '4': 'L',
        '5': 'U',
    }
    return niveis.get(nivel, nivel)
