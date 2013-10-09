from django.conf.urls import patterns, include, url #, redirect_to
from django.views.generic.simple import redirect_to
from articles.views import *
# from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import admin
from django.conf import settings
# from django.contrib.auth.views import login
admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webservices.views.home', name='home'),
    # url(r'^webservices/', include('webservices.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^knowledge/', include('knowledge.urls')),
    # url(r'^forms/', include('forms.urls')),
    url(r'^articles/', include('articles.urls')),

    # url(r'^login/$',LoginRegisterView.as_view(), name='login'),
    # url(r'^login/$', 'django.contrib.auth.views.login', {'template_name':'login.html'}, name='login'),
    # url(r'^register/$',RegisterUserView.as_view(), name='register'),
    # url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url': '/login/'}, name='logout'),
    # url(r'^users/', include('articles.user_urls')),
    url(r'^$', redirect_to, {'url': '/articles/articles/'}),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^user/settings/$', UserSettingsView.as_view(), name="user_settings"),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))

handler500 = 'articles.views.test500'