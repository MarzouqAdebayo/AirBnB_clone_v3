#!/usr/bin/python3
"""
Module "app.py" - Main flask app module
"""
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage
from os import getenv


env_host = getenv('HBNB_API_HOST') or '0.0.0.0'
env_port = getenv('HBNB_API_PORT') or 5000

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(error):
    """ Close db session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Handles non existent paths"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    """Run flask app"""
    app.run(host=env_host, port=env_port,
            debug=True, threaded=True)
