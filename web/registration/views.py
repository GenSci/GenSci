"""
Registration Application - View Classes and Functions

Views will strive to utilize the inheritance of class based views.  However, where appropriate, function based views should be employed to reduce complexity of code.  Simple is better than complex.
"""
from django.shortcuts import render
from django.views import generic
from registration.models import UserReg
from registration.forms import RegistrationForm


class IndexView(generic.TemplateView):
    """
    Here we present the basic landing page describing GenSci.
    """
    template_name = 'registration/index.html'


class ThankYouView(generic.TemplateView):
    """
    A simple view to display a thank you message upon registration completion.
    """
    template_name = 'registration/thankyou.html'


class RegisterFormView(generic.CreateView ):
    """
    This CBV hanldes presenting the user with a registration form
    and processes the returned form
    """
    template_name = 'registration/reg_form.html'
    form_class = RegistrationForm
    success_url = '/register/complete/'
