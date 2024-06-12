#!/usr/bin/python3

from abc import ABC
import datetime
from uuid import uuid4

class Basemodel(ABC):
    def __init__(self):
        self.id = uuid4()
        self.create_at = datetime.datetime.now()
        self.update_at = datetime.datetime.now()

    def save(self):
        self.update_at = datetime.datetime.now()

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

class Place(Basemodel):
    def __init__(self, name, description, number_of_rooms, number_of_bathrooms, max_guests, price_by_nigth, latitude, longitude, City):
        super().__init__()
        self.name = name
        self.description = description
        self.number_of_rooms = number_of_rooms 
        self.number_of_bathrooms = number_of_bathrooms
        self.max_guests = max_guests
        self.price_by_night = price_by_nigth
        self.latitude = latitude
        self.longitude = longitude
        self.City = City
        self.amenities = []
        self.reviews = []
    
    def add_amenity(self, Amenity):
        self.amenities.append(Amenity)
    
    def add_review(self, Review):
        self.reviews.append(Review)


#casitapro = Place(casitgg, casitagg2, 5, 2, 999, 999, lat, long, City)

#casitapro.add_amenity("wifi")

#print(casitapro.amenities)

class Review (Basemodel):
    def __init__(self, Place, User, comment):
        super().__init__()
        self.Place = Place
        self.User = User
        self.comment = comment

"""def add_comment (self, comment):
        self.comment.append(Review)
        
        No va equis de"""


#rev1 = Review(UUID4 place, UUID4 user, "estuvo buena che")

class City(Basemodel):
    def __init__(self, name, country):
        super().__init__()
        self.name = name
        self.country = country


"""
    Creacion clase Amenity
"""
class Amenity(Basemodel):
    def __init__(self, name):
       super().__init__()
       self.name = name


pepito = User("pepito@gmail.com", "pepito", "suarez")
print(pepito.__dict__)
montevideo = City("Montevideo", )
casitapro = Place("viceCity", "cartelua", 99, 30, 999, 20000, )