from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import admin
from django.conf import settings
from django.contrib.auth.views import login
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
    url(r'^articles/', include('articles.urls')),
#    url(r'^feedback/', include('feedback.urls')),
#    (r'^facebook/', include('django_facebook.urls')),
#    (r'^accounts/', include('django_facebook.auth_urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url': '/accounts/login/'}, name='logout'),
#    url(r'^accounts/login/$', login(template_name="login.html"), name='login'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
