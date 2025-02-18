#!/usr/bin/python3
"""
Index view for the API.
This module provides two endpoints:
- `/status`: Returns the API status.
- `/stats`: Returns the count of various objects.
"""

from api.v1.views import app_views
from flask import jsonify
from api.v1.views.index import *
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
# api/v1/views/__init__.py
from flask import Blueprint

# Create a Blueprint named 'app_views' with URL prefix '/api/v1'
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Returns the status of the API"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Returns the number of each objects by type"""
    stats = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(stats)
