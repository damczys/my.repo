from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
     url(r'^', include('Blog.tools.urls'), {'SSL':True}),
     url(r'^', include('Blog.comments.urls'), {'SSL':True}),
     url(r'^', include('Blog.index.urls'), {'SSL':True}),
     url(r'^blog/', include('Blog.blog.urls'), {'SSL':True}),
)
