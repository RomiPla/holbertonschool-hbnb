import IPersistenceManager
import datetime

class DataManager(IPersistenceManager):
    def __init__(self):
        self.data = {}

    def save(self, entity):
        entity_type = type(entity).__name__
        if entity_type not in self.data:
            self.data[entity_type] = {}
        self.data[entity_type][entity.id] = entity

    def get(self, entity_id, entity_type):
        if entity_type in self.data:
            return self.data[entity_type].get(entity_id)
        return None

    def update(self, entity):
        entity_type = type(entity).__name__
        if entity_type in self.data:
            entity_id = entity.id
            if entity_id in self.data[entity_type]:
                entity.updated_at = datetime.datetime.now()
                self.data[entity_type][entity_id] = entity

    def delete(self, entity_id, entity_type):
        if entity_type in self.data:
            if entity_id in self.data[entity_type]:
                del self.data[entity_type][entity_id]