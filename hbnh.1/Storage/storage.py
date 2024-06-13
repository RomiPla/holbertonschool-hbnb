#!/usr/bin/python3

from model.basemodel import Basemodel
from model.amenity import Amenity
from model.city import City
from model.country import Country
from model.user import User
from model.place import Place
from model.review import Review
import json


class FileStorage():
    """ Se va a serializar y deserealizar utilizando a JSON"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """all() metodo

        Return:
            Retorna un diccionario de objetos
        """
        return self.__objects

    def new(self, obj):
        """new() metodo
        key: Llave formada por el nombre de la clase del objeto y su ID (<ClassName>.id).
        FileStorage.__objects[key] = obj: Guarda la instancia en el diccionario __objects
        con la llave generada.
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """save() method
        Convierte las instancias del diccionario __objects a diccionarios utilizando
        el método to_dict() de cada objeto.
        json.dump(obj_dict, file): Serializa el diccionario de objetos
        y lo guarda en el archivo JSON.
        """
        with open(FileStorage.__file_path, "w") as file:
            obj_dict = {}
            for key, value in FileStorage.__objects.items():
                obj_dict[key] = value.to_dict()
            json.dump(obj_dict, file)

    def reload(self):
        """reload() method

        Deserealiza el Json en un diccionario
        """

        
        self.defclass = {
            'basemodel': Basemodel,
            'user': User,
            'Amenity': Amenity,
            'City': City,
            'Place': Place,
            'Review': Review,
        }

        try:
            with open(FileStorage.__file_path, "r") as file:
                deserialized = json.load(file)
                for key, value in deserialized.items():
                    classname = value["__class__"]
                    if classname in self.defclass:
                        newobj = self.defclass[classname](**value)
                        key = "{}.{}".format(classname, newobj.id)
                        FileStorage.__objects[key] = newobj
        except FileNotFoundError:
            pass