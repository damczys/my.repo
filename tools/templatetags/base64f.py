from django.template import Library
from base64 import urlsafe_b64encode
from Blog.tools.jsonconverter import toJSON
from django.template.defaultfilters import stringfilter
register = Library()

@register.filter
@stringfilter
def base64f(string):
  return urlsafe_b64encode(toJSON(string))