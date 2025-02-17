#!/usr/bin/python3
"""
Handles all default RESTFul API actions for Review objects
"""

from flask import Flask, jsonify, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review

app = Flask(__name__)


@app.route('/api/v1/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place(place_id):
    """Retrieve all Review objects for a specific Place"""
    # Fetch the place object using place_id
    place = storage.get(Place, place_id)
    if not place:
        # Return 404 error if place not found
        return jsonify({"error": "Place not found"}), 404
    # Return the list of reviews associated with the place
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app.route('/api/v1/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """Retrieve a single Review object by review_id"""
    # Fetch the review object using review_id
    review = storage.get(Review, review_id)
    if not review:
        # Return 404 error if review not found
        return jsonify({"error": "Review not found"}), 404
    # Return the review as a dictionary
    return jsonify(review.to_dict())


@app.route('/api/v1/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Delete a Review object by review_id"""
    # Fetch the review object using review_id
    review = storage.get(Review, review_id)
    if not review:
        # Return 404 error if review not found
        return jsonify({"error": "Review not found"}), 404
    # Delete the review object from storage
    storage.delete(review)
    storage.save()
    # Return an empty dictionary with status code 200
    return jsonify({}), 200


@app.route('/api/v1/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Create a new Review object for a specific Place"""
    # Fetch the place object using place_id
    place = storage.get(Place, place_id)
    if not place:
        # Return 404 error if place not found
        return jsonify({"error": "Place not found"}), 404
    # Parse the request body as JSON
    data = request.get_json()
    if not data:
        # Return 400 error if the body is not JSON
        return jsonify({"error": "Not a JSON"}), 400
    # Check for the presence of user_id and text in the data
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, data['user_id'])
    if not user:
        return jsonify({"error": "User not found"}), 404
    if 'text' not in data:
        return jsonify({"error": "Missing text"}), 400
    # Create a new review object and save it to storage
    review = Review(text=data['text'], place_id=place.id, user_id=user.id)
    storage.new(review)
    storage.save()
    # Return the created review with status code 201
    return jsonify(review.to_dict()), 201


@app.route('/api/v1/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Update an existing Review object by review_id"""
    # Fetch the review object using review_id
    review = storage.get(Review, review_id)
    if not review:
        # Return 404 error if review not found
        return jsonify({"error": "Review not found"}), 404
    # Parse the request body as JSON
    data = request.get_json()
    if not data:
        # Return 400 error if the body is not JSON
        return jsonify({"error": "Not a JSON"}), 400
    # Update the review with valid data, ignoring some fields
    for key, value in data.items():
        if key not in [
            'id', 'user_id', 'place_id', 'created_at', 'updated_at'
        ]:
            setattr(review, key, value)
    # Save the updated review to storage
    storage.save()
    # Return the updated review with status code 200
    return jsonify(review.to_dict()), 200


@app.teardown_appcontext
def teardown(exc):
    """Closes the storage session after each request"""
    storage.close()


if __name__ == "__main__":
    # Start the Flask application
    app.run(host='0.0.0.0', port=5000, threaded=True)
