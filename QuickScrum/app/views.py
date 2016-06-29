"""
Definition of views.
"""
import re
import app.jira.JiraIntegration
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpRequest
from django.utils.timezone import now
from django.forms.forms import NON_FIELD_ERRORS
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from app.forms import StatusForm
from app.models import YesterdayStatus, TodayStatus, IssueStatus, Status, Status_JiraIssue
from django.utils import timezone
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
                messages.success(request, 'Successfully Logged in to Quick Scrum')
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
                      {'title':extra_context['title'], 'year':extra_context['year'], 'form':authentication_form})

@login_required
@csrf_protect
def jiralogin_view(request, template_name, authentication_form, extra_context):

    if request.method == 'POST': # POST request

        #jiraurl = request.POST['jiraurl']
        username = request.POST['username']
        password = request.POST['password']

        jira_instance = app.jira.JiraIntegration.JiraIntegration()
        signin_success = jira_instance.signIn(settings.JIRA['site_url'], username, password)
        if signin_success: # Jira login successful, given credentials are correct
            messages.success(request, 'Successfully Logged in to Jira')
            request.session['jira_username'] = username
            request.session['jira_password'] = password
            #request.session['jiraurl'] = jiraurl

            jira_instance.signOut() # Credentials test pass, log user out.

            form = StatusForm(auto_id=False)
            nexturl = settings.LOGIN_REDIRECT_URL
            if request.GET.get('next', False):
                nexturl = request.GET.get('next', False)
            return redirect(nexturl,
                            {
                                'form':form,
                            })
        else: # Jira login failed. Possibly wrong credentials.
            form = authentication_form()
            #form.full_clean()
            form.errors[NON_FIELD_ERRORS] = form.error_class(['Jira credentials are incorrect. Please try again.'])
            return render(request,
                          template_name,
                          {'title':extra_context['title'], 'year':extra_context['year'], 'form':form})

    else: # GET request
        jira_credentials = request.session.get('jira_username', None)
        if jira_credentials is None:
            return render(request,
                          template_name,
                          {'title':extra_context['title'], 'year':extra_context['year'], 'form':authentication_form})
        else:
            return redirect('/status')


@login_required
@csrf_protect
def status_view(request):
    """Renders the status page."""
    assert isinstance(request, HttpRequest)

    form = StatusForm(request.POST or None, auto_id=False)
    issue_list = None

    if request.method == 'POST':
        if form.is_valid():
            s = Status()
            s.timestamp = now()
            s.submitter = request.user
            s.save()

            for key in list(request.POST.keys()):
                form_values = request.POST.getlist(key)
                modl = None

                if re.compile('csrfmiddlewaretoken').match(key):
                    # ignore
                    continue

                elif re.compile('yesterday_\d').match(key):
                    modl = YesterdayStatus()
                    for text in form_values:
                        modl.status_text = text
                        modl.status = s
                        modl.save()

                    jira_issues_list = request.POST.getlist('jira_issue_for_'+key)

                    for status_issue_value in jira_issues_list:
                        saveStatus_JiraIssue('Yesterday', s, status_issue_value, modl.id)
                        #s_ji = Status_JiraIssue()
                        #s_ji.status_type = 'Yesterday'
                        #s_ji.status = s
                        #s_ji.jira_issue_id = status_issue_value.split(']')[0][1:]
                        #s_ji.jira_issue_text = status_issue_value.split(']')[1]
                        #s_ji.status_particulars_id = modl.id
                        #s_ji.save()

                elif re.compile('today_\d').match(key):
                    modl = TodayStatus()
                    for text in form_values:
                        modl.status_text = text
                        modl.status = s
                        modl.save()

                    jira_issues_list = request.POST.getlist('jira_issue_for_'+key)

                    for status_issue_value in jira_issues_list:
                        saveStatus_JiraIssue('Today', s, status_issue_value, modl.id)
                        #s_ji = Status_JiraIssue()
                        #s_ji.status_type = 'Today'
                        #s_ji.status = s
                        #s_ji.jira_issue_id = status_issue_value.split(']')[0][1:]
                        #s_ji.jira_issue_text = status_issue_value.split(']')[1]
                        #s_ji.status_particulars_id = modl.id
                        #s_ji.save()

                elif re.compile('issue_\d').match(key):
                    modl = IssueStatus()
                    for text in form_values:
                        modl.status_text = text
                        modl.status = s
                        modl.save()

                    jira_issues_list = request.POST.getlist('jira_issue_for_'+key)

                    for status_issue_value in jira_issues_list:
                        saveStatus_JiraIssue('Issue', s, status_issue_value, modl.id)
                        #s_ji = Status_JiraIssue()
                        #s_ji.status_type = 'Issue'
                        #s_ji.status = s
                        #s_ji.jira_issue_id = status_issue_value.split(']')[0][1:]
                        #s_ji.jira_issue_text = status_issue_value.split(']')[1]
                        #s_ji.status_particulars_id = modl.id
                        #s_ji.save()

            messages.success(request, 'Statuses submitted successfully')
    else:
        if hasattr(settings, 'JIRA'):
            jira_credentials = request.session.get('jira_username', None)
            if jira_credentials is None:
                return redirect('/jiralogin')
            else:
                jira_instance = app.jira.JiraIntegration.JiraIntegration()
                jira_instance.signIn(settings.JIRA['site_url'], 
                                     request.session['jira_username'], 
                                     request.session['jira_password'])
                issue_list = jira_instance.getOpenIssues()
                jira_instance.signOut()

        return render(request, "app/status.html",
                      {
                          'title':'Log your Status',
                          'year':now().year,
                          'form':form,
                          'issue_list':issue_list,
                      })

#@login_required
def readstatus_view(request, status_id):
    """Renders the status page in Read Only mode."""
    assert isinstance(request, HttpRequest)

    s = Status.objects.filter(id=status_id).first()
    ylist = YesterdayStatus.objects.filter(status_id=status_id)
    tlist = TodayStatus.objects.filter(status_id=status_id)
    ilist = IssueStatus.objects.filter(status_id=status_id)
    jira_site_url = None

    if hasattr(settings, 'JIRA'):
        jira_site_url = settings.JIRA['site_url']

    return render(request,
                  'app/readstatus.html',
                  {
                      'title':'Status Submitted on %s' % timezone.localtime(s.timestamp), #("%d %b %Y %I:%M:%S %p"),
                      'year':now().year,
                      'yesterday_list':ylist,
                      'today_list':tlist,
                      'issue_list':ilist,
                      'jira_site_url':jira_site_url,
                  })

#@login_required
def dashboard_view(request):
    """Renders the dashboard page."""
    assert isinstance(request, HttpRequest)
    statuses = Status.objects.filter(submitter=request.user).order_by('-timestamp')
    return render(request,
                  'app/dashboard.html',
                  {
                      'title':'Dashboard',
                      'year':now().year,
                      'statuses': enumerate(statuses),
                  })

def saveStatus_JiraIssue(status_type, status, status_issue_value, status_particulars_id):
    s_ji = Status_JiraIssue()
    s_ji.status_type = status_type
    s_ji.status = status
    s_ji.jira_issue_id = status_issue_value.split(']')[0][1:]
    s_ji.jira_issue_text = status_issue_value.split(']')[1]
    s_ji.status_particulars_id = status_particulars_id
    s_ji.save()