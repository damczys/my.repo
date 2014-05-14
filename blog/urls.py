from django.conf.urls import patterns, url



urlpatterns = patterns('Blog.blog.views',
    url(r'^index', 'user_blog_index', name='user_blog_index'),    
)
