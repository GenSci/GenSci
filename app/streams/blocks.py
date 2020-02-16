# -*- coding: utf-8 -*-
"""
Stream Blocks

Defining custom blocks for StreamFields
"""
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class TextDiv(blocks.StructBlock):
    """Simple text chunks rendered in a <div> element with CSS classes applied."""
    text = blocks.RichTextBlock(required=True)
    classes = blocks.CharBlock(required=False)

    class Meta:
        template = 'blocks/text_div.html'
        icon = 'document',
        label = 'Text Div'
        

class TitleAndTextBlock(blocks.StructBlock):
    """Just a title and some text."""

    title = blocks.CharBlock(required=True, help_text="Section Title")
    title_css_class = blocks.CharBlock(
        required=False, help_text="Enter the " "CSS classes to be applied"
    )
    text = blocks.RichTextBlock(required=True, help_text="Body text")
    text_css_class = blocks.CharBlock(required=False)

    class Meta:
        template = "blocks/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"


class CardBlock(blocks.StructBlock):
    """Card element with image, text, and buttons"""

    title = blocks.CharBlock(
        required=True, max_length=100, help_text='Enter Section Title'
    )
    cards = blocks.ListBlock(
        blocks.StructBlock([
            ("image", ImageChooserBlock(required=False)),
            ("title", blocks.CharBlock(required=True, max_length=40)),
            ("text", blocks.TextBlock(required=True, max_length=500)),
            ("button_page", blocks.PageChooserBlock(required=False)),
            ("button_url", blocks.URLBlock(required=False))
        ])
    )

    class Meta:
        template = "blocks/card_block.html"
        icon = "user"
        label = "Cards"


class RichtextBlock(blocks.RichTextBlock):
    class Meta:
        template = "blocks/richtext_block.html"
        icon = "doc-full"
        label = 'RichText'
