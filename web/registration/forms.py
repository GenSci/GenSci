"""
Registration Forms Definitions
"""

from django import forms
from registration.models import UserReg


class RegistrationForm(forms.ModelForm):
    """
    Defining the form users will fill out to sign up for 'Go Live'
     notifications.
    """
    title = "Get Notified"
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={"class": 'form-control'}))
    class Meta:
        model = UserReg
        fields = ['name', 'email']
