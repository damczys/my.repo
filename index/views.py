#vim: set fileencoding=utf-8
from django.shortcuts import render
from django.db import IntegrityError, connection, transaction
import models
import forms
from django.contrib.auth import models as user_model
# Create your views here.
from django.views.generic import View
from django.views.generic.edit import FormView, CreateView
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from Blog.tools.views import BaseView
from Blog.tools.jsonconverter import fromJSON
from django.core.urlresolvers import reverse_lazy
from base64 import urlsafe_b64decode
import datetime
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from Blog.comments.views import dictfetchall, get_comments, get_comment, add_comments, get_comments_form, delete_comment, add_reply, update_comment
from xml.dom import VALIDATION_ERR
from django.db import IntegrityError
from django.core.exceptions import ValidationError

footer_value = models.Var.objects.filter(name='footer_value')[0].var
item_for_page = int(models.Var.objects.filter(name='item_for_page')[0].var)
default_page_number = int(models.Var.objects.filter(name='default_page')[0].var)
    
class Index(BaseView):
  def get(self, request, *args, **kwargs):
    super(Index, self).get(request, *args, **kwargs)
    return render_to_response(self.template_name, self.view_data, content_type="HTML5", context_instance = RequestContext(request))
  
index = Index.as_view(template_name='index.html',
                      page_view ='index',
                      item_for_page = item_for_page,
                      default_page_number = default_page_number,
                      footer_value = footer_value,
                      model = models.Note,
                      order_by=['-date_add',],
                      )
  
class AddNews(FormView):
  success_url = reverse_lazy('index')
  form_class = forms.NewsForm
  tag_form_class = forms.NewsTagForm
  template_name = 'add_news.html'
  
  @method_decorator(login_required)
  def get(self, request, *args, **kwargs):
    form = self.form_class()
    tagform = self.tag_form_class()
    return render_to_response(self.template_name, {'request':request, 'form':form, 'tagform':tagform}, content_type="HTML5", context_instance = RequestContext(request))
  
  @method_decorator(login_required)
  def post(self, request, *args, **kwargs):
    data=request.POST.dict()
    form = self.form_class(data)
    tagform = self.tag_form_class(data)
    tags=data['tags'].split(';')
    if form.is_valid() and tagform.is_valid():
      form.save()
      where={'topic':data['topic'], 'note':data['note']}
      note = models.Note.objects.get(**where)
      tags2=[]
      for tag in tags:
        tagobj=models.Tag(name=tag.strip())
        try:
          tagobj.save()
        except IntegrityError:
          tagobj=models.Tag.objects.get(name=tag.strip())
        tags2.append(tagobj)
      if len(tags2)>0:
        for tag in tags2:
          models.Group(note=note, tag=tag, author=request.user).save()
      else:
        models.Group(note=note).save()
      return redirect(self.success_url)
    return render(request, self.template_name, {'request':request, 'form':form, 'tagform':tagform})

add_news = AddNews.as_view()

class ShowNews(View):
  template_name='show_news.html'
  
  def get(self, request, *args, **kwargs):
    news = models.Note.objects.get(id=kwargs['newsid'])
    init={'note':news.pk}
    comments_form = get_comments_form(request, **init)
    comments = get_comments(news.pk)
    return render_to_response(self.template_name, {'request':request, 'news':news, 'comments_form':comments_form, 'comments':comments, 'deep':0, 'footer_value':footer_value}, content_type="HTML5", context_instance = RequestContext(request))
  
  def post(self, request, *args, **kwargs):
    add_comments(request)
    return HttpResponseRedirect(request.path)
  
show_news = ShowNews.as_view()

class ShowNewsByTag(BaseView):
  def get(self, request, *args, **kwargs):
    super(ShowNewsByTag, self).get(request, *args, **kwargs)
    cursor = connection.cursor()
    cursor.execute("SELECT tools_group.id, tools_note.id as pk, tools_note.topic, tools_note.note, tools_note.date_add, tools_tag.name FROM tools_group LEFT JOIN tools_note on tools_note.id=tools_group.note_id LEFT JOIN tools_tag on tools_tag.id=tools_group.tag_id WHERE tools_tag.name='%s' ORDER BY date_add DESC" % fromJSON( urlsafe_b64decode( str(kwargs['tag']) ) ))
    data = dictfetchall(cursor)
    self.view_data['data']=data
    return render_to_response(self.template_name, self.view_data, content_type="HTML5", context_instance = RequestContext(request))
  
