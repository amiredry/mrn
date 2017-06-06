__author__ = 'ShadowTrader'
from django.conf.urls import patterns, url


urlpatterns = patterns('newsfirst.views',

    url(r'^$', 'get_apfirst_stories', name='news_first'),
    url(r'^news_updates/(?P<hash2>.+)$', 'get_latest_stories', name='get-latest-story'),
    url(r'^apfirst/(?P<hash2>.+)$', 'get_story', name='get-story'),
    url(r'^test$', 'test')

)

