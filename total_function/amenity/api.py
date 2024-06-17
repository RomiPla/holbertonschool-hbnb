#!/usr/bin/python3
from amenity_total import Amenity, Storage
from flask import  Flask, jsonify, request
import re
from uuid import UUID

app = Flask(__name__)

"""
POST /Amenities: Create a new amenity.
GET /Amenities: Retrieve a list of all amenities.
GET /Amenities/{amenity_id}: Retrieve details of a specific amenity.
PUT /Amenities/{amenity_id}: Update an existing amenity.
DELETE /amenities/{amenity_id}: Delete a amenity.

"""
@app.route("/")
def home():
    return "Welcome to HBNB"

@app.route("/amenities")
def get_amenities():
    return jsonify(Amenity.get_all())

@app.route("/amenities/<amenity_id>", methods=['GET'])
def get_amenity(amenity_id):
    try:
        amenity_uuid = UUID(amenity_id)
    except ValueError:
        return jsonify({"error": "Invalid amenity ID format"}), 400
    amenity = Amenity.get(amenity_uuid)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        return jsonify({"error": "Amenity not found"}), 404

@app.route('/amenities', methods=['POST'])
def add_amenity():
    new_amenity = request.get_json()
    name = new_amenity.get("name")
    try:
        validate_amenity(name)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    new = Amenity(name)
    Amenity.add_amenity(new)
    return jsonify({"message": "Amenity added", "amenity": new.to_dict()}), 201

@app.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    try:
        amenity_uuid = UUID(amenity_id)
    except ValueError:
        return jsonify({"error": "Invalid amenity ID format"}), 400
    to_update = Amenity.get(amenity_uuid)
    if to_update is not None:
        update_data = request.get_json()
        name = update_data.get("name")

        if name:
            validate_amenity(name)
            to_update.name = name

        Amenity.update(to_update)
        return jsonify({"message": "Amenity updated", "amenity": to_update.to_dict()}), 200
    else:
        return jsonify({"error": "Amenity not found"}), 404

@app.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    try:
        amenity_uuid = UUID(amenity_id)
    except ValueError:
        return jsonify({"error": "Invalid amenity ID format"}), 400
    to_delete = Amenity.get(amenity_uuid)
    if to_delete is not None:
        Amenity.delete(to_delete)
        return '', 204
    else:
        return jsonify({"error": "Amenity not found"}), 404

def validate_amenity(name):
    if not name or not isinstance(name, str):
        raise ValueError("Amenity name must be a non-empty string")

if __name__ == "__main__":
    Storage.load()
    app.run(debug=True)
