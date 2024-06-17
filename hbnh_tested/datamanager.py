from abc import ABC, abstractmethod
from datetime import datetime

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
        
        if entity_type == "Country":
            self.data[entity_type][entity.code] = entity
        else:
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
