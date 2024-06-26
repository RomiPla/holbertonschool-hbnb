"""
    Creacion clase Amenity
"""
from basemodel import Basemodel
from datamanager import DataManager
import re

class Amenity(Basemodel):
    def __init__(self, name):
       if not re.match(r"^[A-Za-z]+$", name):
            raise ValueError("Name cannot contain numbers or \
special characters.")

       super().__init__()
       self.name = name
       DataManager.save(self)
