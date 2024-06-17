from basemodel import Basemodel
from datetime import datetime
from uuid import UUID

class Amenity(Basemodel):
    def __init__(self, name, description):
        self.validate_amenity(name, description)
        super().__init__()
        self.name = name
        self.description = description

    def validate_amenity(self, name, description):
        if not name or not isinstance(name, str):
            raise TypeError("Name must be a non-empty string")
        
        if not description or not isinstance(description, str):
            raise TypeError("Description must be a non-empty string")

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
