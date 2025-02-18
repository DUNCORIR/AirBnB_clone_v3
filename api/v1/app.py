#!/usr/bin/python3
"""
Flask application for the AirBnB clone API.
This module sets up the Flask app and registers blueprints
for handling various API endpoints, including state, city,
user, and place management.
"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
# Enable CORS with wildcard origin for all resources
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
# Register Blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Close the storage session on app context teardown."""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors and returns a JSON response."""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
