"""
    Creacion clase Amenity
"""
from basemodel import Basemodel
import re

class Amenity(Basemodel):
    def __init__(self, name):
       if not re.match(r"^[A-Za-z]+$", name):
            raise ValueError("Name cannot contain numbers or \
special characters.")

       super().__init__()
       self.name = name
       self.save_data()
    @classmethod
    def delete(cls, place_id):
        if not cls.data["amenities"].get(place_id):
             raise ValueError(f"Place with id {place_id} does not exist.")
        del cls.data["amanities"][place_id]
