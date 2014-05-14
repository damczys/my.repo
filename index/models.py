from django.db import models

# Create your models here.

class Group(models.Model):
  class Meta:
    app_label='tools'
    
class Var(models.Model):
  class Meta:
    app_label='tools'

class Note(models.Model):
  class Meta:
    app_label='tools'
    
class Tag(models.Model):
  class Meta:
    app_label='tools'
    
class Comments(models.Model):
  class Meta:
    app_label='comments'