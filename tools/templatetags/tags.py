from django.template import Library
register = Library()
from Blog.tools import models

@register.inclusion_tag('tags.html')
def tags(note):
  if not isinstance(note, dict):
    tags = models.Group.objects.filter(note=note)
    tagslist = []
  else:
    tags = models.Group.objects.filter(note_id=note['pk'])
    tagslist = []
    
  for item in tags:
    tagslist.append(item.tag.name)
  return {'tagslist':tagslist}