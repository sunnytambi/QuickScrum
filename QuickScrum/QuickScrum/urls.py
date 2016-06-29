"""
Definition of urls for QuickScrum.
"""

from django.conf.urls import include, url
from app.forms import BootstrapAuthenticationForm, JiraAuthenticationForm
from app.views import status_view, readstatus_view, dashboard_view, login_view, jiralogin_view

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth.views import logout
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

    url(r'^jiralogin$', jiralogin_view, {
        'template_name': 'app/jirasignin.html',
        'authentication_form': BootstrapAuthenticationForm,
        'extra_context':
        {
            'title':'Sign in to Jira',
            'year':now().year,
        },
    }, name='jiralogin'),

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
