#!/usr/bin/python3
from basemodel import Basemodel
from country import Country

class City(Basemodel, Country):
    Countries = Country.preload_countries()
    
    def __init__(self, name, country_code):
        if country_code.upper() not in self.Countries:
            raise ValueError(f"Invalid country_code country_code: {country_code}. Must be an ISO 3166-1 alpha-2 country_code.")
        if not isinstance(name, str) or not name:
            raise ValueError("Name must be a non-empty string.")

        super().__init__()
        self.country_code = country_code.upper()
        self.name = name

    def __repr__(self):
       return f"City(name='{self.name}', country={self.country})"


city1 = City("Uruguay", "uy")

print(city1)