from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gea.views.home', name='home'),
    # url(r'^gea/', include('gea.foo.urls')),

	url(r'^new/', 'qpcr.views.newRun'),
)
