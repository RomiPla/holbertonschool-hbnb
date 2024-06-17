from datamanager import DataManager
from user import User
from country import Country
from city import City
from amenity import Amenity
from place import Place
import json
import os

class Storage:
    """Clase que gestiona la persistencia utilizando DataManager y JSON"""

    file_path = "file.json"

    @classmethod
    def save(self):
        obj_dict = {}
        for entity_type in DataManager.data:
            obj_dict[entity_type] = {}
            if entity_type == "Country":
                for country_code in DataManager.data[entity_type]:
                    to_save = DataManager.data[entity_type][country_code].to_dict()
                    obj_dict[entity_type][to_save["code"]] = to_save
            else:
                for entity_id, entity in DataManager.data[entity_type].items():
                    #to_save = DataManager.data[entity_type][entity_id].to_dict()
                    to_save = entity.to_dict()
                    obj_dict[entity_type][to_save["id"]] = to_save

        with open(Storage.file_path, "w") as file:
            json.dump(obj_dict, file)

    @classmethod
    def load(self):
        defclass = {
            "User": User,
            "Country": Country,
            "City": City,
            "Amenity": Amenity,
            "Place": Place
        }

        if os.path.exists(Storage.file_path):
            with open(Storage.file_path, "r") as file:
                obj_dict = json.load(file)
                for entity_type in obj_dict:
                    if entity_type in defclass:
                        for entity_data in obj_dict[entity_type].values():
                            new_obj = defclass[entity_type].to_obj(entity_data)
                            DataManager.save(new_obj)