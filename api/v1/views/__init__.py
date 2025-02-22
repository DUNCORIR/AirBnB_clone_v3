#!/usr/bin/python3
"""Initialize Blueprint for API views
This module creates a Flask Blueprint named 'app_views' with a URL prefix of /api/v1.
It imports all the view modules required for handling different resources like:
- Index
- States
- Cities
- Amenities
- Users
- Places
- Place Reviews
- Place Amenities
"""
from flask import Blueprint

# Create the app_views Blueprint with a URL prefix of /api/v1
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
# Import views at the end to avoid circular imports
from api.v1.views.index import *
from api.v1.views.states import *  # Import the new states view
from api.v1.views.cities import *  # Import the new cities view
from api.v1.views.amenities import *  # Import the amenities view
from api.v1.views.users import *  # Import the users view
from api.v1.views.places import *  # Import the places  view
from api.v1.views.places_reviews import *  # Import the places_reviews view
from api.v1.views.places_amenities import *  # Places-amenities view
