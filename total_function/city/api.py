#!/usr/bin/python3
from city_total import City, Storage
from flask import Flask, jsonify, request
import re
from uuid import UUID

app = Flask(__name__)

"""
POST /cities: Create a new city.
GET /cities: Retrieve a list of all cities.
GET /cities/{city_id}: Retrieve details of a specific city.
PUT /cities/{city_id}: Update an existing city.
DELETE /cities/{city_id}: Delete a city.
"""

@app.route("/")
def home():
    return "Welcome to HBNB"

@app.route("/cities")
def get_cities():
    return jsonify(City.get_all())

@app.route("/cities/<city_id>", methods=['GET'])
def get_city(city_id):
    try:
        city_uuid = UUID(city_id)
    except ValueError:
        return jsonify({"error": "Invalid city ID format"}), 400
    city = City.get(city_uuid)
    if city:
        return jsonify(city.to_dict())
    else:
        return jsonify({"error": "City not found"}), 404

@app.route('/cities', methods=['POST'])
def add_city():
    new_city = request.get_json()
    name = new_city.get("name")
    country = new_city.get("country")
    try:
        validate_city(name, country)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    new = City(name, country)
    City.add_city(new)
    return jsonify({"message": "City added", "city": new.to_dict()}), 201

@app.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    to_update = City.get(city_id)
    if to_update is not None:
        update_data = request.get_json()
        name = update_data.get("name")
        country = update_data.get("country")

        if name:
            validate_name(name)
            to_update.name = name
        if country:
            validate_country(country)
            to_update.country = country

        City.update(to_update)
        return jsonify({"message": "City updated", "city": to_update.to_dict()}), 200
    else:
        return jsonify({"error": "City not found"}), 404

@app.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    to_delete = City.get(city_id)
    if to_delete is not None:
        City.delete(to_delete)
        return '', 204
    else:
        return jsonify({"error": "City not found"}), 404

def validate_city(name, country):
    validate_name(name)
    validate_country(country)

def validate_name(name):
    if not name or not isinstance(name, str):
        raise ValueError("Name must be a non-empty string.")

def validate_country(country):
    if not country or not isinstance(country, str):
        raise ValueError("Country must be a non-empty string.")

if __name__ == "__main__":
    Storage.load()
    app.run(debug=True)
