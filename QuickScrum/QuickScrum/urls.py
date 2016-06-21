"""
Definition of urls for QuickScrum.
"""

from datetime import datetime
from django.conf.urls import patterns, include, url
from app.forms import BootstrapAuthenticationForm
from app.views import status, readstatus, dashboard, home, contact, about

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth.views import login, logout
admin.autodiscover()

urlpatterns = [
    url(r'^$', status, name='status'),
    url(r'^status/$', status, name='status'),
    url(r'^readstatus/$', readstatus, name='readstatus'),
    url(r'^dashboard$', dashboard, name='dashboard'),

    url(r'^home$', home, name='home'),
    url(r'^contact$', contact, name='contact'),
    url(r'^about$', about, name='about'),
    url(r'^login/$',
        login,
        {
            'template_name': 'app/Signin.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Sign in',
                'year':datetime.now().year,
            }
        },
        name='login'),
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
