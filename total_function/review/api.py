#!/usr/bin/python3
from review_total import Review, Storage
from flask import Flask, jsonify, request
import re
from uuid import UUID

app = Flask(__name__)

"""
POST /reviews: Create a new review.
GET /reviews: Retrieve a list of all reviews.
GET /reviews/{review_id}: Retrieve details of a specific review.
PUT /reviews/{review_id}: Update an existing review.
DELETE /reviews/{review_id}: Delete a review.
"""

@app.route("/")
def home():
    return "Welcome to Reviews API"

@app.route("/reviews")
def get_reviews():
    return jsonify(Review.get_all())

@app.route("/reviews/<review_id>")
def get_review(review_id):
    try:
        review_uuid = UUID(review_id)
    except ValueError:
        return jsonify({"error": "Invalid review ID format"}), 400
    
    review = Review.get(review_uuid)
    if review:
        return jsonify(review.to_dict())
    else:
        return jsonify({"error": "Review not found"}), 404
    
@app.route('/reviews', methods=['POST'])
def add_review():
    new_review = request.get_json()
    title = new_review.get("title")
    content = new_review.get("content")
    rating = new_review.get("rating")
    
    try:
        validate_review(title, content, rating)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    new = Review(title, content, rating)
    Review.add_review(new)
    return jsonify({"message": "Review added", "review": new.to_dict()}), 201

@app.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    try:
        review_uuid = UUID(review_id)
    except ValueError:
        return jsonify({"error": "Invalid review ID format"}), 400
    
    to_update = Review.get(review_uuid)
    if to_update:
        update_data = request.get_json()
        title = update_data.get("title")
        content = update_data.get("content")
        rating = update_data.get("rating")

        try:
            if title:
                validate_title(title)
                to_update.title = title
            if content:
                validate_content(content)
                to_update.content = content
            if rating:
                validate_rating(rating)
                to_update.rating = rating
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        Review.update(to_update)
        return jsonify({"message": "Review updated", "review": to_update.to_dict()}), 200
    else:
        return jsonify({"error": "Review not found"}), 404
    
@app.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    try:
        review_uuid = UUID(review_id)
    except ValueError:
        return jsonify({"error": "Invalid review ID format"}), 400
    
    to_delete = Review.get(review_uuid)
    if to_delete:
        Review.delete(to_delete)
        return '', 204
    else:
        return jsonify({"error": "Review not found"}), 404


def validate_review(title, content, rating):
    validate_title(title)
    validate_content(content)
    validate_rating(rating)

def validate_title(title):
    if not title or not isinstance(title, str):
        raise ValueError("Title must be a non-empty string.")

def validate_content(content):
    if not content or not isinstance(content, str):
        raise ValueError("Content must be a non-empty string.")

def validate_rating(rating):
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        raise ValueError("Rating must be an integer between 1 and 5.")

if __name__ == "__main__":
    Storage.load()
    app.run(debug=True)
