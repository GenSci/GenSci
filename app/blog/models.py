from django.db import models
from django.utils.text import slugify
from django.shortcuts import render

from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField, RichTextField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.admin.edit_handlers import (
    FieldPanel,
    RichTextFieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    InlinePanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.api import APIField
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from modelcluster.fields import ParentalManyToManyField

from streams.blocks import CardBlock, RichtextBlock, TitleAndTextBlock

from logging import getLogger

logger = getLogger(__name__)


@register_snippet
class BlogCategory(models.Model):
    """
    Define categories for blog entries
    """

    # FIELDS
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    slug = models.SlugField(
        verbose_name="Slug", allow_unicode=True, max_length=100, default=""
    )
    # API FIELDS
    api_fields = [APIField("name"), APIField("slug")]
    # ADMIN INTERFACE CONFIGURATION
    panels = [FieldPanel("name")]

    def save(self, *args, **kwargs):
        name = self.name
        self.slug = slugify(name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]


class BlogListingPage(RoutablePageMixin, Page):
    """
    Return a list of individual BlogPage objects.
    """

    template = "blog/blog_listing_page.html"
    parent_page_types = ['home.HomePage']

    # FIELDS
    page_title = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        help_text="A title for the header of this page.",
    )

    # CUSTOM METHODS
    def get_context(self, request, *args, **kwargs):
        """Adding blog pages to our context"""
        context = super().get_context(request, *args, **kwargs)

        context["categories"] = BlogCategory.objects.all()
        return context

    # API FIELDS
    api_fields = [APIField("page_title")]
    # ADMIN INTERFACE
    content_panels = Page.content_panels + [FieldPanel("page_title")]

    class Meta:
        verbose_name = "Blog Listing"
        verbose_name_plural = "Blog Listings"

    @route(r"^latest/")
    def latest_posts(self, request, *args, **kwargs):
        context = self.get_context(request, *args, *kwargs)
        context["latest_posts"] = context["posts"][:4]
        context["n"] = len(context["latest_posts"])
        return render(request, template_name="blog/latest_posts.html", context=context)


class BlogDetailPage(Page):
    """Define our general Blog Post model"""
    # SETTINGS
    parent_page_types = ['blog.BlogListingPage']
    # FIELDS
    post_title = models.CharField(max_length=100, null=True, blank=False)
    post_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    post_summary = RichTextField(
        blank=False,
        null=True,
        help_text="A helpful short summary of what this post is about.",
    )
    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)

    content = StreamField([
        ('title_and_text', TitleAndTextBlock()),
        ('richtext', RichtextBlock()),
        ('cards', CardBlock())
    ], null=True, blank=True)
    # DEFINE FIELDS TO SEARCH
    search_fields = Page.search_fields + [
        index.SearchField("post_title"),
        index.SearchField("post_summary"),
        index.SearchField("categories"),
        index.SearchField("content"),
    ]
    # ADMIN INTERFACE
    content_panels = Page.content_panels + [
        FieldPanel("post_title"),
        RichTextFieldPanel("post_summary"),
        ImageChooserPanel("post_image"),
        StreamFieldPanel("content"),
        MultiFieldPanel([InlinePanel("categories")]),
    ]
    # API FIELDS
    api_fields = [
        APIField("post_title"),
        APIField("post_image"),
        APIField("post_summary"),
        APIField("content"),
        APIField("categories"),
    ]

    class Meta:
        verbose_name = "Blog Detail"
        verbose_name_plural = "Blog Details"

    def save(self, *args, **kwargs):
        """Clear cache for specific objects when saved."""
        # TODO (ryan@gensci.org): Add cache clearing when caching is implemented
        return super().save(*args, **kwargs)
