#!/usr/bin/python3

from basemodel import Basemodel
from uuid import UUID
from datetime import datetime
from datamanager import DataManager

class City(Basemodel):
    def __init__(self, name, country_code):
        self.validate_city(name, country_code)
        super().__init__()
        self.name = name
        self.country_code = country_code

    def to_dict(self):
        return {
            'id': str(self.id),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'name': self.name,
            'country_code': self.country_code,
            '__class__': self.__class__.__name__
        }

    @classmethod
    def to_obj(cls, dict_obj):
        id = UUID(dict_obj['id'])
        created_at = datetime.fromisoformat(dict_obj['created_at'])
        updated_at = datetime.fromisoformat(dict_obj['updated_at'])
        name = dict_obj['name']
        country_code = dict_obj['country_code']

        city = cls(name, country_code)
        city.id = id
        city.created_at = created_at
        city.updated_at = updated_at
        return city

    @classmethod
    def validate_city_name(cls, name, country_code):
        all_cities = DataManager.get_all_class("City")
        if all_cities:
            for city in all_cities.values():
                if city.name == name and city.country_code == country_code:
                    raise ValueError(f"A city with the name '{name}' already exists in the country with code '{country_code}'")

    @classmethod
    def validate_city_country_code(cls, country_code):
        if not country_code or not isinstance(country_code, str) or not country_code.isalpha() or len(country_code) != 2:
            raise TypeError("Country code must be a non-empty string with only two alphabetic characters.")
        country_code = country_code.upper()
        
        if DataManager.data.get("Country") and country_code not in DataManager.data["Country"]:
            raise ValueError("Country code does not exist in the list of preloaded countries")
        
######APIIIIIIIII########
    def validate_city(self, name, country_code):
        if not name or not isinstance(name, str):
            raise TypeError("City name must be a non-empty string with only alphabetic characters")
        
        self.validate_city_country_code(country_code)
        self.validate_city_name(name, country_code)
