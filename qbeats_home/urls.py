__author__ = 'ShadowTrader'

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('qbeats_home.views',

                       #url(r'^$', 'qbeats_home', name='request'),
                       url(r'^$', TemplateView.as_view(template_name='qbeats_home/index_2.html'), name='homepage'),
                       url(r'^contact-us$', TemplateView.as_view(template_name='qbeats_home/contact.html'), name='contact_us'),

                       )
