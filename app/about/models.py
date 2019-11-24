
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import (
    StreamFieldPanel
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.api import APIField
from wagtail.search import index

from streams.blocks import CardBlock, RichtextBlock, TitleAndTextBlock

from logging import getLogger

logger = getLogger(__name__)


class AboutPage(Page):
    """
    Define a data model for our general About page
    """
    # SETTINGS
    max_count = 1
    # parent_page_types = ['home.HomePage']
    # FIELDS
    content = StreamField([
        ('title_and_text', TitleAndTextBlock()),
        ('richtext', RichtextBlock()),
        ('cards', CardBlock())
    ], null=True, blank=True)
    # ADMIN INTERFACE
    content_panels = Page.content_panels + [
        StreamFieldPanel('content')
    ]
    # API CONFIGURATION
    api_fields = [
        APIField('content')
    ]
    # SEARCH FIELDS
    search_fields = Page.search_fields + [
        index.SearchField('content'),
    ]

    class Meta:
        verbose_name = 'About Page'

