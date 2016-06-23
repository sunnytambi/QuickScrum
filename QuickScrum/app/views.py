"""
Definition of views.
"""

from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from datetime import datetime
from django.views.decorators.csrf import csrf_protect
from django.http import HttpRequest
from django.http.response import HttpResponseRedirect, HttpResponse
from django.utils.timezone import now
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.forms.forms import NON_FIELD_ERRORS
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from app.forms import StatusForm, BootstrapAuthenticationForm
from app.models import YesterdayStatus, TodayStatus, IssueStatus, Status
from QuickScrum import settings


@csrf_protect
def login_view(request, template_name, authentication_form, extra_context):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                # User login successful
                messages.success(request, 'Successfully Logged in')
                form = StatusForm(auto_id=False)
                nexturl = settings.LOGIN_REDIRECT_URL
                if request.GET.get('next', False):
                    nexturl = request.GET.get('next', False)
                return redirect(nexturl,
                                {
                                    'title':'Log your Status',
                                    'year':now().year,
                                    'form':form,
                                })
            else:
                # Return a 'disabled account' error message
                return render(request, 
                              template_name, 
                              {'title':'Sign in', 'year':now().year, 'form':authentication_form})
        else:
            # Return an 'invalid login' error message.
            form = authentication_form()
            form.full_clean()
            form.errors[NON_FIELD_ERRORS] = form.error_class(['Invalid login details supplied'])
            #form.add_error(field=None, error="Invalid login details supplied")
            return render(request, 
                          template_name, 
                          {'title':'Sign in', 'year':now().year, 'form':form})
            #return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 
                      template_name, 
                      {'title':'Sign in', 'year':now().year, 'form':authentication_form})
                      #context = RequestContext(request,
                      #                        {
                      #                            'title':'Sign in',
                      #                            'year':now().year,
                      #                            'form':authentication_form,
                      #                        }))

@login_required
@csrf_protect
def status_view(request):
    """Renders the status page."""
    assert isinstance(request, HttpRequest)
    form = StatusForm(request.POST or None, auto_id=False)

    if request.method == 'POST':
        if form.is_valid():
            s = Status()
            s.timestamp = now()
            s.submitter = request.user
            s.save()

            ylist = request.POST.getlist('yesterday')
            tlist = request.POST.getlist('today')
            ilist = request.POST.getlist('issue')

            for y in ylist:
                m = YesterdayStatus()
                m.status_text = y
                m.status = s
                m.save()

            for t in tlist:
                m = TodayStatus()
                m.status_text = t
                m.status = s
                m.save()

            for i in ilist:
                m = IssueStatus()
                m.status_text = i
                m.status = s
                m.save()

            messages.success(request, 'Statuses submitted successfully')
    
    return render(request, "app/status.html",
            {
                'title':'Log your Status',
                'year':now().year,
                'form':form,
            })

#@login_required
def readstatus_view(request, status_id):
    """Renders the status page in Read Only mode."""
    assert isinstance(request, HttpRequest)

    s = Status.objects.filter(id=status_id).first()
    ylist = YesterdayStatus.objects.filter(status_id=status_id)
    tlist = TodayStatus.objects.filter(status_id=status_id)
    ilist = IssueStatus.objects.filter(status_id=status_id)

    return render(request,
        'app/readstatus.html',
        {
            'title':'Status Submitted on %s' % s.timestamp,
            'year':now().year,
            'yesterday_list':ylist,
            'today_list':tlist,
            'issue_list':ilist,
        })

#@login_required
def dashboard_view(request):
    """Renders the dashboard page."""
    assert isinstance(request, HttpRequest)
    statuses = Status.objects.filter(submitter=request.user)
    return render(request,
        'app/dashboard.html',
        {
            'title':'Dashboard',
            'year':now().year,
            'statuses':statuses,
        })