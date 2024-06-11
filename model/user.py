#!/usr/bin/python3


from basemodel import Basemodel
#from review import Review
import re

class User(Basemodel):
    def __init__(self, email, first_name, last_name):
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
            raise ValueError("Invalid email format.")
        
        if not first_name or not last_name:
            raise ValueError("First name and last name are required fields.")
        
        if any(user.email == email for user in self.data['user'].values()):
            raise ValueError(f"Email {email} already in use.")
        
        super().__init__()
        self.__email = email
        self.__first_name = first_name
        self.__last_name = last_name
        #llamo a la classmethod para guardar automaticamente en data al crear objeto
        self.save_data()

    @property
    def places(self):
        places = []
        for place in self.data["place"].values():
            if place.host_id == self.id:
                places.append(place)
        return places
        #return [place for place in self.data["place"].values() if place.host_id == self.id]

    def __setattr__(self, key, value):
        if hasattr(self, key):
            raise AttributeError("No se puede agregar un nuevo atributo a un usuario existente.")
        else:
            super().__setattr__(key, value)

    """@property
    def reviews(self):
        reviews = []
        for review in self.data["review"].values():
            if review.user_id == self.id:
                reviews.append(review)
        return reviews
        #return [review for review in self.data["review"].values() if review.user_id == self.id]"""

pepe = User("pepe@gm.com", "pepe", "cra")
print(pepe.__dict__)
pepe.email = "cambio@email"
print(pepe.__dict__)
