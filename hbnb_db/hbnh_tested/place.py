from basemodel import Basemodel, datetime
from uuid import UUID
from datamanager import DataManager
import re

class Place(Basemodel):
    def __init__(self, host_id, name, description, number_of_rooms, \
                 number_of_bathrooms, max_guests, price_per_night, \
                 latitude, longitude, city_id, amenity_ids=None):
     
        if amenity_ids is None:
                    amenity_ids = []

        self.validate_place(host_id, name, description, \
                            number_of_rooms, number_of_bathrooms,\
                            max_guests, price_per_night, latitude, \
                            longitude, city_id)
        super().__init__()
        self.host_id = host_id
        self.name = name
        self.description = description
        self.number_of_rooms = number_of_rooms 
        self.number_of_bathrooms = number_of_bathrooms
        self.max_guests = max_guests
        self.price_by_night = float(price_per_night)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.city_id = city_id
        self.amenity_ids = amenity_ids

    def to_dict(self):
        return {
            'id': str(self.id),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'host_id': str(self.host_id),
            'name': self.name,
            'description': self.description,
            'number_of_rooms': self.number_of_rooms,
            'number_of_bathrooms': self.number_of_bathrooms,
            'max_guests': self.max_guests,
            'price_by_night': self.price_by_night,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'city_id': str(self.city_id),
            'amenity_ids': [str(am_id) for am_id in self.amenity_ids],
            '__class__': self.__class__.__name__
        }

    @classmethod
    def to_obj(cls, dict_obj):
        id = UUID(dict_obj['id'])
        created_at = datetime.fromisoformat(dict_obj['created_at'])
        updated_at = datetime.fromisoformat(dict_obj['updated_at'])
        host_id = UUID(dict_obj['host_id'])
        name = dict_obj['name']
        description = dict_obj['description']
        number_of_rooms = dict_obj['number_of_rooms']
        number_of_bathrooms = dict_obj['number_of_bathrooms']
        max_guests = dict_obj['max_guests']
        price_by_night = dict_obj['price_by_night']
        latitude = dict_obj['latitude']
        longitude = dict_obj['longitude']
        city_id = UUID(dict_obj['city_id'])
        amenity_ids = [UUID(am_id) for am_id in dict_obj.get('amenity_ids')]

        place = cls(host_id, name, description, number_of_rooms, 
                    number_of_bathrooms, max_guests, price_by_night, 
                    latitude, longitude, city_id, amenity_ids)
        place.id = id
        place.created_at = created_at
        place.updated_at = updated_at
        return place

    @classmethod
    def validate_place_host_id(cls, host_id):
       if host_id not in DataManager.data["User"]:
            raise ValueError(f"Host with id {host_id} does not exist.")

    @classmethod
    def validate_place_city_id(cls, city_id):
        if city_id not in DataManager.data["City"]:
            raise ValueError(f"City with id {city_id} does not exist.")

    @classmethod
    def validate_place_data(cls, host_id, city_id):
        cls.validate_place_host_id(host_id)
        cls.validate_place_city_id(city_id)


    def validate_place(self, host_id, name, description, number_of_rooms, number_of_bathrooms,\
                 max_guests, price_per_night, latitude, longitude, city_id):

        if not host_id or not name or not description or not number_of_rooms\
            or not  number_of_bathrooms or not max_guests or not price_per_night\
                or not latitude or not longitude or not city_id:
            raise TypeError("All fields must be filled in.")
        
        if not re.match(r"^[A-Za-z0-9\s]+$", name):
            raise TypeError("Name cannot contain special characters.")

        if not isinstance(number_of_rooms, int) or number_of_rooms < 0:
            raise ValueError("Number of rooms must be a positive integer.")

        if not isinstance(number_of_bathrooms, int) or number_of_bathrooms < 0:
            raise ValueError("Number of bathrooms must be a positive integer.")

        if not isinstance(max_guests, int) or max_guests < 0:
                raise ValueError("Max guests must be a positive integer.")

        if not isinstance(price_per_night, (int, float)) or price_per_night < 0:
                raise ValueError("Price by nigth must be a positive number.")

        if not isinstance(latitude, (int, float)):
            raise ValueError("Latitude must be a number.")

        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90 degrees.")

        if not isinstance(longitude, (int, float)):
            raise ValueError("Longitude must be a number.")

        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180 degrees.")

        self.validate_place_data(host_id, city_id)