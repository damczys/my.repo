#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
  topic = models.CharField(unique=True, max_length=100)
  date_add = models.DateTimeField(auto_now=True)
  date_change = models.DateTimeField(null=True)
  note = models.TextField()
  
class Tag(models.Model):
  name = models.CharField(unique=True, max_length=32)
  
class Group(models.Model):
  note = models.ForeignKey('Note', null=False, blank=False)
  tag = models.ForeignKey('Tag', null=True, blank=False)
  author = models.ForeignKey(User)
  
class Var(models.Model):
  name = models.CharField(max_length=100)
  var = models.CharField(max_length=100)
  