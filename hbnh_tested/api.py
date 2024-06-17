from user import User, ConflictError
from country import Country
from city import City
from storage import Storage
from flask import  Flask, jsonify, request
import re
from uuid import UUID

app = Flask(__name__)

"""
POST /users: Create a new user.
GET /users: Retrieve a list of all users.
GET /users/{user_id}: Retrieve details of a specific user.
PUT /users/{user_id}: Update an existing user.
DELETE /users/{user_id}: Delete a user.

"""
@app.route("/")
def home():
    return "Welcome to HBNB"

#####################
#       USER        #
#####################

@app.route("/users")
def get_usernames():
    return jsonify(User.get_all())

@app.route("/users/<user_id>")
def get_user(user_id):
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        return jsonify({"error": "Invalid user ID format"}), 400
    user = User.get(user_uuid)
    if user:
        return jsonify(user.to_dict())
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def add_user():
    new_user = request.get_json()
    email = new_user.get("email")
    first_name = new_user.get("first_name")
    last_name = new_user.get("last_name")
    try:
        validate_user(email, first_name, last_name)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except ConflictError as e:
        return jsonify({"error": str(e)}), 409

    new = User(email, first_name, last_name)
    User.add(new)
    return jsonify({"message": "User added", "user": new.to_dict()}), 201

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        return jsonify({"error": "Invalid user ID format"}), 400
    to_update = User.get(user_uuid)
    if to_update:
        update_data = request.get_json()
        email = update_data.get("email")
        first_name = update_data.get("first_name")
        last_name = update_data.get("last_name")

        if email:
            try:
                validate_email(email)
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
            except ConflictError as e:
                return jsonify({"error": str(e)}), 409
            to_update.email = email

        if first_name:
            try:
                validate_first_name(first_name)
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
            to_update.first_name = first_name

        if last_name:
            try:
                validate_last_name(last_name)
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
            to_update.last_name = last_name

        User.update(to_update)
        return jsonify({"message": "User updated", "user": to_update.to_dict()}), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        return jsonify({"error": "Invalid user ID format"}), 400
    to_delete = User.get(user_uuid)
    if to_delete:
        User.delete(to_delete)
        return '', 204
    else:
        return jsonify({"error": "User not found"}), 404

def validate_user(email, first_name, last_name):
    validate_first_name(first_name)
    validate_last_name(last_name)
    validate_email(email)

def validate_email(email):
    if not email or not isinstance(email, str) or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Invalid email format.")

    User.validate_email(email)

def validate_first_name(first_name):
    if not first_name or not isinstance(first_name, str) or not first_name.isalpha():
        raise ValueError("First name must be a non-empty string with only alphabetic characters.")

def validate_last_name(last_name):
    if not last_name or not isinstance(last_name, str) or not last_name.isalpha():
        raise ValueError("Last name must be a non-empty string with only alphabetic characters.")




#####################
#       COUNTRY     #
#####################

@app.route("/countries")
def get_countries():
    return jsonify(Country.get_all())

@app.route("/countries/<country_code>")
def get_country(country_code):
    try:
        validate_country_code(country_code)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    country = Country.get(country_code)

    if country:
        return jsonify(country.to_dict())
    else:
        return jsonify({"error": "Country not found"}), 404
    
@app.route("/countries/<country_code>/cities")
def get_country_cities(country_code):
    try:
        validate_country_code(country_code)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    country = Country.get(country_code)
    
    if country:
        cities = Country.cities(country_code)
        return jsonify(cities)
    else:
        return jsonify({"error": "Country not found"}), 404

def validate_country_code(code):
    if not code or not isinstance(code, str) or not code.isalpha() or len(code) != 2:
        raise ValueError("Country code must be a non-empty string with only two alphabetic characters.")
    code = code.upper()


#####################
#       CITY        #
#####################
def validate_city_type_name(name):
    if not name or not isinstance(name, str) or len(name) == 0:
        raise TypeError("City name must be a non-empty string with only alphabetic characters")
    
def validate_city(name, country_code):
    validate_city_type_name(name)
    validate_country_code(country_code)
    City.validate_city_country_code(country_code)
    City.validate_city_name(name, country_code)

@app.route('/cities', methods=['POST'])
def create_city():
    data = request.get_json()
    try:
        new_city = City(data['name'], data['country_code'])
        new_city.add()
        return jsonify(new_city.to_dict()), 201
    except TypeError as e:
                return jsonify({"error": str(e)}), 400
    except ValueError as e:
                return jsonify({"error": str(e)}), 409

@app.route("/cities")
def get_cities():
    return jsonify(City.get_all())

@app.route("/cities/<city_id>")
def get_city(city_id):
    try:
        city_uuid = UUID(city_id)
        city = City.get(city_uuid)
        if city:
            return jsonify(city.to_dict())
        else:
            return jsonify({"error": "City not found"}), 404
    except ValueError:
        return jsonify({"error": "Invalid city ID format"}), 400

@app.route("/cities/<city_id>", methods=['PUT'])
def update_city(city_id):
    try:
        city_uuid = UUID(city_id)
    except ValueError:
        return jsonify({"error": "Invalid user ID format"}), 400
    to_update = City.get(city_uuid)
    
    if to_update:
        update_data = request.get_json()
        name = update_data.get("name")
        country_code = update_data.get("country_code")
        
        if name:
            try:
                validate_city_type_name(name)
            except TypeError as e:
                return jsonify({"error": str(e)}), 400
            to_update.name = name
        
        if country_code:
            try:
                validate_country_code(country_code)
            except TypeError as e:
                    return jsonify({"error": str(e)}), 400
            except ValueError as e:
                    return jsonify({"error": str(e)}), 409
            to_update.country_code = country_code
            
        City.update(to_update)
        return jsonify(to_update.to_dict())
    else:
        return jsonify({"error": "City not found"}), 404

@app.route("/cities/<city_id>", methods=['DELETE'])
def delete_city(city_id):
    try:
        city_uuid = UUID(city_id)
    except ValueError:
        return jsonify({"error": "Invalid user ID format"}), 400
    city = City.get(city_uuid)
    if not city:
        return jsonify({"error": "City not found"}), 404
    City.delete(city)
    return '', 204

if __name__ == "__main__":
    Storage.load()
    app.run(debug=True)