show_news_by_tag = ShowNewsByTag.as_view(template_name='index.html',
                      page_view ='news/show/by/tag',
                      item_for_page = item_for_page,
                      default_page_number = default_page_number,
                      footer_value = footer_value,
                      model = models.Group,
                      order_by = ['-date_add',],
                      )

class Login(FormView):
  template_name = 'login.html'
  form_class = forms.LoginForm
  success_url = reverse_lazy('index')
  
  def get(self, request, *args, **kwargs):
    return render_to_response(self.template_name, {'request':request, 'form':self.form_class(), 'footer_value':footer_value}, content_type="HTML5", context_instance = RequestContext(request))
  
  def post(self, request, *args, **kwargs):
    if request.user.is_authenticated():
      return HttpResponseRedirect(self.success_url)
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    login_failed = True
    if user is None:
      return render_to_response(self.template_name, {'request':request, 'form':self.form_class(request.POST), 'login_failed':login_failed}, content_type="HTML5", context_instance = RequestContext(request))
    if user.is_active:
      auth.login(request, user)
      login_failed = False
      return HttpResponseRedirect(self.success_url)
    else:
      return render(request, 'info.html', {'request':request, 'back_url':'index', 'errors':[_('Konto jest nieaktywne.'), ]})
      
login = Login.as_view()

class Registration(CreateView):#FormView):
    template_name = 'rejestracja.html'
    form_class = forms.RegisterForm
    success_url = reverse_lazy('index')
    
    """def get(self, request, *args, **kwargs):
        return render_to_response(self.template_name, {'request':request, 'form':self.form_class(), 'footer_value':footer_value}, content_type="HTML5", context_instance = RequestContext(request))"""
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form.password2=request.POST['password2']
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        return render_to_response(self.template_name, {'form':form}, content_type="HTML5", context_instance = RequestContext(request))
         
        
registration = Registration.as_view()
class Logout(View):
  success_url = reverse_lazy('index')
  
  @method_decorator(login_required)
  def get(self, request, *args, **kwargs):
    auth.logout(request)
    return HttpResponseRedirect(self.success_url)
  
logout = Logout.as_view()



class DeleteNews(View):
  success_url = reverse_lazy('index')
  template_name = 'delete_news.html'
  
  @method_decorator(login_required)
  def get(self, request, *args, **kwargs):
    return render_to_response(self.template_name, {'request':request, 'pk':kwargs['pk']}, content_type="HTML5", context_instance = RequestContext(request))
  
  @method_decorator(login_required)
  @method_decorator(transaction.atomic)
  def post(self, request, *args, **kwargs):
    pk=kwargs['pk']
    group = models.Group.objects.filter(note_id=pk)
    for item in group:
      item.delete()
    models.Note.objects.get(id=pk).delete()      
    return HttpResponseRedirect(self.success_url)

delete_news = DeleteNews.as_view()

