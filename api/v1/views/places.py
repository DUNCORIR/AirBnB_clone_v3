#!/usr/bin/python3
"""
Handles all default RESTFul API actions for Place objects
"""

from flask import Flask, jsonify, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User

app = Flask(__name__)


@app.route('/api/v1/cities/<city_id>/places', methods=['GET'])
def get_places_by_city(city_id):
    """Retrieve all Place objects of a specific City"""
    # Fetch the city object using the city_id
    city = storage.get(City, city_id)
    if not city:
        # Return 404 error if city not found
        return jsonify({"error": "City not found"}), 404
    # Return the list of places in the city
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app.route('/api/v1/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieve a single Place object by place_id"""
    # Fetch the place object using the place_id
    place = storage.get(Place, place_id)
    if not place:
        # Return 404 error if place not found
        return jsonify({"error": "Place not found"}), 404
    # Return the place as a dictionary
    return jsonify(place.to_dict())


@app.route('/api/v1/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Delete a Place object by place_id"""
    # Fetch the place object using the place_id
    place = storage.get(Place, place_id)
    if not place:
        # Return 404 error if place not found
        return jsonify({"error": "Place not found"}), 404
    # Delete the place object from storage
    storage.delete(place)
    storage.save()
    # Return an empty dictionary with status code 200
    return jsonify({}), 200


@app.route('/api/v1/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Create a new Place object for a specific City"""
    # Fetch the city object using the city_id
    city = storage.get(City, city_id)
    if not city:
        # Return 404 error if city not found
        return jsonify({"error": "City not found"}), 404
    # Parse the request body as JSON
    data = request.get_json()
    if not data:
        # Return 400 error if the body is not JSON
        return jsonify({"error": "Not a JSON"}), 400
    # Check for the presence of user_id and name in the data
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, data['user_id'])
    if not user:
        return jsonify({"error": "User not found"}), 404
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    # Create a new place object and save it to storage
    place = Place(name=data['name'], city_id=city.id, user_id=user.id)
    storage.new(place)
    storage.save()
    # Return the created place with status code 201
    return jsonify(place.to_dict()), 201


@app.route('/api/v1/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Update an existing Place object by place_id"""
    # Fetch the place object using the place_id
    place = storage.get(Place, place_id)
    if not place:
        # Return 404 error if place not found
        return jsonify({"error": "Place not found"}), 404
    # Parse the request body as JSON
    data = request.get_json()
    if not data:
        # Return 400 error if the body is not JSON
        return jsonify({"error": "Not a JSON"}), 400
    # Update the place with valid data, ignoring some fields
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    # Save the updated place to storage
    storage.save()
    # Return the updated place with status code 200
    return jsonify(place.to_dict()), 200


@app.route('/api/v1/places_search', methods=['POST'])
def places_search():
    """Search for places based on states, cities, and amenities"""
    # Step 1: Check if the body is valid JSON
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    # Step 2: Parse the JSON body
    filters = request.get_json()

    states = filters.get("states", [])
    cities = filters.get("cities", [])
    amenities = filters.get("amenities", [])

    # Step 3: Handle the case where there is no valid search data
    places = storage.all(Place).values()

    if not states and not cities and not amenities:
        # No filters, return all places
        return jsonify([place.to_dict() for place in places])

    # Step 4: Apply the filter by states
    if states:
        state_places = []
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    # Add all places from the cities of the state
                    state_places.extend(city.places)
        places = set(state_places)  # Remove duplicates

    # Step 5: Apply the filter by cities
    if cities:
        city_places = []
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                city_places.extend(city.places)
        # Combine with the state search results
        places = set(places).union(set(city_places))

    # Step 6: Apply the filter by amenities
    if amenities:
        amenity_filtered_places = []
        for place in places:
            if all(amenity in place.amenities for amenity in amenities):
                amenity_filtered_places.append(place)
        places = amenity_filtered_places

    # Step 7: Return the final list of places
    return jsonify([place.to_dict() for place in places])


@app.teardown_appcontext
def teardown(exc):
    """Closes the storage session after each request"""
    storage.close()


if __name__ == "__main__":
    # Start the Flask application
    app.run(host='0.0.0.0', port=5000, threaded=True)
