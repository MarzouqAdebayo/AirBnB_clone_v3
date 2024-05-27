#!/usr/bin/python3
"""
Module "states.py" handles all states views
"""
from flask import jsonify, abort, request, Response, make_response
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False)
def get_all_states():
    """
    Return all state objects
    """
    all_states = storage.all(State).values()
    states = [obj.to_dict() for obj in all_states]
    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state(state_id):
    """
    Return a state object with id state_id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state = state.to_dict()
    return jsonify(state)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Delete a state object with id state_id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """
    Create a new State object
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data.keys():
        abort(400, "Missing name")
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """
    Create a new State object
    """
    data = request.get_json()
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
