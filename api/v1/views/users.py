#!/usr/bin/python3
"""
Module "users.py" - handles all the views for User object
"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """Return all User objects"""
    return jsonify([x.to_dict() for x in storage.all(User).values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id=None):
    """Return User with id user_id"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id=None):
    """Delete User object with id user_id"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new User object"""
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in data:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in data:
        return make_response(jsonify({'error': 'Missing password'}), 400)
    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id=None):
    """Update an existing User object"""
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    user = storage.get(User, user_id)
    if user:
        for k, v in data.items():
            if key not in ['id', 'created_at', 'updated_at', 'email']:
                setattr(user, k, v)
        storage.save()
        return make_response(jsonify(user.to_dict()), 200)
    abort(404)
