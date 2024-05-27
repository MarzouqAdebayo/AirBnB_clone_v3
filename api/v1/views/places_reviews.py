#!/usr/bin/python3
"""Module "places_reviews.py" - handles all views for places_reviews route"""
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route('places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """
    Return all Review object for a Place object with id place_id
    """
    place = storage.get(Place, place_id)
    if place:
        return jsonify([review.to_dict() for review in place.reviews])
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Return Review object with id review_id
    """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Delete Review object with id review_id
    """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id=None):
    """
    Create a new Review for Place object place_id
    """
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if not data.get('user_id'):
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if not data.get('text'):
        return make_response(jsonify({'error': 'Missing text'}), 400)
    place = storage.get(Place, place_id)
    user = storage.get(User, data['user_id'])
    if place and user:
        new_review = Review(**data)
        new_review.place_id = place.id
        storage.new(new_review)
        storage.save()
        return make_response(jsonify(new_review.to_dict()), 201)
    abort(404)
