from django.db import models
from django import forms
from django.utils.text import slugify
from django.core.paginator import (
    EmptyPage, PageNotAnInteger, Paginator
)

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import (
    RichTextFieldPanel, FieldPanel, MultiFieldPanel, PageChooserPanel,
    InlinePanel
)
from wagtail.search import index
from wagtail.api import APIField
from wagtail.snippets.models import register_snippet
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from streams import blocks
from blog.models import BlogCategory

from logging import getLogger

logger = getLogger(__name__)


class PublicationAuthorOrderable(Orderable):
    page = ParentalKey('projects.Publication',related_name='authors')
    author = models.ForeignKey(
        'projects.Scientist',
        on_delete=models.CASCADE,
        related_name='publications'
    )
    api_fields = [
        APIField('author_name'),
        APIField('author_institutions'),
    ]
    @property
    def author_name(self):
        return self.author.name()

    @property
    def author_institutions(self):
        return self.author.get_institutions()


@register_snippet
class Scientist(models.Model):
    first_name = models.CharField(
        max_length=100, null=True, blank=False,
        help_text="Scientist's first name"
    )
    last_name = models.CharField(
        max_length=100, null=True, blank=False,
        help_text="Scientist's last name"
    )
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='+'
    )
    institutions = models.ManyToManyField(
        'projects.Institution',
        related_name='scientists'
    )
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    def name(self, format='f l'):
        names = {
            'f l': f'{self.first_name} {self.last_name}',
            'l f': f'{self.last_name}, {self.first_name}'
        }
        return names.get(format)

    def __str__(self):
        return  self.name()

    def get_institutions(self):
        return [
            {
                'name': inst.name,
                'website': inst.website
            } for inst in self.institutions.all()
        ]

    class Meta:
        verbose_name = 'Scientist'
        verbose_name_plural = 'Scientists'


