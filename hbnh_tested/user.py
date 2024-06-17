from basemodel import Basemodel, DataManager
from uuid import UUID
from datetime import datetime
import re

class ConflictError(Exception):
    pass

class User(Basemodel):
    def __init__(self, email, first_name, last_name):
        self.validate_user(email, first_name, last_name)
        super().__init__()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def to_dict(self):
        return {
            'id': str(self.id),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            '__class__': self.__class__.__name__
        }
    
    @classmethod
    def to_obj(cls, dict_obj):
        id = UUID(dict_obj['id'])
        created_at = datetime.fromisoformat(dict_obj['created_at'])
        updated_at = datetime.fromisoformat(dict_obj['updated_at'])
        email = dict_obj['email']
        first_name = dict_obj['first_name']
        last_name = dict_obj['last_name']

        user = cls(email, first_name, last_name)
        user.id = id
        user.created_at = created_at
        user.updated_at = updated_at
        return user

    def validate_user(self, email, first_name, last_name):
        if not first_name or not isinstance(first_name, str) or not first_name.isalpha():
            raise TypeError("First name must be a non-empty string with only alphabetic characters")
        
        if not last_name or not isinstance(last_name, str) or not last_name.isalpha():
            raise TypeError("Last name must be a non-empty string with only alphabetic characters")
        
        if not email or not isinstance(email, str) or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise TypeError("Email must be a non-empty string in a valid email format")

        self.validate_email(email)

    @classmethod
    def validate_email(cls, email):
        if cls.__name__ in DataManager.data:
            for users in DataManager.data[cls.__name__].values():
                if users.email == email:
                    raise ConflictError("Email already taken")

        #return True

    @property
    def places(self):
        key = "place"
        places = []
        if key in DataManager.data:
            for place in DataManager.data[key].values():
                if place.host_id == self.id:
                    places.append(place)
        return places

    """@property
    def reviews(self):
        reviews = []
        for review in self.data["review"].values():
            if review.user_id == self.id:
                reviews.append(review)
        return reviews
        #return [review for review in self.data["review"].values() if review.user_id == self.id]"""
