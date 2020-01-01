# -*- coding: utf-8 -*-
"""
API ENDPOINT CONFIGURATION

This file defines the API endpoints exposed by this application.
"""
from wagtail.api.v2.endpoints import PagesAPIEndpoint
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.endpoints import ImagesAPIEndpoint
from wagtail.documents.api.v2.endpoints import DocumentsAPIEndpoint

from home.api import HomeAPIEndpoint

api_router = WagtailAPIRouter("api")

api_router.register_endpoint(r'home', HomeAPIEndpoint)
api_router.register_endpoint('pages', PagesAPIEndpoint)
api_router.register_endpoint('documents', DocumentsAPIEndpoint)
api_router.register_endpoint('images', ImagesAPIEndpoint)
