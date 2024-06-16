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
                    #raise ValueError("Email already taken")
        return True

    @property
    def places(self):
        key = "place"
        places = []
        if key in DataManager.data:
            for place in DataManager.data[key].values():
                if place.host_id == self.id:
                    places.append(place)
        return places
        #return [place for place in self.data["place"].values() if place.host_id == self.id]

    """def __setattr__(self, key, value):
        self.validate_user(self.email, self.first_name, self.last_name)
        self.key = value"""
    #no logro codear el _setattr_ para que verifique antes de modificar el objeto

    """@property
    def reviews(self):
        reviews = []
        for review in self.data["review"].values():
            if review.user_id == self.id:
                reviews.append(review)
        return reviews
        #return [review for review in self.data["review"].values() if review.user_id == self.id]"""
############################################################
#API METHODS
    @classmethod
    def get_all(cls):
        all_users = DataManager.get_all_class(cls.__name__)
        if all_users is not None:
            return [users.to_dict() for users in all_users.values()]
        return []
    
    @classmethod
    def get(cls, id):
        return DataManager.get(id, cls.__name__)
        
    #@classmethod
    def add_user(self):
        DataManager.save(self)

    @classmethod
    def update(cls, entity):
        DataManager.update(entity)

    @classmethod
    def delete(cls, entity):
        DataManager.delete(entity.id, cls.__name__)

class Storage:
    """Clase que gestiona la persistencia utilizando DataManager y JSON"""

    file_path = "file.json"
    #objects = DataManager()

    #def all(self):
    #    """Retorna el diccionario de objetos de DataManager"""
    #    return self.objects.data

    #def new(self, obj):
     #   """Agrega una nueva instancia en el diccionario de objetos"""
     #   self.objects.save(obj)

    @classmethod
    def save(self):
        """Serializa todo DataManager a JSON y guarda en el archivo"""
        obj_dict = {}
        for entity_type in DataManager.data:
            obj_dict[entity_type] = {}
            for entity_id in DataManager.data[entity_type]:
                # creo una instancia del objeto en modo #to_dict#
                # para asegurarme de tener su id en str y sus
                # fechas en isoformat
                to_save = DataManager.data[entity_type][entity_id].to_dict()
                #print(to_save)
                obj_dict[entity_type][to_save["id"]] = to_save

        with open(Storage.file_path, "w") as file:
            json.dump(obj_dict, file)

    @classmethod
    def load(self):
        """Deserializa el JSON desde el archivo y carga en DataManager"""
        defclass = {
            'User': User,
        }

        if os.path.exists(Storage.file_path):
            with open(Storage.file_path, "r") as file:
                obj_dict = json.load(file)
                for entity_type in obj_dict:
                    if entity_type in defclass:
                        for entity_data in obj_dict[entity_type].values():
                            new_obj = defclass[entity_type].to_obj(entity_data)
                            DataManager.save(new_obj)

        
        
        """self.defclass = {
            'Basemodel': Basemodel,
            'User': User,
            #'Amenity': Amenity,
           # 'City': City,
            #'Country': Country,
           # 'Place': Place,
           # 'Review': Review,
        }

        if os.path.exists(Storage.__file_path):
            with open(Storage.__file_path, "r") as file:
                deserialized = json.load(file)
                for key, value in deserialized.items():
                    classname = value["__class__"]
                    if classname in self.defclass:
                        newobj = self.defclass[classname](**value)
                        self.__objects.save(newobj)"""


#############################################################


"""pepe = User("pepe@pepe.com", "pepe", "cra")
print("User =", pepe.first_name, "update_at =", pepe.updated_at)
print(DataManager.data)
DataManager.save(pepe)
print(DataManager.data)

pepe.first_name = "ramon"
print("User =", pepe.first_name, "update_at =", pepe.updated_at)

DataManager.update(pepe)

user_from_data = DataManager.get(pepe.id, "User")

print("User =", user_from_data.first_name, "update_at =", user_from_data.updated_at)"""

#time.sleep(2)
#DataManager.update(pepe)
#print(DataManager.get(pepe.id,))

#pepe.email = "cambio@email"
#print(pepe.__dict__)
#print(pepe.places)
#pepe2 = User("maria2@pepe.com", "maria", "lacra")
#print(pepe2.__dict__)
#print(pepe.data)
#val = User.get_user(pepe.id)
#print("val")
#print(val.__dict__)
#print(DataManager.get_all("User").__dict__)
#print(User.get_all_users())
