#!/usr/bin/python3
from basemodel import Basemodel, DataManager
import pycountry

class Country(Basemodel):
    def __init__(self, name, code):
        self._name = name
        self._code = code

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code
    
    def to_dict(self):
        return {
            'name': self.name,
            'code': self.code,
        }
    
    @classmethod
    def to_obj(cls, dict_obj):
        name = dict_obj['name']
        code = dict_obj['code']

        country = cls(name, code)
        return country
    
    @classmethod
    def load_countries(cls):
        DataManager.data["Country"] = {}
        for country in pycountry.countries:
            country_obj = cls(country.name, country.alpha_2)
            DataManager.data["Country"][country.alpha_2] = country_obj

    @classmethod
    def cities(cls, code):
        cities = []
        for city_obj in DataManager.data["City"].values():
            if city_obj and city_obj.country_code == code:
                cities.append(city_obj.to_dict())
        return cities

#print(DataManager.data)
#print(Country.get_all())
#pais = Country("cheche", "CH")
#print(pais)
#print(pais.to_dict())
#Country.load_countries()
#print(Country.get_all())

#city