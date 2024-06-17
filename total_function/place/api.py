#!/usr/bin/python3
from place_total import Place, Storage
from flask import Flask, jsonify, request
from uuid import UUID
import re

app = Flask(__name__)

"""
POST /place: Create a new place.
GET /places: Retrieve a list of all places.
GET /place/{place_id}: Retrieve details of a specific place.
PUT /places/{place_id}: Update an existing place.
DELETE /places/{place_id}: Delete a place.

"""

@app.route("/")
def home():
    return "Welcome to HBNB"

@app.route("/places")
def get_places():
    return jsonify(Place.get_all())

@app.route("/places/<place_id>")
def get_place(place_id):
    try:
        place_uuid = UUID(place_id)
    except ValueError:
        return jsonify({"error": "Invalid place ID format"}), 400
    place = Place.get(place_uuid)
    if place:
        return jsonify(place.to_dict())
    else:
        return jsonify({"error": "Place not found"}), 404

@app.route('/places', methods=['POST'])
def add_place():
    new_place = request.get_json()
    name = new_place.get("name")
    description = new_place.get("description")
    host_id = new_place.get("host_id")
    try:
        validate_place(name, description, host_id)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    new = Place(name, description, UUID(host_id))
    Place.add_place(new)
    return jsonify({"message": "Place added", "place": new.to_dict()}), 201

@app.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    try:
        place_uuid = UUID(place_id)
    except ValueError:
        return jsonify({"error": "Invalid place ID format"}), 400
    to_update = Place.get(place_uuid)
    if to_update is not None:
        update_data = request.get_json()
        name = update_data.get("name")
        description = update_data.get("description")
        host_id = update_data.get("host_id")

        if name:
            validate_name(name)
            to_update.name = name
        if description:
            validate_description(description)
            to_update.description = description
        if host_id:
            validate_host_id(UUID(host_id))
            to_update.host_id = UUID(host_id)

        Place.update(to_update)
        return jsonify({"message": "Place updated", "place": to_update.to_dict()}), 200
    else:
        return jsonify({"error": "Place not found"}), 404

@app.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    try:
        place_uuid = UUID(place_id)
    except ValueError:
        return jsonify({"error": "Invalid place ID format"}), 400
    to_delete = Place.get(place_uuid)
    if to_delete is not None:
        Place.delete(to_delete)
        return '', 204
    else:
        return jsonify({"error": "Place not found"}), 404

def validate_place(name, description, host_id):
    validate_name(name)
    validate_description(description)
    validate_host_id(host_id)

def validate_name(name):
    if not name or not isinstance(name, str):
        raise ValueError("Name must be a non-empty string")

def validate_description(description):
    if not description or not isinstance(description, str):
        raise ValueError("Description must be a non-empty string")

def validate_host_id(host_id):
    if not host_id or not isinstance(host_id, str) or not UUID(host_id):
        raise ValueError("Host ID must be a valid UUID")

if __name__ == "__main__":
    Storage.load()
    app.run(debug=True)
