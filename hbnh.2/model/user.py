#!/usr/bin/python3

from datamanager import DataManager
from basemodel import Basemodel
#from review import Review
import re

class User(Basemodel):
    def __init__(self, email, first_name, last_name):
        #self.validate_user(email, first_name, last_name)
        super().__init__()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        #DataManager.save(self)

    """def validate_user(self, email, first_name, last_name):
        if not email or not first_name or not last_name:
            raise ValueError("All fields must be filled in.")
        
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            raise ValueError("Invalid email format.")
        
        if type(self).__name__ in DataManager.data:
            for users in DataManager.data[type(self).__name__].values():
                if users.email == email:
                    raise ValueError("Email already taken")

        if not isinstance(first_name, str) or not isinstance(last_name, str):
            raise ValueError("First name and last name must be strings.")
        
        if not re.match(r"^[A-Za-z]+$", first_name):
            raise ValueError("First name cannot contain numbers or \
special characters.")
        
        if not re.match(r"^[A-Za-z]+$", last_name):
            raise ValueError("Last name cannot contain numbers or \
special characters.")"""

    @classmethod
    def validate_email(self, email):
        if type(self).__name__ in DataManager.data:
            for users in DataManager.data[type(self).__name__].values():
                if users.email == email:
                    return False
                    #raise ValueError("Email already taken")
        return True

    @property
    def places(self):
        key = "place"
        places = []
        if key in DataManager.data:
            for place in DataManager.data[key].values():
                if place.host_id == self.id:
                    places.append(place)
        return places
        #return [place for place in self.data["place"].values() if place.host_id == self.id]

    """def __setattr__(self, key, value):
        self.validate_user(self.email, self.first_name, self.last_name)
        self.key = value"""
    #no logro codear el _setattr_ para que verifique antes de modificar el objeto

    """@property
    def reviews(self):
        reviews = []
        for review in self.data["review"].values():
            if review.user_id == self.id:
                reviews.append(review)
        return reviews
        #return [review for review in self.data["review"].values() if review.user_id == self.id]"""
############################################################
#API METHODS
    @classmethod
    def get_all(cls):
        all_users = DataManager.get_all(cls.__name__)
        if all_users is not None:
            return [users.__dict__ for users in all_users.values()]
        return []
    
    @classmethod
    def get(cls, id):
        return DataManager.get(id, cls.__name__)
        
    #@classmethod
    def add_user(self):
        DataManager.save(self)

    @classmethod
    def update(cls, entity):
        DataManager.update(entity)

    @classmethod
    def delete(cls, entity):
        DataManager.delete(entity.id, cls.__name__)

#############################################################
#pepe = User("pepe@pepe.com", "pepe", "cra")
#print(pepe)
#pepe.email = "cambio@email"
#print(pepe.__dict__)
#print(pepe.places)
#pepe2 = User("maria2@pepe.com", "maria", "lacra")
#print(pepe2.__dict__)
#print(pepe.data)
#print(DataManager.data)
#val = User.get_user(pepe.id)
#print("val")
#print(val.__dict__)
#print(DataManager.get_all("User").__dict__)
#print(User.get_all_users())
