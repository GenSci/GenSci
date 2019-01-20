from django.views import generic
from django.shortcuts import render

from about import models

# Create your views here.
class AboutIndex(generic.ListView):
    """
    A view providing descriptions of the goals and projects of Gentlemen Scientists
    """
    model = models.Story

class StoryView(generic.DetailView):
    """
    A view rendering individual story componenets
    """
    model = models.Story
