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
                                   'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput({
        'class': 'form-control',
        'required': '',
        'placeholder':'Password'}))

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
