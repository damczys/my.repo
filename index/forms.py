#vim: set fileencoding=utf-8
from django import forms
from django.forms import ModelForm
import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.admin.forms import ERROR_MESSAGE

class NewsForm(ModelForm):
  class Meta:
    model = models.Note
    fields = ['topic', 'note']
    labels = {
              'topic':_(u'Temat'),
              'note':_(u'Wiadomość'),
              }
    
class NewsFormEdit(ModelForm):
  class Meta:
    model = models.Note
    fields = ['topic', 'note', 'date_change']
    labels = {
              'topic':_(u'Temat'),
              'note':_(u'Wiadomość'),
              }
    widgets = {
               'date_change':forms.HiddenInput(),
               }
    
class NewsTagForm(forms.Form):
  tags = forms.CharField(required=False, max_length=255, label=_(u'Tagi'))
  
  def clean_tags(self):
    tags = self.cleaned_data.get('tags').split(';')
    if len(tags)>5:
      raise ValidationError(_(u'Podano za dużo tagów!'), code='invalid')
    return self.cleaned_data.get('tags')


class LoginForm(forms.Form):
  username = forms.CharField(max_length=30, label=_(u'Login'))
  
  password = forms.CharField(
                          max_length = 32,
                          label=_(u'Hasło'),
                          widget = forms.PasswordInput(),
                          )
  

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
                   'password': forms.PasswordInput(),
                   }
    def save(self,commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit == True:
            user.save()
        return user
    
    def clean_password(self):
        print self.cleaned_data
        if self.cleaned_data['password'] != self.password2:
            raise ValidationError(_(u'Hasła nie są identyczne'), code='invalid')
        return self.cleaned_data['password']
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password2']=forms.CharField(label=_(u'Powtórz hasło'), widget=forms.PasswordInput())

