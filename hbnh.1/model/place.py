#!/usr/bin/python3
from basemodel import Basemodel
from amenity import Amenity
from city import City
from country import Country
from user import User
import re

class Place(Basemodel):
    def __init__(self, host_id, name, description, number_of_rooms, \
                 number_of_bathrooms, max_guests, price_by_nigth, \
                 latitude, longitude, city_id, amenity_ids=None):
        
        if amenity_ids is None:
             amenity_ids = []

        self.validate_place(host_id, name, description, \
                            number_of_rooms, number_of_bathrooms,\
                            max_guests, price_by_nigth, latitude, \
                            longitude, city_id)
        
        super().__init__()
        self.host_id = host_id
        self.name = name
        self.description = description
        self.number_of_rooms = number_of_rooms 
        self.number_of_bathrooms = number_of_bathrooms
        self.max_guests = max_guests
        self.price_by_night = float(price_by_nigth)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.city_id = city_id
        self.amenity_ids = amenity_ids

        self.save_data()

    def validate_place(self, host_id, name, description, number_of_rooms, number_of_bathrooms,\
                 max_guests, price_by_nigth, latitude, longitude, city_id):

        if not host_id or not name or not description or not number_of_rooms\
            or not  number_of_bathrooms or not max_guests or not price_by_nigth\
                or not latitude or not longitude or not city_id:
            raise ValueError("All fields must be filled in.")

        if host_id not in self.data["user"]:
            raise ValueError(f"Host with id {host_id} does not exist.")

        if not re.match(r"^[A-Za-z0-9\s]+$", name):
            raise ValueError("Name cannot contain special characters.")

        if not isinstance(number_of_rooms, int) or number_of_rooms < 0:
            raise ValueError("Number of rooms must be a positive integer.")
        
        if not isinstance(number_of_bathrooms, int) or number_of_bathrooms < 0:
            raise ValueError("Number of bathrooms must be a positive integer.")
        
        if not isinstance(max_guests, int) or max_guests < 0:
                raise ValueError("Max guests must be a positive integer.")
        
        if not isinstance(price_by_nigth, (int, float)) or price_by_nigth < 0:
                raise ValueError("Price by nigth must be a positive number.")
        
        if not isinstance(latitude, (int, float)):
            raise ValueError("Latitude must be a number.")

        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90 degrees.")
        
        if not isinstance(longitude, (int, float)):
            raise ValueError("Longitude must be a number.")

        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180 degrees.")
        
        if city_id not in self.data["city"]:
            raise ValueError(f"City with id {city_id} does not exist.")
        
    @classmethod
    def delete(cls, place_id):
        if not cls.data["place"].get(place_id):
             raise ValueError(f"Place with id {place_id} does not exist.")
        del cls.data["place"][place_id]

    def add_amenity(self, amenity_id):
        if amenity_id not in self.amenity_ids:
            self.amenity_ids.append(amenity_id)
            self.save_data()

    def remove_amenity(self, amenity_id):
        if amenity_id in self.amenity_ids:
            self.amenity_ids.remove(amenity_id)
            self.save_data()

pepe = User("pepe@pepe.com", "pepe", "cra")
pepe2 = User("maria2@pepe.com", "maria", "lacra")


a1 = Amenity("wifi")
a2 = Amenity("pool")
a_list = [a1, a2]
#print(Basemodel.data)

Country.preload_countries()
city1 = City("Montevideo", "uy")

d = []

p1 = Place(pepe.id, "ca3ita", "fi3na", 99, 1, 999, 20000, 13, 33, city1.id, a1)

print(p1)
print(p1.__dict__)

print(Basemodel.data)

#Place.delete(p1.id)

#print(Basemodel.data)