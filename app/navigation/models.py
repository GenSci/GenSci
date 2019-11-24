# -*- coding: utf-8 -*-
"""
Navigation Models

These models define how we will construction our site navigation objects.
"""
from django.db import models
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django_extensions.db.fields import AutoSlugField

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.core.models import Orderable
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    PageChooserPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet


class MenuItem(Orderable):
    """Define a single menu item."""

    link_title = models.CharField(max_length=100, blank=True, null=True)
    # URL field uses too strict validation criteria, we use CharField for more
    # flexibility
    link_url = models.CharField(max_length=250, blank=True, null=True)
    icon = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        help_text="The html required for any icon you wish to display.",
    )
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="+",
    )
    open_in_new_tab = models.BooleanField(default=False, blank=True)

    page = ParentalKey("Menu", related_name="menu_items")

    panels = [
        FieldPanel("link_title"),
        FieldPanel("link_url"),
        PageChooserPanel("link_page"),
        FieldPanel("open_in_new_tab"),
    ]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        else:
            return "#"

    @property
    def title(self):
        if self.link_page and not self.link_url:
            return self.link_page.title
        elif self.link_title:
            return self.link_title
        else:
            return "Missing Title"

    def save(self, *args, **kwargs):
        """Clear cache when changing menu items."""
        # These items appear in two caches.
        navbar_key = make_template_fragment_key("navigation")
        sidenav_key = make_template_fragment_key("side_nav")
        cache.delete(navbar_key)
        cache.delete(sidenav_key)
        return super().save(*args, **kwargs)


@register_snippet
class Menu(ClusterableModel):
    """Define main menu object."""

    title = models.CharField(max_length=100, null=True, blank=False)
    # A custom field to autopopulate the slug field
    slug = AutoSlugField(populate_from="title", editable=True)
    background_color_class = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        help_text="Enter the css class to be applied to the nav bar.",
    )
    menu_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("title"),
                FieldPanel("slug"),
                FieldPanel("background_color_class"),
                ImageChooserPanel("menu_image"),
            ],
            heading="Menu",
        ),
        InlinePanel("menu_items", label="Menu Item"),
    ]

    def __str__(self):
        return self.title
