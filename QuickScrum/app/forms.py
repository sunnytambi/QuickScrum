"""
Definition of forms.
"""

from django import forms
from django.forms import Form
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

class StatusForm(forms.Form):
    # Incoming data (initial render)
    def __init__(self, *args, **kwargs):
        #extra = kwargs.pop('extra')
        super(StatusForm, self).__init__(*args, **kwargs)
        #self.fields['yesterday'] = forms.CharField(widget=forms.Textarea({
        #    'placeholder':'Yesterday\'s Status',
        #    'rows':'',
        #    'cols':'',
        #    'class':'form-control',
        #    'required':''}), strip=True)
        #self.fields['today'] = forms.CharField(widget=forms.Textarea({
        #    'placeholder':'Today\'s Status',
        #    'rows':'',
        #    'cols':'',
        #    'class':'form-control',
        #    'required':''}))
        #self.fields['issue'] = forms.CharField(widget=forms.Textarea({
        #    'placeholder':'Issue',
        #    'rows':'',
        #    'cols':'',
        #    'class':'form-control',
        #    'required':''}))
        #for i, question in enumerate(extra):
        #    self.fields['custom_%s' % i] = forms.CharField(label=question)
    
    # Outgoing data (POST)
    def statuses(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (value)
