from model.datamanager import DataManager
from model.basemodel import Basemodel
from model.amenity import Amenity
from model.city import City
from model.country import Country
from model.user import User
from model.place import Place
from model.review import Review
import json
import os

class Storage:
    """Clase que gestiona la persistencia utilizando DataManager y JSON"""

    __file_path = "file.json"
    __objects = DataManager()

    def all(self):
        """Retorna el diccionario de objetos de DataManager"""
        return self.__objects.data

    def new(self, obj):
        """Agrega una nueva instancia en el diccionario de objetos"""
        self.__objects.save(obj)

    def save(self):
        """Serializa __objects a JSON y lo guarda en el archivo"""
        obj_dict = {}
        for entity_type, entities in self.__objects.data.items():
            for entity_id, entity in entities.items():
                obj_dict[f"{entity_type}.{entity_id}"] = entity.to_dict()

        with open(Storage.__file_path, "w") as file:
            json.dump(obj_dict, file)

    def reload(self):
        """Deserializa el JSON desde el archivo a __objects"""
        self.defclass = {
            'Basemodel': Basemodel,
            'User': User,
            'Amenity': Amenity,
            'City': City,
            'Country': Country,
            'Place': Place,
            'Review': Review,
        }

        if os.path.exists(Storage.__file_path):
            with open(Storage.__file_path, "r") as file:
                deserialized = json.load(file)
                for key, value in deserialized.items():
                    classname = value["__class__"]
                    if classname in self.defclass:
                        newobj = self.defclass[classname](**value)
                        self.__objects.save(newobj)
