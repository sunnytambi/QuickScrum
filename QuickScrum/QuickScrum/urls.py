"""
Definition of urls for QuickScrum.
"""

from django.conf.urls import include, url
from app.forms import BootstrapAuthenticationForm, JiraAuthenticationForm, BootstrapRegisterForm, BootstrapPasswordChangeForm
from app.views import status_view, readstatus_view, dashboard_view, login_view, jiralogin_view, register_view, password_change_view

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth.views import logout, password_reset, password_reset_confirm, password_reset_done, password_reset_complete
from django.utils.timezone import now
admin.autodiscover()

urlpatterns = [
    url(r'^$', status_view, name='status'),
    url(r'^status/$', status_view, name='status'),
    url(r'^readstatus/(?P<status_id>\w+)/$', readstatus_view, name='readstatus'),
    url(r'^dashboard$', dashboard_view, name='dashboard'),

    #url(r'^home$', home, name='home'),
    #url(r'^contact$', contact, name='contact'),
    #url(r'^about$', about, name='about'),
    url(r'^login$', login_view, {
        'template_name': 'app/Signin.html',
        'authentication_form': BootstrapAuthenticationForm,
        'extra_context':
        {
            'title':'Sign in',
            'year':now().year,
        },
    }, name='login'),

    url(r'^register$', register_view, {
        'template_name': 'app/register.html',
        'register_form': BootstrapRegisterForm,
        'extra_context':
        {
            'title':'Register',
            'year':now().year,
        },
    }, name='register'),

    url(r'^password_change/$', password_change_view, {
        'template_name': 'app/passwordchange.html',
        'password_change_form': BootstrapPasswordChangeForm,
        'extra_context':
        {
            'title':'Change Password',
            'year':now().year,
        },
    }, name='password_change'),

    url(r'^jiralogin$', jiralogin_view, {
        'template_name': 'app/jirasignin.html',
        'authentication_form': BootstrapAuthenticationForm,
        'extra_context':
        {
            'title':'Sign in to Jira',
            'year':now().year,
        },
    }, name='jiralogin'),

    # TODO - Password Reset
    url(r'^password_reset/$', password_reset, {'post_reset_redirect' : '/password_reset/done/'}, name='password_reset'),
    url(r'^password_reset/done/$', password_reset_done),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'post_reset_redirect' : '/reset/done/'}),
    url(r'^reset/done/$', password_reset_complete),

    #url(r'^login$',
    #    login,
    #    {
    #        'template_name': 'app/login.html',
    #        'authentication_form': BootstrapAuthenticationForm,
    #        'extra_context':
    #        {
    #            'title':'Sign in',
    #            'year':now().year,
    #        },
    #    },
    #    name='login'),
    url(r'^logout$',
        logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]
