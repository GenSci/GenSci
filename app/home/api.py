# -*- coding: utf-8 -*-
"""
HOME API CONFIGURATION

Configuration of custom API endpoints for the Home App.
"""

from wagtail.api.v2.endpoints import BaseAPIEndpoint, PagesAPIEndpoint

from .models import HomePage


class HomeAPIEndpoint(PagesAPIEndpoint):
    """
    Define a class for the home page.  This will serve as the root API
    endpoint from which we will branch out.  We will return the querysets we
    wish to display on the home page as the links to other endpoints.
    """
    model = HomePage

