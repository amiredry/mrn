from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

                       url(r'^',  include('qbeats_home.urls')),
                       url(r'^news/', include('newsfirst.urls')),
                       url(r'^captcha/', include('captcha.urls')),
                       url(r'^accounts/', include('custom_user_profile.urls')),
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                    )
