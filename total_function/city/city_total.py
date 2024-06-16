#!/usr/bin/python3

from datamanager import DataManager
from basemodel import Basemodel
from abc import ABC
from datetime import datetime
from uuid import uuid4
import re
from abc import ABC, abstractmethod
import json
import os
from uuid import UUID

class IPersistenceManager(ABC):
       @abstractmethod
       def save(self, entity):
           pass

       @abstractmethod
       def get(self, entity_id, entity_type):
           pass

       @abstractmethod
       def update(self, entity):
           pass

       @abstractmethod
       def delete(self, entity_id, entity_type):
           pass

#from IPersistenceManager import IPersistenceManager
#import datetime

class DataManager(IPersistenceManager):
    #def __init__(self):
    #    self.data = {}

    data = {}

    @classmethod
    def save(self, entity):
        entity_type = type(entity).__name__
        if entity_type not in self.data:
            self.data[entity_type] = {}
        self.data[entity_type][entity.id] = entity

    @classmethod
    def get(self, entity_id, entity_type):
        if entity_type in self.data:
            return self.data[entity_type].get(entity_id)
        return None

    @classmethod
    def get_all_class(self, entity_type):
        if entity_type in self.data:
            return self.data[entity_type]
        return None

    @classmethod
    def update(self, entity):
        to_update = DataManager.get(entity.id, type(entity).__name__)
        if to_update is not None:
            to_update.updated_at = datetime.now()
            DataManager.save(to_update)
        """entity_type = type(entity).__name__
        if entity_type in self.data:
            entity_id = entity.id
            if entity_id in self.data[entity_type]:
                entity.updated_at = datetime.now()
                #self.data[entity_type][entity_id] = entity"""

    @classmethod
    def delete(self, entity_id, entity_type):
        if entity_type in self.data:
            if entity_id in self.data[entity_type]:
                del self.data[entity_type][entity_id]

class Basemodel(ABC):
    def __init__(self):
        self.id = uuid4()
        self.created_at = datetime.now()
        self.updated_at = self.created_at
    
    @abstractmethod
    def to_dict(self):
        pass

    @classmethod
    @abstractmethod
    def to_obj(self):
        pass

class City(Basemodel):
    def __init__(self, name, country):
        self.validate_city(name, country)
        super().__init__()
        self.name = name
        self.country = country

    def to_dict(self):
        return {
            'id': str(self.id),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'name': self.name,
            'country': self.country,
            '__class__': self.__class__.__name__
        }

    @classmethod
    def to_obj(cls, dict_obj):
        id = UUID(dict_obj['id'])
        created_at = datetime.fromisoformat(dict_obj['created_at'])
        updated_at = datetime.fromisoformat(dict_obj['updated_at'])
        name = dict_obj['name']
        country = dict_obj['country']

        city = cls(name, country)
        city.id = id
        city.created_at = created_at
        city.updated_at = updated_at
        return city

    def validate_city(self, name, country):
        if not name or not isinstance(name, str):
            raise TypeError("City name must be a non-empty string")

        if not country or not isinstance(country, str):
            raise TypeError("Country name must be a non-empty string")

    @classmethod
    def get_all(cls):
        all_cities = DataManager.get_all_class(cls.__name__)
        if all_cities is not None:
            return [cities.to_dict() for cities in all_cities.values()]
        return []

    @classmethod
    def get(cls, id):
        return DataManager.get(id, cls.__name__)

    def add_city(self):
        DataManager.save(self)

    @classmethod
    def update(cls, entity):
        DataManager.update(entity)

    @classmethod
    def delete(cls, entity):
        DataManager.delete(entity.id, cls.__name__)
