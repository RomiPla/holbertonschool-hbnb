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

class Place(Basemodel):
    def __init__(self, name, description, host_id):
        self.validate_place(name, description, host_id)
        super().__init__()
        self.name = name
        self.description = description
        self.host_id = host_id

    def to_dict(self):
        return {
            'id': str(self.id),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'name': self.name,
            'description': self.description,
            'host_id': str(self.host_id),
            '__class__': self.__class__.__name__
        }

    @classmethod
    def to_obj(cls, dict_obj):
        id = UUID(dict_obj['id'])
        created_at = datetime.fromisoformat(dict_obj['created_at'])
        updated_at = datetime.fromisoformat(dict_obj['updated_at'])
        name = dict_obj['name']
        description = dict_obj['description']
        host_id = UUID(dict_obj['host_id'])

        place = cls(name, description, host_id)
        place.id = id
        place.created_at = created_at
        place.updated_at = updated_at
        return place

    def validate_place(self, name, description, host_id):
        if not name or not isinstance(name, str):
            raise TypeError("Name must be a non-empty string")

        if not description or not isinstance(description, str):
            raise TypeError("Description must be a non-empty string")

        if not host_id or not isinstance(host_id, UUID):
            raise TypeError("Host ID must be a valid UUID")

    @classmethod
    def get_all(cls):
        all_places = DataManager.get_all_class(cls.__name__)
        if all_places is not None:
            return [places.to_dict() for places in all_places.values()]
        return []

    @classmethod
    def get(cls, id):
        return DataManager.get(id, cls.__name__)

    def add_place(self):
        DataManager.save(self)

    @classmethod
    def update(cls, entity):
        DataManager.update(entity)

    @classmethod
    def delete(cls, entity):
        DataManager.delete(entity.id, cls.__name__)
