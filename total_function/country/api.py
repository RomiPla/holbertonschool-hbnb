#!/usr/bin/python3
from country_total import Country, Storage
from flask import Flask, jsonify, request
import re
from uuid import UUID

app = Flask(__name__)

"""
POST /countries: Create a new country.
GET /countries: Retrieve a list of all countries.
GET /countries/{country_id}: Retrieve details of a specific country.
PUT /countries/{country_id}: Update an existing country.
DELETE /countries/{country_id}: Delete a country.
"""

@app.route("/")
def home():
    return "Welcome to HBNB"

@app.route("/countries")
def get_countries():
    return jsonify(Country.get_all())

@app.route("/countries/<country_id>")
def get_country(country_id):
    try:
        country_uuid = UUID(country_id)
    except ValueError:
        return jsonify({"error": "Invalid country ID format"}), 400
    country = Country.get(country_uuid)
    if country:
        return jsonify(country.to_dict())
    else:
        return jsonify({"error": "Country not found"}), 404
    
@app.route('/countries', methods=['POST'])
def add_country():
    new_country_data = request.get_json()
    name = new_country_data.get("name")
    capital = new_country_data.get("capital")
    population = new_country_data.get("population")

    try:
        validate_country(name, capital, population)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    new_country = Country(name, capital, population)
    Country.add_country(new_country)
    return jsonify({"message": "Country added", "country": new_country.to_dict()}), 201

@app.route('/countries/<country_id>', methods=['PUT'])
def update_country(country_id):
    to_update = get_country(country_id)
    if to_update is not None:
        update_data = request.get_json()
        name = update_data.get("name")
        capital = update_data.get("capital")
        population = update_data.get("population")

        if name:
            validate_name(name)
            to_update.name = name
        if capital:
            validate_capital(capital)
            to_update.capital = capital
        if population:
            validate_population(population)
            to_update.population = population

        Country.update(to_update)
        return jsonify({"message": "Country updated", "country": to_update.to_dict()}), 200
    else:
        return jsonify({"error": "Country not found"}), 404
    
@app.route('/countries/<country_id>', methods=['DELETE'])
def delete_country(country_id):
    to_delete = get_country(country_id)
    if to_delete is not None:
        Country.delete(to_delete)
        return '', 204
    else:
        return jsonify({"error": "Country not found"}), 404

def validate_country(name, capital, population):
    validate_name(name)
    validate_capital(capital)
    validate_population(population)

def validate_name(name):
    if not name or not isinstance(name, str):
        raise ValueError("Name must be a non-empty string.")

def validate_capital(capital):
    if not capital or not isinstance(capital, str):
        raise ValueError("Capital must be a non-empty string.")

def validate_population(population):
    if not isinstance(population, int) or population < 0:
        raise ValueError("Population must be a non-negative integer.")

if __name__ == "__main__":
    Storage.load()
    app.run(debug=True)
