from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('knowledge.views',
    url(r'^demo/$', direct_to_template, {'template': 'feedback/demo.html'}),
    url(r'^feedback-form/$', direct_to_template, {'template': 'feedback/feedback-form.html'}),
#    url(r'^submit-feedback/$', submit_feedback),
#    url(r'^screenshot/$', get_screenshot),
#    url(r'^get-related-results/$', get_related_results),

)
