from django.shortcuts import render
from django.views import generic

# Create your views here.
class IndexView(generic.TemplateView):
    """
    The general template view into which we will load other components via AJAX requests.
    """
    template_name = 'blog/index.html'
