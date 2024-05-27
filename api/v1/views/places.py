#!/usr/bin/python3
"""Module "places.py" - handles all views for places route"""
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route('/api/v1/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id = None):
    """
    Return place objects that belong to city with id city_id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Return place with id place_id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Delete place object with id place_id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Create new place under city with id city_Id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    req = request.get_json()
    if not isinstance(req, dict):
        abort(400, description="Not a JSON")
    user_id = req.get("user_id")
    if not user_id:
        abort(400, description="Missing user_id")
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    place_name = req.get('name')
    if not place_name:
        abort(400, description='Missing name')
    new_place = Place(**req)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update existing place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    req = request.get_json()
    if not isinstance(req, dict):
        abort(400, description="Not a JSON")
    for key, value in req.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
