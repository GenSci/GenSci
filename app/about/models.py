from django.db import models
from django.utils.text import slugify

# Create your models here.
class Story(models.Model):
    """
    A model for story componenets that will be rendered on the About page of Gentlemen Scientsits.
    """
    date_created = models.DateTimeField(auto_now_add=True, help_text='date record created.')
    date_modified = models.DateTimeField(auto_now=True, help_text='date of most recent record modification.')
    created_by = models.ForeignKey('auth.User', help_text='user who created record.', null=True, blank=True, on_delete=models.SET_NULL, related_name='Story_created')
    modified_by=models.ForeignKey('auth.User', help_text='user who most recently modified record.', null=True, blank=True, on_delete=models.SET_NULL, related_name='Story_modified')
    title = models.CharField(max_length=100, null=True, blank=True, help_text='The title for this story component.')
    text = models.TextField(help_text='The text of this story component')
    class_names = models.CharField(max_length=255, null=True, blank=True, help_text='The class names that will be applied to HTML elements when rendering this story component')
    order = models.IntegerField(default=0)

    class Meta:
        app_label = 'about'
        ordering = ['order', ]
