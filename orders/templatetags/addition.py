from django import template

register=template.Library()

@register.simple_tag(name='addition')
def addition(a,b):
    return a+b