# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'captor_mesh.mesh.views.index', name='home'),
    url(r'^gauge/(?P<arduino_id>\d+)/$', 'captor_mesh.mesh.views.gauge', name='gauge'),
    url(r'^gauge_api/(?P<arduino_id>\d+)/$', 'captor_mesh.mesh.views.gauge_api', name='gauge_api'),
    url(r'^line/(?P<arduino_id>\d+)/$', 'captor_mesh.mesh.views.line', name='line'),
    url(r'^line_api/(?P<arduino_id>\d+)/$', 'captor_mesh.mesh.views.line_api', name='line_api'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),)
