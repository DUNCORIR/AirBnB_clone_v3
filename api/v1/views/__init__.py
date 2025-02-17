#!/usr/bin/python3
"""Initialize Blueprint for API views"""
from flask import Blueprint

# Create the app_views Blueprint with a URL prefix of /api/v1
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
# Import views at the end to avoid circular imports
from api.v1.views.index import *
from api.v1.views.states import *  # Import the new states view
