"""
Registration application URL Configuration.

Url pattern matching for the registration application.
"""
from django.conf.urls import url
from registration import views as reg_views

app_name = 'registration'
urlpatterns = [
    url(r'^$', reg_views.IndexView.as_view(), name='register'),
    url(r'^register/complete/$', reg_views.ThankYouView.as_view(), \
        name='reg-complete'),
    url(r'^reg-form/$', reg_views.RegisterFormView.as_view(), \
        name='reg-form')
]
