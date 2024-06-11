from abc import ABC
import datetime
from uuid import uuid4

class Basemodel(ABC):
    data = {
        "user": {},
        "place": {},
        "review": {},
        "amenity": {},
        "city": {},
        "country": {}
    }

    def __init__(self):
        self.id = uuid4()
        self.created_at = datetime.datetime.now()
        self.updated_at = self.created_at

#metodo para actualizar la fecha
    def update(self, key, value):
        self.key = value
        self.update_at = datetime.datetime.now()

#metodo para guardar en data
    #@classmethod
    def save_data(self):
        print(self)
        type_name = type(self).__name__.lower()
        self.data[type_name][self.id] = self


    """def __setattr__(self, key, value):
        if hasattr(self, key):
            raise AttributeError("Invalid key.")
        else:
            super().__setattr__(key, value)"""