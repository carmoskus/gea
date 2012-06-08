from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView, UpdateView
from qpcr.models import Run

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gea.views.home', name='home'),
    # url(r'^gea/', include('gea.foo.urls')),

	url(r'^new-run/?$', 'qpcr.views.new_run'),
	url(r'^runs/?$', ListView.as_view(queryset=Run.objects.all(), context_object_name='runs', template_name='qpcr/run_list.html')),
	url(r'^runs/(?P<pk>\d+)/?$', DetailView.as_view(model=Run, template_name='qpcr/run_detail.html')),
	url(r'^runs/(?P<pk>\d+)/update/?$', UpdateView.as_view(model=Run, template_name='qpcr/run_update.html')),
	# r'^runs/(\d+)/average/?$'
)
