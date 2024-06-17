#!/usr/bin/python3
from user_total import User, Storage, ConflictError
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
    User.add_user(new)
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

if __name__ == "__main__":
    Storage.load()
    app.run(debug=True)