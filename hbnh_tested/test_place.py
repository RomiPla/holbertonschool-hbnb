#!/usr/bin/python3
import unittest
from place import Place
from user import User
from city import City
from datamanager import DataManager
from uuid import uuid4
from storage import Storage
from amenity import Amenity
import os
from api import app

print("PLACE")

class TestPlace_Logical(unittest.TestCase):

    def setUp(self):
        DataManager.data = {}
        user = User("pepe@g.com", "Pedrito", "pe")
        User.add(user)
        city = City("bondiola", "AR")
        City.add(city)
        self.host_id = user.id
        self.city_id = city.id
        self.name = "Test Place"
        self.description = "A place for testing"
        self.number_of_rooms = 3
        self.number_of_bathrooms = 2
        self.max_guests = 4
        self.price_by_night = 100.0
        self.latitude = 45.0
        self.longitude = 90.0
        self.amenity_ids = [uuid4(), uuid4()]

    def test_place_name(self):
        place = Place(self.host_id, self.name, self.description, self.number_of_rooms,
                      self.number_of_bathrooms, self.max_guests, self.price_by_night,
                      self.latitude, self.longitude, self.city_id)
        self.assertEqual(place.name, self.name)

        with self.assertRaises(TypeError):
            Place(self.host_id, 'InvalidName@', self.description, self.number_of_rooms,
                  self.number_of_bathrooms, self.max_guests, self.price_by_night,
                  self.latitude, self.longitude, self.city_id)

        with self.assertRaises(TypeError):
            Place(self.host_id, '', self.description, self.number_of_rooms,
                  self.number_of_bathrooms, self.max_guests, self.price_by_night,
                  self.latitude, self.longitude, self.city_id)

    def test_place_latitude(self):
        with self.assertRaises(ValueError):
            Place(self.host_id, self.name, self.description, self.number_of_rooms,
                  self.number_of_bathrooms, self.max_guests, self.price_by_night,
                  100, self.longitude, self.city_id)

    def test_place_longitude(self):
        with self.assertRaises(ValueError):
            Place(self.host_id, self.name, self.description, self.number_of_rooms,
                  self.number_of_bathrooms, self.max_guests, self.price_by_night,
                  self.latitude, 200, self.city_id)
            
class TestPlace_DataManager(unittest.TestCase):

    def setUp(self):
        DataManager.data = {}
        user = User("pepe@g.com", "Pedrito", "pe")
        User.add(user)
        city = City("bondiola", "AR")
        City.add(city)
        self.host_id = user.id
        self.city_id = city.id
        self.name = "Test Place"
        self.description = "A place for testing"
        self.number_of_rooms = 3
        self.number_of_bathrooms = 2
        self.max_guests = 4
        self.price_by_night = 100.0
        self.latitude = 45.0
        self.longitude = 90.0
        self.amenity_ids = [uuid4(), uuid4()]

    def test_save_place(self):
        place = Place(self.host_id, self.name, self.description, self.number_of_rooms,
                      self.number_of_bathrooms, self.max_guests, self.price_by_night,
                      self.latitude, self.longitude, self.city_id, self.amenity_ids)
        DataManager.save(place)
        retrieved_place = DataManager.get(place.id, 'Place')
        self.assertEqual(place, retrieved_place)

    def test_update_place(self):
        place = Place(self.host_id, self.name, self.description, self.number_of_rooms,
                      self.number_of_bathrooms, self.max_guests, self.price_by_night,
                      self.latitude, self.longitude, self.city_id, self.amenity_ids)
        DataManager.save(place)
        old_updated_at = place.updated_at
        place.name = 'New Test Place'
        DataManager.update(place)
        updated_place = DataManager.get(place.id, 'Place')
        self.assertNotEqual(old_updated_at, updated_place.updated_at)
        self.assertEqual(updated_place.name, 'New Test Place')

    def test_delete_place(self):
        place = Place(self.host_id, self.name, self.description, self.number_of_rooms,
                      self.number_of_bathrooms, self.max_guests, self.price_by_night,
                      self.latitude, self.longitude, self.city_id, self.amenity_ids)
        DataManager.save(place)
        DataManager.delete(place.id, 'Place')
        retrieved_place = DataManager.get(place.id, 'Place')
        self.assertIsNone(retrieved_place)

    def test_get_all_places(self):
        place1 = Place(self.host_id, self.name, self.description, self.number_of_rooms,
                       self.number_of_bathrooms, self.max_guests, self.price_by_night,
                       self.latitude, self.longitude, self.city_id, self.amenity_ids)
        place2 = Place(self.host_id, 'Another Test Place', 'Another description', 2, 1, 2, 75.0, 50.0, 100.0, self.city_id, self.amenity_ids)
        places = {place1.id: place1, place2.id: place2}
        DataManager.save(place1)
        DataManager.save(place2)
        all_places_saved = DataManager.get_all_class("Place")
        self.assertEqual(all_places_saved, places)

