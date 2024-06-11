"""
    Creacion clase Amenity
"""
from basemodel import Basemodel

class Amenity(Basemodel):
    def __init__(self, name):
       super().__init__()
       self.name = name
