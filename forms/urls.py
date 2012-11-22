from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template
from django.views.generic import TemplateView, ListView, DetailView
from views import *


urlpatterns = patterns('',
    url(r'^$', FormList.as_view(), name='forms'),
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/$', FormView.as_view(), name="form"),
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/$', FormView.as_view(), name="form-theme"),
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/thankyou/$', ThankYou.as_view(), name="thanks"),
    url(r'^new/$', CreateFormView.as_view(),name='new-form'),
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/edit/$', UpdateFormView.as_view(), name="form-edit"),
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/csv/$', ExportCSV.as_view(), name="csv"),
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/facebook/$', FacebookView.as_view(), name="facebook"),
    url(r'^(?P<pk>\d+)-(?P<slug>[-\w]+)/get/$', FormGetView.as_view(), name="form-get"),
)
