#-*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from exceptions import Exception
import models

class ClearForm(object):  
  def clean_comment(self):
    print "clear"
    comment = self.cleaned_data.get('comment')
    if len(comment)==0:
      raise ValidationError(_('Komentarz nie może być pusty!'))
    return self.cleaned_data.get('comment')

class CommentNotLogged(ModelForm, ClearForm):
  class Meta:
    model = models.Comments
    fields = ['not_logged_user', 'comment', 'note']
    labels = {
              'not_logged_user':_(u'Użytkownik'),
              'comment':_(u'Komentarz'),
              }
    widgets = {
               'note':forms.HiddenInput(),
               }
      
class CommentLogged(ModelForm, ClearForm):
  class Meta:
    model = models.Comments
    fields = ['logged_user', 'comment', 'note']
    labels = {
              'logged_user':_(u'Użytkownik'),
              'comment':_(u'Komentarz'),
              }
    widgets = {
               'logged_user':forms.HiddenInput(),
               'note':forms.HiddenInput(),
               }
    
class CommentUpdate(ModelForm, ClearForm):
  id = forms.CharField(widget=forms.HiddenInput())
  class Meta:
    model = models.Comments
    fields = ['comment', 'note']
    labels = {
              'comment':_(u'Komentarz'),
              }
    widgets = {
               'note':forms.HiddenInput(),
               }