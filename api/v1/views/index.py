#!/usr/bin/python3
"""Controller that returns the status of the application"""
from flask import jsonify
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", strict_slashes=False)
def status():
    """
    View function that returns status of the app as json
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def count():
    """
    View function that returns count of all objects by type
    """
    return jsonify({
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    })
