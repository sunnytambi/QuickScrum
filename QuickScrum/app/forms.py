"""
Definition of forms.
"""

from django.forms import Form, ModelForm, CharField, TextInput, PasswordInput
from django.contrib.auth.forms import AuthenticationForm
from app.models import Teams

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = CharField(max_length=254,
                               widget=TextInput({
                                   'class': 'form-control',
                                   'autofocus': '',
                                   'type': 'email',
                                   'required': '',
                                   'placeholder': 'Username (email)'}))
    password = CharField(widget=PasswordInput({
        'class': 'form-control',
        'required': '',
        'placeholder':'Password'}))

class BootstrapRegisterForm(AuthenticationForm):
    """Register form which uses boostrap CSS."""
    username = CharField(max_length=254,
                               widget=TextInput({
                                   'class': 'form-control',
                                   'autofocus': '',
                                   'required': '',
                                   'type':'email',
                                   'placeholder': 'Username (email)'}))

    password = CharField(widget=PasswordInput({
        'class': 'form-control',
        'required': '',
        'placeholder':'Password'}))

    passwordConfirm = CharField(widget=PasswordInput({
        'class': 'form-control',
        'required': '',
        'placeholder':'Password (confirm)'}))

    fname = CharField(max_length=254,
                               widget=TextInput({
                                   'class': 'form-control',
                                   'autofocus': '',
                                   'required': '',
                                   'placeholder': 'First Name'}))

    lname = CharField(max_length=254,
                               widget=TextInput({
                                   'class': 'form-control',
                                   'autofocus': '',
                                   'required': '',
                                   'placeholder': 'Last Name'}))

    #email = CharField(max_length=254,
    #                           widget=TextInput({
    #                               'class': 'form-control',
    #                               'autofocus': '',
    #                               'required': '',
    #                               'type':'email',
    #                               'placeholder': 'Email'}))



class BootstrapPasswordChangeForm(Form):
    """Password change form which uses boostrap CSS."""
    
    currentPassword = CharField(widget=PasswordInput({
        'class': 'form-control',
        'required': '',
        'autofocus': '',
        'placeholder':'Current Password'}))
    
    newPassword = CharField(widget=PasswordInput({
        'class': 'form-control',
        'required': '',
        'placeholder':'New Password'}))

    newPasswordConfirm = CharField(widget=PasswordInput({
        'class': 'form-control',
        'required': '',
        'placeholder':'New Password (confirm)'}))

class JiraAuthenticationForm(BootstrapAuthenticationForm):
    jiraurl = CharField(widget=TextInput({
        'class': 'form-control',
        'required': '',
        'autofocus': '',
        'placeholder': 'Jira site url'}))

class TeamLoginForm(ModelForm):
    """Team login form which uses boostrap CSS."""
    class Meta:
        model = Teams
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control',
                                     'required': '',
                                     'autofocus': '',
                                     'placeholder':'teamdomain'}),
            }
        #teamname = CharField(widget=TextInput({
        #    'class': 'form-control',
        #    'required': '',
        #    'autofocus': '',
        #    'placeholder':'teamdomain'}))

class StatusForm(Form):

    # Incoming data (initial render)
    def __init__(self, *args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)

    # Outgoing data (POST)
    def statuses(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield value
