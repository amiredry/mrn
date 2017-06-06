__author__ = 'ShadowTrader'
from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from views import RegistrationView, ProfileView, ActivationView
from django.views.generic.base import TemplateView


extra_auth_patterns = patterns('',

    url(r'^login/$', auth_views.login, {'template_name': 'qb_registration/login_2.html'}, name='auth_login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'qb_registration/logout.html'}, name='auth_logout'),
    url(r'^password/change/$', auth_views.password_change, name='auth_password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done, name='auth_password_change_done'),
    url(r'^password/reset/$', auth_views.password_reset, {'template_name': 'qb_registration/password_reset_form.html',
                                                          'email_template_name': 'qb_registration/password_reset_email.html', 'subject_template_name':'qb_registration/password_reset_subject.txt' }, name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',auth_views.password_reset_confirm, {'template_name': 'qb_registration/password_reset_confirm.html'} ,name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$',auth_views.password_reset_complete, {'template_name': 'qb_registration/password_reset_complete.html'},name='auth_password_reset_complete'),
    url(r'^password/reset/done/$',auth_views.password_reset_done, {'template_name': 'qb_registration/password_reset_done.html'}, name='auth_password_reset_done'),
)

extra_activation_patterns = patterns('',
    url(r'^activate/(?P<activation_key>\w+)/$', ActivationView , name='registration_activate'),
    url(r'^activate/complete/$', TemplateView.as_view(template_name='qb_registration/activation_complete.html'), name='registration_activation_complete'),
)

urlpatterns = patterns('',

    #url(r'^captcha/', include('captcha.urls')),
    #url(r'^$', 'HomePage', name='author_add'),
    url(r'^register/$',  RegistrationView.as_view(), name='auth_register'),
    url(r'^profile/$', ProfileView.as_view(), name='userprofiles_profile'),

    url(r'^register/complete/$',TemplateView.as_view(template_name='qb_registration/registration_complete.html'), name='registration_complete'),

    url(r'^', include(extra_auth_patterns)),
    url(r'^', include(extra_activation_patterns)),

)