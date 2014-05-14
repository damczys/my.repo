#-*- coding: utf-8 -*-
from django.db import connection, DatabaseError
from forms import CommentLogged, CommentNotLogged, CommentUpdate
import models
import datetime
from django.utils.timezone import utc
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError

def dictfetchall(cursor):
  desc = cursor.description
  return [
      dict(zip([col[0] for col in desc], row))
      for row in cursor.fetchall()
  ]
  
def get_comments(news_pk):
  cursor = connection.cursor()
  cursor.execute("""SELECT comments_comments.id, comments_comments.date_add, comments_comments.date_change, comments_comments.not_logged_user, comments_comments.note_id, comments_comments.comment, auth_user.username FROM comments_comments LEFT JOIN auth_user ON comments_comments.logged_user_id=auth_user.id WHERE comments_comments.note_id=%s and not comments_comments.id in (SELECT reply_id FROM comments_commentsreply)""" % news_pk)
  return dictfetchall(cursor)

def get_comment(pk):
  return models.Comments.objects.get(id=pk)
  
def add_comments(request, update=False):
  data=request.POST
  if len(data['comment'])==0:
    raise DatabaseError(_(u'Komentarz nie może być pusty!'))
  comments_form=CommentNotLogged(data)
  if request.user.is_authenticated():
    comments_form=CommentLogged(data)
  if update==True:
    comment = models.Comments.objects.get(pk=int(data['id']))
    if comment is None:
      raise DatabaseError(_(u"Nastąpił nieprzewidziany błąd z bazą danych. Komentarz o numerze id = %s nie został znaleziony!" % data['id']))
    comment.comment=data['comment']
    comment.date_change=datetime.datetime.utcnow().replace(tzinfo=utc)
    return comment.save()
  if comments_form.is_valid():
    return comments_form.save()
    
def get_comments_form(request, update=False, **init):
  initial={}
  initial.update(init)
  comments_form=CommentNotLogged(initial=initial)
  if request.user.is_authenticated():
    initial={'logged_user':request.user.id}
    initial.update(init)
    comments_form=CommentLogged(initial=initial)
  if update==True:
    comments_form=CommentUpdate(initial=init)
  return comments_form

def add_reply(request, *args, **kwargs):
  data=request.POST
  base_comment_id=kwargs['pk']
  print data
  reply = add_comments(request)
  if reply is None:
    raise DatabaseError(_("Nastąpił nieprzewidziany problem z bazą danych"))
  base_comment = models.Comments.objects.get(id=base_comment_id)
  if base_comment is None:
    raise DatabaseError(_("Nastąpił nieprzewidziany problem z bazą danych"))
  comments_reply = models.CommentsReply(comment=base_comment, reply=reply)
  comments_reply.save()
    
def delete_comment(pk):
  replies = models.CommentsReply.objects.filter(comment_id=pk)
  for reply in replies:
    delete_comment( reply.reply_id )
  obj = models.Comments.objects.get(id=pk)
  obj.delete()
  
def update_comment(request):
  add_comments(request, update=True)