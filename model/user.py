from basemodel import Basemodel

class User(Basemodel):
    user_emails = {}
    def __init__(self, email, first_name, last_name):
        super().__init__()
        if email in User.user_emails.values():
            raise ValueError(f"Email {email} already in use.")

        """if email is @:
            self.email = email
        else:
            raise TypeError("email de vrg")"""
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.places = []
        self.reviews = []
        User.user_emails[self.id] = email

    def add_place(self, Place):
        self.places.append(Place)

    def add_review(self, Review):
        self.reviews.append(Review)
