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


class Review(Basemodel):
    def __init__(self, user_id, place_id, rating, text):
        self.validate_review(user_id, place_id, rating, text)
        super().__init__()
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating
        self.text = text

    def to_dict(self):
        return {
            'id': str(self.id),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'user_id': str(self.user_id),
            'place_id': str(self.place_id),
            'rating': self.rating,
            'text': self.text,
            '__class__': self.__class__.__name__
        }
    
    @classmethod
    def to_obj(cls, dict_obj):
        id = UUID(dict_obj['id'])
        created_at = datetime.fromisoformat(dict_obj['created_at'])
        updated_at = datetime.fromisoformat(dict_obj['updated_at'])
        user_id = UUID(dict_obj['user_id'])
        place_id = UUID(dict_obj['place_id'])
        rating = dict_obj['rating']
        text = dict_obj['text']

        review = cls(user_id, place_id, rating, text)
        review.id = id
        review.created_at = created_at
        review.updated_at = updated_at
        return review

    def validate_review(self, user_id, place_id, rating, text):
        if not isinstance(user_id, UUID):
            raise TypeError("User ID must be a valid UUID")
        
        if not isinstance(place_id, UUID):
            raise TypeError("Place ID must be a valid UUID")
        
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        
        if not isinstance(text, str) or len(text) > 1024:
            raise ValueError("Review text must be a string of up to 1024 characters")
        
        # Se puede agregar lógica de validación adicional según sea necesario

    @property
    def user(self):
        return DataManager.get(self.user_id, "User")

    @property
    def place(self):
        return DataManager.get(self.place_id, "Place")
