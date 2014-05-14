from django.template import Library
register = Library()
from Blog.tools import models
from django.db import connection
from Blog.index.views import dictfetchall

@register.inclusion_tag('comments.html')
def comments(news_pk, comment_id, **kwargs):
  deep=int(kwargs['deep'])
  deep+=1
  cursor = connection.cursor()
  cursor.execute("""SELECT comments_comments.id, comments_comments.date_add, comments_comments.date_change, comments_comments.not_logged_user, comments_comments.note_id, comments_comments.comment, auth_user.username FROM comments_commentsreply
  JOIN comments_comments ON comments_commentsreply.reply_id=comments_comments.id
  LEFT JOIN auth_user ON comments_comments.logged_user_id=auth_user.id
  WHERE comments_comments.note_id=%s and comments_commentsreply.comment_id=%s
  ORDER BY comments_comments.date_add 
  """ % (news_pk, comment_id))
  comments = dictfetchall(cursor)
  return {'comments':comments, 'deep':deep, 'news':{'pk':news_pk}, 'request':kwargs['request'], 'perms':kwargs['perms']}