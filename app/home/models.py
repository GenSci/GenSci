from django.db import models

from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.api import APIField
from wagtail.api.v2.serializers import PageSerializer
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.admin.edit_handlers import (
    FieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel

from projects.models import Project, Publication

from blog.models import BlogDetailPage

class HomePageCarousel(Orderable):
    """Add between 1 and 5 images."""

    page = ParentalKey("home.HomePage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    title = models.CharField(max_length=40, null=True, blank=True)
    subtitle = models.CharField(max_length=100, null=True, blank=True)
    text_orient = models.CharField(
        choices=(("left", "Left"), ("right", "Right"), ("center", "Center")),
        max_length=20,
        null=True,
        blank=True,
    )

    api_fields = [
        APIField("title"),
        APIField("subtitle"),
        APIField("text_orient"),
        APIField("carousel_image"),
    ]
    panels = [
        FieldPanel("title"),
        FieldPanel("subtitle"),
        FieldPanel("text_orient"),
        ImageChooserPanel("carousel_image"),
    ]


class HomePage(RoutablePageMixin, Page):
    # Page Settings
    template = "home/home_page.html"
    max_count = 1  # Restrict instances of this page to a single instance.
    # Constants
    MASKS = (("d", "Dark"), ("l", "Light"), ("n", "None"))
    # Fields
    subtitle = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        help_text="A subtitle to be displayed on the home page",
    )
    background_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Apply an image to the background",
    )
    background_mask = models.CharField(
        max_length=1,
        choices=MASKS,
        blank=True,
        null=True,
        help_text="Select semi-transparent mask to apply over background image.",
    )
    n_publications = models.IntegerField(
        verbose_name='Number of Recent Publications',
        default=5,
        help_text='The number of recent publications to return to the homepage.'
    )
    n_projects = models.IntegerField(
        verbose_name='Number of Recent Projects',
        default=5,
        help_text='The number of recent projects to return to the homepage.'
    )
    n_blog_posts = models.IntegerField(
        verbose_name='Number of Recent Blog Posts',
        default=5,
        help_text='The number of recent blog posts to return to the homepage.'
    )
    # Admin Content Panels
    content_panels = Page.content_panels + [
        MultiFieldPanel([FieldPanel("subtitle")]),
        MultiFieldPanel(
            [ImageChooserPanel("background_image"), FieldPanel("background_mask")]
        ),
        MultiFieldPanel([
            FieldPanel('n_publications'),
            FieldPanel('n_projects'),
            FieldPanel('n_blog_posts'),
        ], heading='Home Page Records')
    ]

    api_fields = [
        APIField('subtitle'),
        APIField('background_image'),
        APIField('latest_projects', serializer=PageSerializer),
        APIField('latest_publications', serializer=PageSerializer),
        APIField('latest_blog_posts', serializer=PageSerializer)
    ]

    def get_context(self, request, *args, **kwargs):
        """Linking to projects"""

        context = super().get_context(request, *args, **kwargs)
        context['latest_projects'] = self.latest_projects
        context['latest_publications'] = self.latest_publications
        context['latest_blogs'] = self.latest_blog_posts
        return context
    
    @property
    def latest_projects(self):
        return Project.objects.live().public().order_by(
            '-first_published_at')[:self.n_projects]

    @property
    def latest_publications(self):
        return Publication.objects.live().public().order_by(
            '-first_published_at')[:self.n_publications]

    @property
    def latest_blog_posts(self):
        return BlogDetailPage.objects.live().public().order_by(
            '-first_published_at')[:self.n_blog_posts]

