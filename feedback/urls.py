from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('knowledge.views',
    url(r'^demo/$', direct_to_template, {'template': 'feedback/demo.html'}),
    url(r'^feedback-form/$', direct_to_template, {'template': 'feedback/feedback-form.html'}),
)
