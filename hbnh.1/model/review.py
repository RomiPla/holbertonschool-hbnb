#!/usr/bin/python3

"""
    Creacion clase review
"""
from basemodel import Basemodel
from place import Place
from user import User
import re

class Review(Basemodel):
    def __init__(self, user_id, place_id, rating, comment):
        self.validate_review(user_id, place_id, rating, comment)
        
        super().__init__()
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating
        self.comment = comment
        
        self.save_data()

    def validate_review(self, user_id, place_id, rating, comment):
        if not user_id or not place_id or rating is None:
            raise ValueError("User ID, Place ID, and Rating must be provided.")

        if not isinstance(rating, (int, float)) or not (1 <= rating <= 5):
            raise ValueError("Rating must be a number between 1 and 5.")

        if not isinstance(comment, str):
            raise ValueError("Comment must be a string.")

        if len(comment) > 500:
            raise ValueError("Comment cannot be longer than 500 characters.")

    def __setattr__(self, key, value):
        if key in ['user_id', 'place_id', 'rating', 'comment']:
            temp_user_id = self.user_id if key != 'user_id' else value
            temp_place_id = self.place_id if key != 'place_id' else value
            temp_rating = self.rating if key != 'rating' else value
            temp_comment = self.comment if key != 'comment' else value
            self.validate_review(temp_user_id, temp_place_id, temp_rating, temp_comment)
        super().__setattr__(key, value)

    @property
    def user(self):
        return self.data["user"].get(self.user_id)

    @property
    def place(self):
        return self.data["place"].get(self.place_id)
