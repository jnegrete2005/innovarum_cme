from django.template import Library

register = Library()


@register.filter()
def times(ls: list):
  return range(len(ls))


@register.filter()
def get_item(ls: list, i):
  return ls[i]
