from django.conf.urls import patterns, url



urlpatterns = patterns('Blog.index.views',
    url(r'^$', 'index', name='index'),
    url(r'^index/$', 'index', name='index'),
    url(r'^index/(?P<page>\d*)/$', 'index', name='index'),
    url(r'^news/add', 'add_news', name='news/add'),
    url(r'^news/show/(?P<newsid>\d+)/$', 'show_news', name='news/show'),
    url(r'^news/show/by/tag/(?P<tag>.*)/$', 'show_news_by_tag', name='news/show/by/tag'),
    url(r'^news/delete/(?P<pk>\d+)/$', 'delete_news', name='news/delete'),
    url(r'^news/edit/(?P<pk>\d+)/$', 'edit_news', name='news/edit'),
    url(r'^comment/delete/(?P<pk>\d+)/(?P<back_url>/news/show/\d+/)/$', 'comment_delete', name='comment/delete'),
    url(r'^reply/add/(?P<newsid>\d+)/(?P<pk>\d+)/(?P<back_url>/news/show/\d+/)/$', 'reply_add', name='reply/add'),
    url(r'^comment/edit/(?P<pk>\d+)/(?P<back_url>/news/show/\d+/)/$', 'comment_update', name='comment/edit'),
    
)

urlpatterns += patterns('Blog.index.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^registration/$', 'registration', name='registration'),
    
)