class EditNews(View):
  success_url = reverse_lazy('index')
  form_class = forms.NewsFormEdit
  tag_form_class = forms.NewsTagForm
  template_name = 'add_news.html'
  
  @method_decorator(login_required)
  def get(self, request, *args, **kwargs):
    news = models.Note.objects.get(id=kwargs['pk'])
    group = models.Group.objects.filter(note_id=kwargs['pk'])
    form = self.form_class(initial={
                                    'date_change':str(datetime.datetime.now()),
                                    'topic':news.topic,
                                    'note':news.note,
                                    })
    tagslist=[]
    for item in group:
      tagslist.append(item.tag.name)
    tagform = self.tag_form_class(initial={'tags':'; '.join(tagslist)})
    return render_to_response(self.template_name, {'request':request, 'form':form, 'tagform':tagform, 'pk':kwargs['pk'], 'footer_value':footer_value}, content_type="HTML5", context_instance = RequestContext(request))
  
  @method_decorator(login_required)
  def post(self, request, *args, **kwargs):
    data=request.POST.dict()
    form = self.form_class(data)
    tagform = self.tag_form_class(data)
    #Magiczna akcja najpierw pozbywam się średników
    #następnie łaczę wszystko białymi znakami
    #a następnie usuwam białe znaki
    #bo mogą się pojawić białe znaki
    tags=set((' '.join((data['tags'].split(';')))).split())
    if len(tags)>5:
      return render(request, self.template_name, {'request':request, 'form':form, 'tagform':tagform, 'tagserror':True, 'pk':kwargs['pk'], 'footer_value':footer_value})
    news = models.Note.objects.get(id=kwargs['pk'])
    news.topic = data['topic']
    news.note = data['note']
    news.date_change = data['date_change']
    news.save()
    where={'topic':data['topic'], 'note':data['note'], 'date_change':data['date_change']}
    note = models.Note.objects.get(**where)
    models.Group.objects.filter(note=note).delete()
    tags2=[]
    for tag in tags:
      tagobj=models.Tag(name=tag)
      try:
        tagobj.save()
      except IntegrityError:
        tagobj=models.Tag.objects.get(name=tag.strip())
      tags2.append(tagobj)
    if len(tags2)>0:
      for tag in tags2:
        models.Group(note=note, tag=tag, author=request.user).save()
    else:
      models.Group(note=note).save()
    return redirect(self.success_url)
    return render(request, self.template_name, {'request':request, 'form':form, 'tagform':tagform, 'footer_value':footer_value})
  
edit_news = EditNews.as_view()
    
    
class CommentDelete(View):
  template_name = 'delete_comment.html'
  
  @method_decorator(login_required)
  def get(self, request, *args, **kwargs):
    return render_to_response(self.template_name, {'request':request, 'back_url':kwargs['back_url'], 'footer_value':footer_value}, content_type="HTML5", context_instance = RequestContext(request))

  @method_decorator(login_required)
  def post(self, request, *args, **kwargs):
    delete_comment(kwargs['pk'])
    return redirect(kwargs['back_url'])

comment_delete = CommentDelete.as_view()

class ReplyAdd(View):
  template_name='reply_add.html'
  
  @method_decorator(login_required)
  def get(self, request, *args, **kwargs):
    news = models.Note.objects.get(id=kwargs['newsid'])
    init={'note':news.pk}
    comments_form = get_comments_form(request, **init)
    comments = get_comments(news.pk)
    return render_to_response(self.template_name, {'request':request, 'news':news, 'comments_form':comments_form, 'comments':comments, 'deep':0, 'back_url':kwargs['back_url'], 'footer_value':footer_value}, content_type="HTML5", context_instance = RequestContext(request))
  
  @method_decorator(login_required)
  def post(self, request, *args, **kwargs):
    add_reply(request, *args, **kwargs)
    return redirect(kwargs['back_url'])
  
reply_add = ReplyAdd.as_view()
  
class UpdateComment(View):
  template_name='edit_comment.html'
  def get(self, request, *args, **kwargs):
    comment = get_comment(kwargs['pk'])
    init={'id':comment.pk, 'note':comment.note, 'comment':comment.comment }
    comments_form = get_comments_form(request, update=True, **init)
    return render_to_response(self.template_name, {'request':request, 'comments_form':comments_form, 'footer_value':footer_value, 'comment':comment, 'back_url':kwargs['back_url']}, content_type="HTML5", context_instance = RequestContext(request))
    
  def post(self, request, *args, **kwargs):
    update_comment(request)
    return redirect(kwargs['back_url'])
  
comment_update = UpdateComment.as_view()

class Profile_view(View):
    template_name='profileview.html'
    def profile_clean(self,request, username):
        u = User.objects.get(username=username)
        return render_to_response(self.template_name , content_type="HTML5", context_instance = RequestContext(request))
        
profile_view = Profile_view.as_view()


