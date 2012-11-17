from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import admin




admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webservices.views.home', name='home'),
    # url(r'^webservices/', include('webservices.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^knowledge/', include('knowledge.urls')),
#    url(r'^feedback/', include('feedback.urls')),
    url(r'^forms/', include('forms.urls')),
    (r'^facebook/', include('django_facebook.urls')),
    (r'^accounts/', include('django_facebook.auth_urls')), 



)
