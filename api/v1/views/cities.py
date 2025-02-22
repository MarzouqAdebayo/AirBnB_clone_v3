#!/usr/bin/python3
"""
Module "cities.py" - Defines all views for cities
"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """
    Return all cities of a state
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """
    Return a city object with city_id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Delete a city object with city_id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Create a new city object under a state
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data.keys():
        abort(400, "Missing name")
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    data['state_id'] = state_id
    new_city = City(**data)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """
    Update a city object city_id
    """
    data = request.get_json()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not data:
        abort(400, "Not a JSON")
    for k, v in data.items():
        setattr(city, k, v)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
