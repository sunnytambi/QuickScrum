"""
Definition of forms.
"""

from django import forms
from django.forms import Form
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'type': 'email',
                                   'autofocus': '',
                                   'required': '',
                                   'placeholder': 'Email address'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'required': '',
                                   'placeholder':'Password'}))

class StatusForm(forms.Form):
    def __init__(self, *args, **kwargs):
        #extra = kwargs.pop('extra')
        super(StatusForm, self).__init__(*args, **kwargs)

        for i, question in enumerate(extra):
            self.fields['custom_%s' % i] = forms.CharField(label=question)
    
    def statuses(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (value)
