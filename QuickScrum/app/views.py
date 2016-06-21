"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

def status(request):
    """Renders the status page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/status.html',
        context_instance = RequestContext(request,
        {
            'title':'Log your Status',
            'year':datetime.now().year,
        })
    )

def readstatus(request):
    """Renders the status page in Read Only mode."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/readstatus.html',
        context_instance = RequestContext(request,
        {
            'title':'Status Submitted on 03/03/2016',
            'year':datetime.now().year,
        })
    )

def dashboard(request):
    """Renders the dashboard page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/dashboard.html',
        context_instance = RequestContext(request,
        {
            'title':'Dashboard',
            'year':datetime.now().year,
        })
    )

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )
