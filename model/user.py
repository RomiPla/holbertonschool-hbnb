from basemodel import Basemodel

class User(Basemodel):
    def __init__(self, email, first_name, last_name):
        super().__init__()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.places = []
        self.reviews = []

    def add_place(self, Place):
        self.places.append(Place)

    def add_review(self, Review):
        self.reviews.append(Review)
