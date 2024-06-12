#!/usr/bin/python3
from basemodel import Basemodel
from datamanager import DataManager
from country import Country
import re

class City(Basemodel):
    #Countries = Country.preload_countries()
    
    def __init__(self, name, country_code):
        self.validate_city(name, country_code)
        super().__init__()
        self.country_code = country_code.upper()
        self.name = name
        DataManager.save(self)


    def validate_city(self, name, country_code):
        if not name or not country_code:
            raise ValueError("All fields must be filled in.")

        if not re.match(r"^[A-Za-z]+$", name):
            raise ValueError("Name cannot contain numbers or \
special characters.")
        
        if not re.match(r"^[A-Za-z]+$", country_code):
            raise ValueError("Country code cannot contain numbers or \
special characters.")
        
        if not any(DataManager.data["country"]):
            raise ValueError(f"There are no pre-loaded countries.")

        if country_code.upper() not in DataManager.data["country"]:
            raise ValueError(f"Invalid country_code: {country_code}.")
        
    """def __repr__(self):
       return f"City(name='{self.name}', country={self.country_code})"""

"""try:
    city1 = City("Uruguay", "uy")
    print(city1)
except Exception as e:
    print(e)
print(Basemodel.data)

Country.preload_countries()
city1 = City("Montevideo", "uy")
print(city1)
print(Basemodel.data)"""