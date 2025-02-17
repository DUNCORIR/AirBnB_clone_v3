#!/usr/bin/python3
"""Amenity view for the API"""

from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route(
    '/amenities', methods=['GET'], strict_slashes=False
)
def get_all_amenities():
    """Retrieve the list of all Amenity objects"""
    amenities = storage.all(Amenity)  # Get all amenities
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@app_views.route(
    '/amenities/<amenity_id>', methods=['GET'], strict_slashes=False
)
def get_amenity(amenity_id):
    """Retrieve a specific Amenity object"""
    amenity = storage.get(Amenity, amenity_id)  # Retrieves amenity by its ID
    if not amenity:
        return jsonify({"error": "Not found"}), 404
    return jsonify(amenity.to_dict())


@app_views.route(
    '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False
)
def delete_amenity(amenity_id):
    """Delete a specific Amenity object"""
    amenity = storage.get(Amenity, amenity_id)  # Retrieves amenity by its ID
    if not amenity:
        return jsonify({"error": "Not found"}), 404
    storage.delete(amenity)  # Delete the amenity
    storage.save()  # Save the changes to storage
    return jsonify({})  # Return an empty dictionary with status 200


@app_views.route(
    '/amenities', methods=['POST'], strict_slashes=False
)
def create_amenity():
    """Create a new Amenity object"""
    if not request.is_json:  # Check if the body is not JSON
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()  # Parse the JSON request body
    if 'name' not in data:  # Check if the 'name' field is missing
        return jsonify({"error": "Missing name"}), 400
    amenity = Amenity(name=data['name'])  # Create a new Amenity object
    storage.new(amenity)  # Add the new amenity to storage
    storage.save()  # Save the changes to the storage
    return jsonify(amenity.to_dict()), 201  # Returns new amenity-status 201


@app_views.route(
    '/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False
)
def update_amenity(amenity_id):
    """Update a specific Amenity object"""
    amenity = storage.get(Amenity, amenity_id)  # Retrieves amenity by its ID
    if not amenity:
        return jsonify({"error": "Not found"}), 404
    if not request.is_json:  # Check if the body is not JSON
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()  # Parse the JSON request body
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:  # Ignore the fields
            setattr(amenity, key, value)  # Update amenity with new value
    storage.save()  # Save the changes to storage
    return jsonify(amenity.to_dict())  # Return updated amenity-status 200
