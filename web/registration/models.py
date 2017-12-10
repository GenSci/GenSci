"""
Models.py:  Repository for application models - corresponds to database tables.
"""
from django.db import models


class UserReg(models.Model):
    """
    Model to allow users to register for 'Go Live' notification
    """
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True, \
    help_text= \
    'The person that will be notified when Gentlemen Scientists goes live.')
    email = models.EmailField(max_length=254, \
    help_text= \
    'The email address that will be notified when Gentlmen Scientists goes live.')
