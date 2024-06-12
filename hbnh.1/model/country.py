#!/usr/bin/python3
import pycountry
from basemodel import Basemodel

class Country:
#    _countries = {}

    def __init__(self, code, name):
        self._code = code
        self._name = name

    """@property
    def code(self):
        return self._code

    @property
    def name(self):
        return self._name"""

    @classmethod
    def preload_countries(cls):
        Basemodel.data["country"] = {country.alpha_2: country.name for country in pycountry.countries}

    """@classmethod
    def get_country_name(cls, code):
        code = code.upper()
        if code in cls._countries:
            return cls._countries[code]
        else:
            raise ValueError(f"Invalid country code: {code}. Must be an ISO 3166-1 alpha-2 code.")
        
    @classmethod
    def get_country_code(name):
        name = name.lower()
        for country in pycountry.countries:
            if name == country.name.lower():
                return country.alpha_2
        return "Country not found"

    def __repr__(self):
        return f"Country(code='{self.code}', name='{self.name}')"
    """
"""contries = Country
C_dic = contries.preload_countries()
print(C_dic)"""

"""print(Basemodel.data)
Country.preload_countries()
print(Basemodel.data)"""