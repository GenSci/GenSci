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

    def get_context_data(self, **kwargs):
        context = super(IndexView,self).get_context_data(**kwargs)
        context['title'] = 'GenSci Coming Soon'

        return context


class ThankYouView(generic.TemplateView):
    """
    A simple view to display a thank you message upon registration completion.
    """
    template_name = 'registration/thankyou.html'

    def get_context_data(self, **kwargs):
       """
       This function appends additional data to the context variable passed to
       the template.
       """
       context = super(ThankYouView,self).get_context_data(**kwargs)
       context['title'] = "Thank You"
       return context


class RegisterFormView(generic.CreateView ):
    """
    This CBV hanldes presenting the user with a registration form
    and processes the returned form
    """
    template_name = 'registration/reg_form.html'
    form_class = RegistrationForm
    success_url = '/register/complete/'

    def get_context_data(self,**kwargs):
      context = super(RegisterFormView,self).get_context_data(**kwargs)
      context['title'] = 'Register'
      return context
