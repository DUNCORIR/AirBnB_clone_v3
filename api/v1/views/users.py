#!/usr/bin/python3
"""User view for the API"""

from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieve the list of all User objects"""
    users = storage.all(User)  # Get all users
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieve a specific User object"""
    user = storage.get(User, user_id)  # Retrieve the user by its ID
    if not user:
        return jsonify({"error": "Not found"}), 404
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a specific User object"""
    user = storage.get(User, user_id)  # Retrieve the user by its ID
    if not user:
        return jsonify({"error": "Not found"}), 404
    storage.delete(user)  # Delete the user
    storage.save()  # Save the changes to storage
    return jsonify({})  # Return an empty dictionary with status 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new User object"""
    if not request.is_json:  # Check if the body is not JSON
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()  # Parse the JSON request body
    if 'email' not in data:  # Check if the 'email' field is missing
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in data:  # Check if the 'password' field is missing
        return jsonify({"error": "Missing password"}), 400
    user = User(
        email=data['email'], password=data['password']
    )  # Creates new user
    storage.new(user)  # Add the new user to storage
    storage.save()  # Save the changes to storage
    return jsonify(user.to_dict()), 201  # Return the new user with status 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update a specific User object"""
    user = storage.get(User, user_id)  # Retrieve the user by its ID
    if not user:
        return jsonify({"error": "Not found"}), 404
    if not request.is_json:  # Check if the body is not JSON
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()  # Parse the JSON request body
    for key, value in data.items():
        if key not in [
            'id', 'email', 'created_at', 'updated_at'
        ]:  # Ignore specific fields
            setattr(user, key, value)  # Update the user with the new value
    storage.save()  # Save the changes to storage
    return jsonify(user.to_dict())  # Return the updated user with status 200
