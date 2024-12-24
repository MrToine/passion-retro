from django import template
from commons.bbcode_parser import BBCodeParser

register = template.Library()

@register.filter(name='bbcode')
def bbcode(value):
    parser = BBCodeParser()
    return parser.parse(value)