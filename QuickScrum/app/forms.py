"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'autofocus': '',
                                   'required': '',
                                   'placeholder': 'Username (email)'}))
    password = forms.CharField(widget=forms.PasswordInput({
        'class': 'form-control',
        'required': '',
        'placeholder':'Password'}))

class BootstrapRegisterForm(AuthenticationForm):
    """Register form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'autofocus': '',
                                   'required': '',
                                   'type':'email',
                                   'placeholder': 'Username (email)'}))

    password = forms.CharField(widget=forms.PasswordInput({
        'class': 'form-control',
        'required': '',
        'placeholder':'Password'}))

    passwordConfirm = forms.CharField(widget=forms.PasswordInput({
        'class': 'form-control',
        'required': '',
        'placeholder':'Password (confirm)'}))

    fname = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'autofocus': '',
                                   'required': '',
                                   'placeholder': 'First Name'}))

    lname = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'autofocus': '',
                                   'required': '',
                                   'placeholder': 'Last Name'}))

    #email = forms.CharField(max_length=254,
    #                           widget=forms.TextInput({
    #                               'class': 'form-control',
    #                               'autofocus': '',
    #                               'required': '',
    #                               'type':'email',
    #                               'placeholder': 'Email'}))



class BootstrapPasswordChangeForm(forms.Form):
    """Password change form which uses boostrap CSS."""
    
    currentPassword = forms.CharField(widget=forms.PasswordInput({
        'class': 'form-control',
        'required': '',
        'autofocus': '',
        'placeholder':'Current Password'}))
    
    newPassword = forms.CharField(widget=forms.PasswordInput({
        'class': 'form-control',
        'required': '',
        'placeholder':'New Password'}))

    newPasswordConfirm = forms.CharField(widget=forms.PasswordInput({
        'class': 'form-control',
        'required': '',
        'placeholder':'New Password (confirm)'}))

class JiraAuthenticationForm(BootstrapAuthenticationForm):
    jiraurl = forms.CharField(widget=forms.TextInput({
        'class': 'form-control',
        'required': '',
        'autofocus': '',
        'placeholder': 'Jira site url'}))

class StatusForm(forms.Form):

    # Incoming data (initial render)
    def __init__(self, *args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)

    # Outgoing data (POST)
    def statuses(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield value
