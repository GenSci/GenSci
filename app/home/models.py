from django.db import models

from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.api import APIField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.admin.edit_handlers import (
    FieldPanel, PageChooserPanel, StreamFieldPanel, InlinePanel,
    MultiFieldPanel
)
from wagtail.images.edit_handlers import ImageChooserPanel


class HomePageCarousel(Orderable):
    """Add between 1 and 5 images."""

    page = ParentalKey('home.HomePage', related_name='carousel_images')
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    title = models.CharField(max_length=40, null=True, blank=True)
    subtitle = models.CharField(max_length=100, null=True, blank=True)
    text_orient = models.CharField(
        choices=(
            ('left', "Left"),
            ('right', 'Right'),
            ('center', 'Center')
        ), max_length=20, null=True, blank=True
    )

    api_fields = [
        APIField('title'),
        APIField('subtitle'),
        APIField('text_orient'),
        APIField('carousel_image')
    ]
    panels = [
        FieldPanel('title'),
        FieldPanel('subtitle'),
        FieldPanel('text_orient'),
        ImageChooserPanel("carousel_image"),
    ]


class HomePage(RoutablePageMixin, Page):
    # Page Settings
    template = 'home/home_page.html'
    max_count = 1  # Restrict instances of this page to a single instance.
    # Constants
    MASKS = (
        ('d', 'Dark'),
        ('l', 'Light'),
        ('n', 'None')
    )
    # Fields
    background_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Apply an image to the background'
    )
    background_mask = models.CharField(
        max_length=1,
        choices=MASKS,
        blank=True, null=True,
        help_text='Select semi-transparent mask to apply over background image.'
    )
    # Admin Content Panels
    content_panels = Page.content_panels + [
        MultiFieldPanel([
           ImageChooserPanel('background_image'),
           FieldPanel('background_mask')
        ]),
        MultiFieldPanel([
            InlinePanel('carousel_images', min_num=1, max_num=5,
                        label='Images'),
        ], heading='Carousel Images'),
    ]