@register_snippet
class Institution(models.Model):
    name = models.CharField(max_length=150, null=True, blank=False)
    website = models.URLField(blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class PublicationListingPage(RoutablePageMixin, Page):
    """Return a list of published Publication pages."""
    # SETTINGS
    template = 'project/publication_list.html'
    parent_page_types = ['home.HomePage']
    # FIELDS
    page_title = models.CharField(
        max_length=120, blank=False, null=True,
        help_text="Title for List of Publications"
    )
    page_subtitle = RichTextField(
        blank=True, null=True,
        help_text='Sub title text for listing page.'
    )
    pubs_per_page = models.IntegerField(
        default=5, verbose_name='Publications per Page',
        help_text='Define how this listing is paginated'
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        all_publications = Publication.objects.live().public(
                            ).order_by('-pub_date')
        # Adding pagination
        paginator = Paginator(all_publications, self.pubs_per_page)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        context['categories'] = BlogCategory.objects.all()
        return context

    api_fields = [
        APIField('page_title'),
        APIField('page_subtitle'),
    ]
    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        RichTextFieldPanel('page_subtitle'),
        FieldPanel('pubs_per_page')
    ]

    class Meta:
        verbose_name = 'Publication Listing'
        verbose_name_plural = 'Publication Listings'


class Publication(Page):
    # SETTINGS
    template = "project/publication_detail.html"
    parent_page_types = ['projects.PublicationListingPage']
    # FIELDS
    pub_title = models.CharField(
        max_length=150, null=True, blank=False
    )
    pub_abstract = RichTextField(
        blank=False, null=True,
        help_text="Publication abstract"
    )
    pub_link = models.URLField(
        null=True, blank=True,
        help_text='Link to publication'
    )
    pub_date = models.DateField(
        blank=True, null=True,
        verbose_name='Publication Date',
        help_text='The rough date when this publication was published.'
    )
    gs_project = models.ForeignKey(
        'projects.Project',
        null=True, blank=True,
        related_name='publications',
        on_delete=models.SET_NULL
    )

    categories = ParentalManyToManyField('blog.BlogCategory')

    search_fields = Page.search_fields + [
        index.SearchField('pub_title'),
        index.SearchField('pub_abstract'),
        index.SearchField('categories'),
        index.SearchField('authors')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('pub_title'),
        RichTextFieldPanel('pub_abstract'),
        FieldPanel('pub_link'),
        MultiFieldPanel([
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
        ]),
        PageChooserPanel('gs_project'),
        MultiFieldPanel([
            InlinePanel('authors', label="Author", min_num=1)
        ], heading='Publication Authors'),
    ]

    api_fields = [
        APIField('pub_title'),
        APIField('pub_abstract'),
        APIField('gs_project'),
        APIField('pub_link'),
        APIField('authors'),
        APIField('categories'),
    ]

    class Meta:
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'


class ProjectScientistOrderable(Orderable):
    project = ParentalKey('projects.Project',
                          related_name='collaborators')
    scientist = models.ForeignKey(
        'projects.Scientist',
        on_delete=models.CASCADE,
    )


class Project(Page):
    """"Define data model for scientific projects."""
    # CONSTANTS
    PROJECT_TYPES = (
        ('s', 'Software'),
        ('r', 'Research')
    )
    PROJECT_STATUSES = (
        ('pl', 'Planned'),
        ('ip', 'In Progress'),
        ('oh', 'On Hold'),
        ('cp', 'Completed')
    )
    # SETTINGS
    template = "project/project_detail.html"
    parent_page_types = ['projects.ProjectList', ]
    # FIELDS
    name = models.CharField(
        max_length=120, blank=False, null=True,
        help_text='The basic name for a given project'
    )
    description = RichTextField(
        verbose_name='Project Description',
        null=True, blank=False,
        help_text='A description of this project including questions '
                  'that it tries to answer, data sources and tools used, etc. '
    )
    type = models.CharField(
        max_length=5, null=True, blank=False,
        choices=PROJECT_TYPES,
        help_text='The type of work that this project represents'
    )
    repository = models.URLField(
        null=True, blank=True,
        help_text='If a software project, provide a link to the repository '
                  'for the code base.'
    )
    status = models.CharField(
        max_length=3, null=True, blank=False,
        choices=PROJECT_STATUSES,
        help_text='The stage this project is currently at.'
    )

    # API FIELDS
    api_fields = [
        APIField('name'),
        APIField('description'),
        APIField('type'),
        APIField('repository')
    ]
    # ADMIN INTERFACE
    content_panels = Page.content_panels + [
        FieldPanel('name'),
        RichTextFieldPanel('description'),
        FieldPanel('type'),
        FieldPanel('repository'),
        MultiFieldPanel([
            InlinePanel('collaborators', label='Collaborator', min_num=1)
        ], heading='Project Collaborators'),
        FieldPanel('status',)
    ]

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'


class ProjectList(RoutablePageMixin, Page):

    # SETTINGS
    template = 'project/project_list.html'
    parent_page_types = ['home.HomePage']
    # FIELDS
    page_title = models.CharField(
        max_length=120, blank=False, null=True,
        help_text='Title for list of Projects'
    )
    page_subtitle = RichTextField(
        blank=True, null=True,
        help_text='Sub title text for listing page.'
    )
    projects_per_page = models.IntegerField(
        default=5, verbose_name='Projects per Page',
        help_text='Number of projects per page.'
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        all_projects = Project.objects.live().public().order_by(
            '-first_published_at')
        paginator = Paginator(all_projects, self.projects_per_page)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        context['categories'] = BlogCategory.objects.all()
        return context

    api_fields = [
        APIField('page_title'),
        APIField('page_subtitle')
    ]
    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        RichTextFieldPanel('page_subtitle'),
        FieldPanel('projects_per_page')
    ]

    class Meta:
        verbose_name = 'Project Listing'
        verbose_name_plural = 'Project Listings'



from django.db import models

# Create your models here.
