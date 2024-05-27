#!/usr/bin/python3
"""
Module "amenities.py" - handles all amenities view
"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """
    Return all amenity objects
    """
    amenities = storage.all(Amenity).values()
    return jsonify([x.to_dict() for x in amenities])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id=None):
    """
    Return an Amenity object by amenity_id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """
    Delete an Amenity object with amenity_id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity(state_id=None):
    """
    Creates a new Amenity object
    """
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id=None):
    """
    Updates an Amenity object
    """
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        for k, v in data.items():
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, k, v)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
    else:
        return abort(404)
