#!/usr/bin/python3
"""Handles all default RESTful API actions for Place-Amenity relationships"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from flask import abort


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenities(place_id):
    """Retrieve all Amenity objects linked to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenities = place.amenities  # Depends on the relationship setup in models
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>', methods=['DELETE']
)
def delete_amenity_from_place(place_id, amenity_id):
    """Deletes an Amenity from a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()  # Save changes to the storage
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_amenity_to_place(place_id, amenity_id):
    """Links an Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200

    place.amenities.append(amenity)
    storage.save()  # Save changes to the storage
    return jsonify(amenity.to_dict()), 201
