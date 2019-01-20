"""
about/urls.py
--------------------------------------------------------------
URL Routing configuration for the About app.
"""
from django.urls import path
from about import views

app_name = 'about'
urlpatterns = [
    path('', views.AboutIndex.as_view(), name='index'),
    path('story/<int:pk>/<slug:title>/', views.StoryView.as_view(), name='story'),
]
