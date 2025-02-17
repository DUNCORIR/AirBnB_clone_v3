#!/usr/bin/python3
"""State view for the API"""

from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieve the list of all State objects"""
    states = storage.all(State)  # Get all states
    return jsonify([state.to_dict() for state in states.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieve a specific State object"""
    state = storage.get(State, state_id)  # Retrieve the state by its ID
    if not state:
        return jsonify({"error": "Not found"}), 404
    return jsonify(state.to_dict())


@app_views.route(
    '/states/<state_id>', methods=['DELETE'], strict_slashes=False
)
def delete_state(state_id):
    """Delete a State object"""
    state = storage.get(State, state_id)  # Retrieve the state by its ID
    if not state:
        return jsonify({"error": "Not found"}), 404
    storage.delete(state)  # Delete the state
    storage.save()  # Save the changes to the storage
    return jsonify({})  # Return an empty dictionary


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new State object"""
    if not request.is_json:  # Check if the body is not JSON
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()  # Parse the JSON request body
    if 'name' not in data:  # Check if the 'name' field is missing
        return jsonify({"error": "Missing name"}), 400
    state = State(name=data['name'])  # Create a new State object
    storage.new(state)  # Add the new state to storage
    storage.save()  # Save the changes to the storage
    return jsonify(state.to_dict()), 201  # Returns new state with status 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a State object"""
    state = storage.get(State, state_id)  # Retrieve the state by its ID
    if not state:
        return jsonify({"error": "Not found"}), 404
    if not request.is_json:  # Check if the body is not JSON
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()  # Parse the JSON request body
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:  # Ignores the fields
            setattr(state, key, value)  # Update the state with the new value
    storage.save()  # Save the changes to the storage
    return jsonify(state.to_dict())  # Return the updated state with status 200