class TestPlace_Storage(unittest.TestCase):
    def setUp(self):
        DataManager.data = {}

    def cleaner(self):
        if os.path.exists(Storage.file_path):
            os.remove(Storage.file_path)

    def test_storage_serialization(self):
        user = User("pepe@g.com", "Pedrito", "pe")
        User.add(user)
        city = City("bondiola", "AR")
        City.add(city)
        pool = Amenity("Pool", "cool")
        gym = Amenity("Gym", "Yuka")
        Amenity.add(pool)
        Amenity.add(gym)
        place = Place(user.id, "Test Place", "A place for testing", 3, 2, 4, 100.0, 45.0, 90.0, city.id, [pool.id, gym.id])
        DataManager.save(place)
        Storage.save()
        self.assertTrue(os.path.exists(Storage.file_path))

    def test_storage_deserialization(self):
        user = User("pepe@g.com", "Pedrito", "pe")
        User.add(user)
        city = City("bondiola", "AR")
        City.add(city)
        place = Place(user.id, "Test Place", "A place for testing", 3, 2, 4, 100.0, 45.0, 90.0, city.id, [uuid4(), uuid4()])
        DataManager.save(place)
        Storage.save()
        self.setUp()
        Storage.load()
        load_place = DataManager.get(place.id, 'Place')
        self.assertEqual(place.name, load_place.name)
        self.assertEqual(place.description, load_place.description)
        self.assertEqual(place.number_of_rooms, load_place.number_of_rooms)
        self.assertEqual(place.number_of_bathrooms, load_place.number_of_bathrooms)


class TestPlace_API(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        DataManager.data = {}

    def cleaner(self):
        if os.path.exists(Storage.file_path):
            os.remove(Storage.file_path)

    def test_get_all_places(self):
        user = User("pepe@g.com", "Pedrito", "pe")
        User.add(user)
        city = City("bondiola", "AR")
        City.add(city)

        user2 = User("pepe2@g.com", "Pedrito", "pe")
        User.add(user2)
        city2 = City("bondiola", "UY")
        City.add(city2)

        place1 = Place(user.id, "Place 1", "Description 1", 2, 1, 3, 80.0, 30.0, 50.0, city.id, [])
        place2 = Place(user2.id, "Place 2", "Description 2", 3, 2, 4, 120.0, 35.0, 55.0, city2.id, [])
        Place.add(place1)
        Place.add(place2)

        response = self.app.get('/places')
        self.assertEqual(response.status_code, 200)

        places = response.json
        self.assertEqual(len(places), 2)

    def test_get_place(self):
        user = User("pepe@g.com", "Pedrito", "pe")
        User.add(user)
        city = City("bondiola", "AR")
        City.add(city)
        place1 = Place(user.id, "Place 1", "Description 1", 2, 1, 3, 80.0, 30.0, 50.0, city.id, [])
        Place.add(place1)

        response = self.app.get(f'/places/{place1.id}')
        self.assertEqual(response.status_code, 200)

        retrieved_place = response.json
        self.assertEqual(retrieved_place["name"], "Place 1")

    def test_add_place(self):
        user = User("pepe@g.com", "Pedrito", "pe")
        User.add(user)
        city = City("bondiola", "AR")
        City.add(city)

        place_data = {
            "host_id": str(user.id),
            "name": "Test Place",
            "description": "A place for testing",
            "number_of_rooms": 3,
            "number_of_bathrooms": 2,
            "max_guests": 4,
            "price_per_night": 100.0,
            "latitude": 45.0,
            "longitude": 90.0,
            "city_id": str(city.id),
            "amenity_ids": []
        }
        response = self.app.post('/places', json=place_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.get_json())

    def test_update_place(self):
        user = User("pepe@g.com", "Pedrito", "pe")
        User.add(user)
        city = City("bondiola", "AR")
        City.add(city)
        place1 = Place(user.id, "Place 1", "Description 1", 2, 1, 3, 80.0, 30.0, 50.0, city.id, [])
        Place.add(place1)

        updated_data = {
            "name": "Updated Place",
            "description": "Updated description",
            "price_per_night": 120.0
        }

        response = self.app.put(f'/places/{place1.id}', json=updated_data)
        self.assertEqual(response.status_code, 200)

        updated_place = DataManager.get(place1.id, "Place")
        self.assertEqual(updated_place.name, "Updated Place")
        self.assertEqual(updated_place.description, "Updated description")
        self.assertEqual(updated_place.price_per_night, 120.0)

    def test_delete_place(self):
        user = User("pepe@g.com", "Pedrito", "pe")
        User.add(user)
        city = City("bondiola", "AR")
        City.add(city)
        place1 = Place(user.id, "Place 1", "Description 1", 2, 1, 3, 80.0, 30.0, 50.0, city.id, [])
        Place.add(place1)

        response = self.app.delete(f'/places/{place1.id}')
        self.assertEqual(response.status_code, 204)

        self.assertNotIn(place1.id, DataManager.data["Place"])
    
if __name__ == '__main__':
    unittest.main()