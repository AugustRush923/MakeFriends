from django import template

register = template.Library()


@register.filter
def split(value: bytes, index) -> str:
    result = value.decode().split(":")
    return result[index]


@register.filter
def convert2int(value):
    return int(value)
