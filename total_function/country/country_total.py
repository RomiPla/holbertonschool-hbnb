#!/usr/bin/python3

#from datamanager import DataManager
#from basemodel import Basemodel
#from review import Review
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

class Country(Basemodel):
    def __init__(self, name, code):
        self.validate_country(name, code)
        super().__init__()
        self.name = name
        self.code = code
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'name': self.name,
            'code': self.code,
            '__class__': self.__class__.__name__
        }

class User(Basemodel):
    def __init__(self, email, first_name, last_name):
        self.validate_user(email, first_name, last_name)
        super().__init__()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        #DataManager.save(self)

    def to_dict(self):
        return {
            'id': str(self.id),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            '__class__': self.__class__.__name__
        }
    
    
    @classmethod
    def to_obj(cls, dict_obj):
        id = UUID(dict_obj['id'])
        created_at = datetime.fromisoformat(dict_obj['created_at'])
        updated_at = datetime.fromisoformat(dict_obj['updated_at'])
        name = dict_obj['name']
        code = dict_obj['code']

        country = cls(name, code)
        country.id = id
        country.created_at = created_at
        country.updated_at = updated_at
        return country

    def validate_country(self, name, code):
        if not name or not isinstance(name, str):
            raise TypeError("Country name must be a non-empty string")
        
        if not code or not isinstance(code, str):
            raise TypeError("Country code must be a non-empty string")

class DataManager(IPersistenceManager):
    data = {}

    @classmethod
    def save(cls, entity):
        entity_type = type(entity).__name__
        if entity_type not in cls.data:
            cls.data[entity_type] = {}
        cls.data[entity_type][entity.id] = entity

    @classmethod
    def get(cls, entity_id, entity_type):
        if entity_type in cls.data:
            return cls.data[entity_type].get(entity_id)
        return None

    @classmethod
    def get_all_class(cls, entity_type):
        if entity_type in cls.data:
            return cls.data[entity_type]
        return None

    @classmethod
    def update(cls, entity):
        to_update = cls.get(entity.id, type(entity).__name__)
        if to_update is not None:
            to_update.updated_at = datetime.now()
            cls.save(to_update)

    @classmethod
    def delete(cls, entity_id, entity_type):
        if entity_type in cls.data:
            if entity_id in cls.data[entity_type]:
                del cls.data[entity_type][entity_id]

class Storage:
    file_path = "file.json"

    @classmethod
    def save(cls):
        obj_dict = {}
        for entity_type in DataManager.data:
            obj_dict[entity_type] = {}
            for entity_id in DataManager.data[entity_type]:
                to_save = DataManager.data[entity_type][entity_id].to_dict()
                obj_dict[entity_type][to_save["id"]] = to_save

        with open(cls.file_path, "w") as file:
            json.dump(obj_dict, file)

    @classmethod
    def load(cls):
        defclass = {
            'User': User,
            'Country': Country,
        }

        if os.path.exists(cls.file_path):
            with open(cls.file_path, "r") as file:
                obj_dict = json.load(file)
                for entity_type in obj_dict:
                    if entity_type in defclass:
                        for entity_data in obj_dict[entity_type].values():
                            new_obj = defclass[entity_type].to_obj(entity_data)
                            DataManager.save(new_obj)
