from user import User, ConflictError
from country import Country
from city import City
from storage import Storage
from place import Place
from flask import  Flask, jsonify, request
import re
from uuid import UUID
from amenity import Amenity

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


#####################
#     AMENITY       #
#####################

def validate_amenity_name(name):
    if not name or not isinstance(name, str):
        raise TypeError("Name must be a non-empty string")
def validate_amenity_description(description):
    if not description or not isinstance(description, str):
        raise TypeError("Description must be a non-empty string")

def validate_amenity(name, description):
        validate_amenity_name(name)
        validate_amenity_description(description)
        

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
    description = new_amenity.get("description")
    try:
        validate_amenity(name, description)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    new = Amenity(name, description)
    Amenity.add(new)
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
        description = update_data.get("description")

        if name:
            validate_amenity_name(name)
            to_update.name = name
        if description:
            validate_amenity_description(description)
            to_update.description = description

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
    
#####################
#     PLACE         #
#####################

@app.route("/places")
def get_places():
    return jsonify(Place.get_all())

@app.route("/places/<place_id>")
def get_place(place_id):
    try:
        place_uuid = UUID(place_id)
    except ValueError:
        return jsonify({"error": "Invalid user ID format"}), 400
    place = Place.get(place_uuid)
    if place:
        return jsonify(place.to_dict())
    else:
        return jsonify({"error": "Place not found"}), 404
    
@app.route('/places', methods=['POST'])
def add_place():
    data = request.get_json()
    required_fields = ['host_id', 'name', 'description', 'number_of_rooms', 'number_of_bathrooms', 
                       'max_guests', 'price_per_night', 'latitude', 'longitude', 'city_id', 'amenity_ids']
    for field in required_fields:
        if field not in data:
            return jsonify(f"Missing required field: {field}"), 400

    try:
        validate_place(UUID(data.get("host_id")), data.get("name"), data.get("description"),
                       data.get("number_of_rooms"), data.get("number_of_bathrooms"),
                       data.get("max_guests"), data.get("price_per_night"),
                       data.get("latitude"), data.get("longitude"), UUID(data.get("city_id")))
    except TypeError as e:
        return jsonify({"error": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    new = Place(UUID(data.get("host_id")), data.get("name"), data.get("description"),
                       data.get("number_of_rooms"), data.get("number_of_bathrooms"),
                       data.get("max_guests"), data.get("price_per_night"),
                       data.get("latitude"), data.get("longitude"), UUID(data.get("city_id")),
                       data.get("amenity_ids"))
    Place.add(new)
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
        host_id = update_data.get("host_id")
        name = update_data.get("name")
        description = update_data.get("description")
        number_of_rooms = update_data.get("number_of_rooms")
        number_of_bathrooms = update_data.get("number_of_bathrooms")
        max_guests = update_data.get("max_guests")
        price_per_night = update_data.get("price_per_night")
        latitude = update_data.get("latitude")
        longitude = update_data.get("longitude")
        city_id = update_data.get("city_id")
        amenity_ids = update_data.get("amenity_ids")

        if name:
            validate_place_name(name)
            to_update.name = name
        if description:
            to_update.description = description
        if host_id:
            Place.validate_place_host_id(UUID(host_id))
            to_update.host_id = UUID(host_id)
        if number_of_rooms:
            validate_place_number_of_rooms(number_of_rooms)
            to_update.number_of_rooms = number_of_rooms
        if number_of_bathrooms:
            validate_place_number_of_bathrooms(number_of_bathrooms)
            to_update.number_of_bathrooms = number_of_bathrooms
        if max_guests:
            validate_place_max_guests(max_guests)
            to_update.max_guests = max_guests
        if price_per_night:
            validate_place_price_per_night(price_per_night)
            to_update.price_per_night = price_per_night
        if latitude:
            validate_place_latitude(latitude)
            to_update.latitude = latitude
        if longitude:
            validate_place_longitude(longitude)
            to_update.longitude = longitude
        if city_id:
            Place.validate_place_city_id(UUID(city_id))
            to_update.city_id = (UUID(city_id))
        if amenity_ids:
            to_update.amenity_ids = amenity_ids

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

def validate_place_name(name):
    if not re.match(r"^[A-Za-z0-9\s]+$", name):
        raise TypeError("Name cannot contain special characters.")

def validate_place_number_of_rooms(number_of_rooms):
    if not isinstance(number_of_rooms, int) or number_of_rooms < 0:
        raise TypeError("Number of rooms must be a positive integer.")
    
def validate_place_number_of_bathrooms(number_of_bathrooms):
    if not isinstance(number_of_bathrooms, int) or number_of_bathrooms < 0:
        raise TypeError("Number of bathrooms must be a positive integer.")

def validate_place_max_guests(max_guests):
    if not isinstance(max_guests, int) or max_guests < 0:
        raise TypeError("Max guests must be a positive integer.")
    
def validate_place_price_per_night(price_per_night):
    if not isinstance(price_per_night, (int, float)) or price_per_night < 0:
        raise TypeError("Price by nigth must be a positive number.")

def validate_place_latitude(latitude):
    if not isinstance(latitude, (int, float)):
        raise TypeError("Latitude must be a number.")
    if not (-90 <= latitude <= 90):
            raise TypeError("Latitude must be between -90 and 90 degrees.")

def validate_place_longitude(longitude):
    if not isinstance(longitude, (int, float)):
        raise TypeError("Longitude must be a number.")

    if not (-180 <= longitude <= 180):
        raise TypeError("Longitude must be between -180 and 180 degrees.")

def validate_place(host_id, name, description, number_of_rooms, number_of_bathrooms,\
                 max_guests, price_per_night, latitude, longitude, city_id):

        if not host_id or not name or not description or not number_of_rooms\
            or not  number_of_bathrooms or not max_guests or not price_per_night\
                or not latitude or not longitude or not city_id:
            raise TypeError("All fields must be filled in.")

        validate_place_name(name)

        validate_place_number_of_rooms(number_of_rooms)

        validate_place_number_of_bathrooms(number_of_bathrooms)

        validate_place_max_guests(max_guests)

        validate_place_price_per_night(price_per_night)

        validate_place_latitude(latitude)

        validate_place_longitude(longitude)

        Place.validate_place_data(host_id, city_id)

if __name__ == "__main__":
    Storage.load()
    app.run(debug=True)