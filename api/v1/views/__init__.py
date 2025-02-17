#!/usr/bin/python3
"""Initialize Blueprint for API views"""
# Import all view modules (PEP8 will complain, but it's required)
from api.v1.views.index import *
from flask import Blueprint

# Create the app_views Blueprint with a URL prefix of /api/v1
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
