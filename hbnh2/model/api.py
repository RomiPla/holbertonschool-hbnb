#!/usr/bin/python3
from flask import  Flask, jsonify, request
from model.user import User
import re

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

@app.route("/users")
def get_usernames():
    return jsonify(User.get_all())

@app.route("/users/<user_id>")
def get_user(user_id):
    user = User.get(user_id)
    if user:
        return jsonify(user.__dict__)
    else:
        return jsonify({"error": "User not found"}), 404
    
@app.route('/users', methods=['POST'])
def add_user():
    new_user = request.get_json()
    email = new_user.get("email")
    first_name = new_user.get("first_name")
    last_name = new_user.get("last_name")
    validate_user(email, first_name, last_name)
    new = User(email, first_name, last_name)
    User.add_user(new)
    return jsonify({"message": "User added", "user": new}), 201

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    to_update = get_user(user_id)
    if to_update:
        User.update(to_update)
    else:
        return jsonify({"error": "User not found"}), 404
    
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    to_delete = get_user(user_id)
    if to_delete:
        User.delete(to_delete)
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0')






def validate_user(email, first_name, last_name):
        if not email or not first_name or not last_name:
            return jsonify({"error": "All fields must be filled in."}), 400
        
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            return jsonify({"error": "Invalid email format."}), 400

        if not isinstance(first_name, str) or not isinstance(last_name, str):
            return jsonify({"error": "First name and last name must be strings."}), 400
        
        if not re.match(r"^[A-Za-z]+$", first_name):
            return jsonify({"error": "First name cannot contain numbers or \
special characters."}), 400
        
        if not re.match(r"^[A-Za-z]+$", last_name):
            return jsonify({"error": "Last name cannot contain numbers or \
special characters."}), 400
        
        if not User.validate_email(email):
            return jsonify({"error": "Email already taken"}), 409
