#-*- coding: utf-8 -*-
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from Blog.tools.models import Note

class Comments(models.Model):
  logged_user = models.ForeignKey(User, null=True)
  not_logged_user = models.CharField(max_length=30, null=True, validators=[RegexValidator(regex='^.{3,30}$', message=_(u'Nazwa musi posiadać przynajmniej 3 znaki i maksymalnie 30'), code='nomatch')])
  note = models.ForeignKey(Note, null=False, blank=False)
  comment = models.TextField()
  date_add = models.DateTimeField(auto_now=True)
  date_change = models.DateTimeField(auto_created=True, null=True)
  
class CommentsReply(models.Model):
  comment = models.ForeignKey('Comments', null=False, blank=False, related_name='base_comment')
  reply = models.ForeignKey('Comments', null=False, blank=False, related_name='reply')
