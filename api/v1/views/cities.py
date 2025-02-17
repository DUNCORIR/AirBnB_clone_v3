#!/usr/bin/python3
"""City view for the API"""

from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route(
    '/states/<state_id>/cities', methods=['GET'], strict_slashes=False
)
def get_cities_by_state(state_id):
    """Retrieve the list of all City objects of a specific State"""
    state = storage.get(State, state_id)  # Retrieve the state by its ID
    if not state:
        return jsonify({"error": "Not found"}), 404
    cities = storage.all(City)  # Get all cities
    state_cities = [
        city.to_dict() for city in cities.values() if city.state_id == state_id
    ]
    return jsonify(state_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieve a specific City object"""
    city = storage.get(City, city_id)  # Retrieve the city by its ID
    if not city:
        return jsonify({"error": "Not found"}), 404
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a City object"""
    city = storage.get(City, city_id)  # Retrieve the city by its ID
    if not city:
        return jsonify({"error": "Not found"}), 404
    storage.delete(city)  # Delete the city
    storage.save()  # Save the changes to the storage
    return jsonify({})  # Return an empty dictionary


@app_views.route(
    '/states/<state_id>/cities', methods=['POST'], strict_slashes=False
)
def create_city(state_id):
    """Create a new City object"""
    state = storage.get(State, state_id)  # Retrieve the state by its ID
    if not state:
        return jsonify({"error": "Not found"}), 404
    if not request.is_json:  # Check if the body is not JSON
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()  # Parse the JSON request body
    if 'name' not in data:  # Check if 'name' field is missing
        return jsonify({"error": "Missing name"}), 400
    city = City(name=data['name'], state_id=state_id)  # Create new City object
    storage.new(city)  # Add the new city to storage
    storage.save()  # Save the changes to the storage
    return jsonify(city.to_dict()), 201  # Return the new city with status 201


@app_views.route(
    '/cities/<city_id>', methods=['PUT'], strict_slashes=False
)
def update_city(city_id):
    """Update a City object"""
    city = storage.get(City, city_id)  # Retrieve the city by its ID
    if not city:
        return jsonify({"error": "Not found"}), 404
    if not request.is_json:  # Check if the body is not JSON
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()  # Parse the JSON request body
    for key, value in data.items():
        if key not in [
            'id', 'state_id', 'created_at', 'updated_at'
        ]:  # Ignore these fields
            setattr(city, key, value)  # Update the city with the new value
    storage.save()  # Save the changes to the storage
    return jsonify(city.to_dict())  # Return the updated city with status 200
