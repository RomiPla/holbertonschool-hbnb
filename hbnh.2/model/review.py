"""
    Creacion clase review
"""
from basemodel import Basemodel
from place import Place
from user import User

class Review (Basemodel):
    review_storage = {}

    def __init__(self, place_id, user_id, rating, comment):
        super().__init__()
        self.place_id = place_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment

        if place_id not in Place.place_storage:
            raise ValueError(f"Place with id {place_id} does not exist.")
        if user_id not in User.user_emails:
            raise ValueError(f"User with id {user_id} does not exist.")

    def add_review_to(self, review):
        self.reviews.append(review.id)
