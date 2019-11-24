# -*- coding: utf-8 -*-
"""
Custom Menu Application Template Tags

This file defines a simple tag we can use to return a specific menu instance to
the calling template.
"""
from django import template
from django.template.defaultfilters import stringfilter

from ..models import Menu

register = template.Library()


@register.simple_tag()
def get_menu(slug):
    return Menu.objects.get(slug=slug)


@register.filter()
def is_trans(*args):
    import pdb

    pdb.set_trace()
    return class_code == "trans"
