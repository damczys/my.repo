from django.template import Library
register = Library()
from Blog.tools import models

@register.inclusion_tag('author.html')
def author(note):
  newsauthor = None
  if not isinstance(note, dict):
    newsauthor = models.Group.objects.filter(note=note)
  else:
    newsauthor = models.Group.objects.filter(note_id=note['pk'])
    
    print newsauthor
    
  for item in newsauthor:
    newsauthor = item.author
    break
  return {'author':newsauthor}