"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from pentabank.pentasit.models import *

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = "__all__"
        widgets = {
            'name': forms.Textarea(attrs={'rows': 1})
        }


class NpTypeForm(forms.ModelForm):
    class Meta:
        model = NpType
        fields = "__all__"
        widgets = {
            'name': forms.Textarea(attrs={'rows': 1})
        }


class NodeForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = "__all__"
        widgets = {
            'name': forms.Textarea(attrs={'rows': 1})
        }


class ExampleForm(forms.ModelForm):
    class Meta:
        model = Example
        fields = "__all__"
        widgets = {
            'sentence': forms.Textarea(attrs={'rows': 1})
        }



class SituationForm(forms.ModelForm):
    class Meta:
        model = Situation
        # fields = "__all__"
        fields = ['name', 'preposition']