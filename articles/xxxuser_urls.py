from django.conf.urls import patterns, url, include
from articles.views import *

urlpatterns = patterns('',
    url(r'^(?P<username>[-\w]+)/(?P<pk>\d+)/$', UserUpdateView.as_view(template_name='articles/user_form.html'), name='user_update')
)
