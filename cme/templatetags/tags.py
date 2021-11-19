from django.template import Library
from ..views import MODULE_CODE_TO_TEXT

register = Library()


@register.filter()
def times(ls: list):
  return range(len(ls))


@register.filter()
def get_item(ls: list, i):
  return ls[i]


@register.filter()
def get_module(code: str):
  return MODULE_CODE_TO_TEXT[code]
