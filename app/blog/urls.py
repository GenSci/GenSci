"""
blog/urls.py
===========================================================
URL COnfiguration for the Blog App
"""

from django.urls import path
from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
