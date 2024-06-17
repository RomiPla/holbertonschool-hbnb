from abc import ABC, abstractmethod
from uuid import uuid4
from datetime import datetime
from datamanager import DataManager

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

############################################################
#                   API METHODS                            #
############################################################

    @classmethod
    def get_all(cls):
        all_obj = DataManager.get_all_class(cls.__name__)
        if all_obj is not None:
            return [obj.to_dict() for obj in all_obj.values()]
        return []
    
    @classmethod
    def get(cls, id):
        return DataManager.get(id, cls.__name__)
        
    def add(self):
        DataManager.save(self)

    @classmethod
    def update(cls, entity):
        DataManager.update(entity)

    @classmethod
    def delete(cls, entity):
        DataManager.delete(entity.id, cls.__name__)