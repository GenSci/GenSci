"""
Registration Forms Definitions
"""

from django import forms
from registration.models import UserReg


class RegistrationForm(forms.ModelForm):
    """
    Defining the form users will fill out to sign up for 'Go Live' notifications.
    """
    class Meta:
        model = UserReg
        fields = ['name', 'email']
