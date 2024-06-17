#!/usr/bin/python3

from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4, UUID
import re
import json
import os

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

class DataManager(IPersistenceManager):
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
    def to_obj(cls, dict_obj):
        pass

class User(Basemodel):
    def __init__(self, email, first_name, last_name):
        self.validate_user(email, first_name, last_name)
        super().__init__()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

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
        email = dict_obj['email']
        first_name = dict_obj['first_name']
        last_name = dict_obj['last_name']

        user = cls(email, first_name, last_name)
        user.id = id
        user.created_at = created_at
        user.updated_at = updated_at
        return user

    def validate_user(self, email, first_name, last_name):
        if not first_name or not isinstance(first_name, str) or not first_name.isalpha():
            raise TypeError("First name must be a non-empty string with only alphabetic characters")
        
        if not last_name or not isinstance(last_name, str) or not last_name.isalpha():
            raise TypeError("Last name must be a non-empty string with only alphabetic characters")
        
        if not email or not isinstance(email, str) or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise TypeError("Email must be a non-empty string in a valid email format")
        
        if type(self).__name__ in DataManager.data:
            for users in DataManager.data[type(self).__name__].values():
                if users.email == email:
                    raise ValueError("Email already taken")

    @classmethod
    def validate_email(self, email):
        if type(self).__name__ in DataManager.data:
            for users in DataManager.data[type(self).__name__].values():
                if users.email == email:
                    return False
        return True

    @property
    def places(self):
        key = "Place"
        places = []
        if key in DataManager.data:
            for place in DataManager.data[key].values():
                if place.host_id == self.id:
                    places.append(place)
        return places

    @classmethod
    def get_all(cls):
        all_users = DataManager.get_all_class(cls.__name__)
        if all_users is not None:
            return [users.to_dict() for users in all_users.values()]
        return []
    
    @classmethod
    def get(cls, id):
        return DataManager.get(id, cls.__name__)
        
    def add_user(self):
        DataManager.save(self)

    @classmethod
    def update(cls, entity):
        DataManager.update(entity)

    @classmethod
    def delete(cls, entity):
        DataManager.delete(entity.id, cls.__name__)

class Amenity(Basemodel):
    def __init__(self, name, description):
        self.validate_amenity(name, description)
        super().__init__()
        self.name = name
        self.description = description

    def to_dict(self):
        return {
            'id': str(self.id),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'name': self.name,
            'description': self.description,
            '__class__': self.__class__.__name__
        }
    
    @classmethod
    def to_obj(cls, dict_obj):
        id = UUID(dict_obj['id'])
        created_at = datetime.fromisoformat(dict_obj['created_at'])
        updated_at = datetime.fromisoformat(dict_obj['updated_at'])
        name = dict_obj['name']
        description = dict_obj['description']

        amenity = cls(name, description)
        amenity.id = id
        amenity.created_at = created_at
        amenity.updated_at = updated_at
        return amenity

    def validate_amenity(self, name, description):
        if not name or not isinstance(name, str):
            raise TypeError("Name must be a non-empty string")
        
        if not description or not isinstance(description, str):
            raise TypeError("Description must be a non-empty string")

    @classmethod
    def get_all(cls):
        all_amenities = DataManager.get_all_class(cls.__name__)
        if all_amenities is not None:
            return [amenities.to_dict() for amenities in all_amenities.values()]
        return []
    
    @classmethod
    def get(cls, id):
        return DataManager.get(id, cls.__name__)
        
    def add_amenity(self):
        DataManager.save(self)

    @classmethod
    def update(cls, entity):
        DataManager.update(entity)

    @classmethod
    def delete(cls, entity):
        DataManager.delete(entity.id, cls.__name__)

class Storage:
    file_path = "file.json"

    @classmethod
    def save(self):
        obj_dict = {}
        for entity_type in DataManager.data:
            obj_dict[entity_type] = {}
            for entity_id in DataManager.data[entity_type]:
                to_save = DataManager.data[entity_type][entity_id].to_dict()
                obj_dict[entity_type][to_save["id"]] = to_save

        with open(Storage.file_path, "w") as file:
            json.dump(obj_dict, file)

    @classmethod
    def load(self):
        defclass = {
            'User': User,
            'Amenity': Amenity,
        }

        if os.path.exists(Storage.file_path):
            with open(Storage.file_path, "r") as file:
                obj_dict = json.load(file)
                for entity_type in obj_dict:
                    if entity_type in defclass:
                        for entity_data in obj_dict[entity_type].values():
                            new_obj = defclass[entity_type].to_obj(entity_data)
                            DataManager.save(new_obj)


# Crear usuarios y amenidades
user1 = User("user1@example.com", "John", "Doe")
user2 = User("user2@example.com", "Jane", "Doe")
amenity1 = Amenity("WiFi", "High-speed wireless internet")
amenity2 = Amenity("Pool", "Outdoor swimming pool")

# Guardar en DataManager
user1.add_user()
user2.add_user()
amenity1.add_amenity()
amenity2.add_amenity()

# Serializar a JSON
Storage.save()

# Limpiar y cargar desde JSON
DataManager.data = {}
Storage.load()

# Verificar carga
all_users = User.get_all()
all_amenities = Amenity.get_all()

print(all_users)
print(all_amenities)
