#vim: set fileencoding=utf-8
from Blog.tools.views import BaseView
from Blog.tools import models
from django.utils.translation import ugettext_lazy as _
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext

class UserBlogIndex(BaseView):
    item_for_page = 10
    model = models.Group
    template_name = 'blog_index.html'
    page_view = 'user_blog_index'
    
    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user).order_by('note__date_add')
    
    def get(self, request, *args, **kwargs):
        super(UserBlogIndex, self).get(request, *args, **kwargs)
        return render_to_response(self.template_name, self.view_data, content_type="HTML5", context_instance = RequestContext(request))

user_blog_index = login_required(UserBlogIndex.as_view())
                
                        