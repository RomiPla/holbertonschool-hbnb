#!/usr/bin/python3
import unittest
import datetime
import json
import os
from uuid import uuid4, UUID
from place_total import Place
from place_total import DataManager, IPersistenceManager, Storage
from api import app

class TestPlace_Logical(unittest.TestCase):

    def test_place_name(self):
        place = Place('Beach House', 'A nice house by the beach', uuid4())
        self.assertEqual(place.name, 'Beach House')

        with self.assertRaises(TypeError, msg="Name must be a non-empty string"):
            place = Place('', 'A nice house by the beach', uuid4())
        with self.assertRaises(TypeError, msg="Name must be a non-empty string"):
            place = Place(None, 'A nice house by the beach', uuid4())

    def test_place_description(self):
        place = Place('Beach House', 'A nice house by the beach', uuid4())
        self.assertEqual(place.description, 'A nice house by the beach')

        with self.assertRaises(TypeError, msg="Description must be a non-empty string"):
            place = Place('Beach House', '', uuid4())
        with self.assertRaises(TypeError, msg="Description must be a non-empty string"):
            place = Place('Beach House', None, uuid4())

    def test_place_host_id(self):
        host_id = uuid4()
        place = Place('Beach House', 'A nice house by the beach', host_id)
        self.assertEqual(place.host_id, host_id)

        with self.assertRaises(TypeError, msg="Host ID must be a valid UUID"):
            place = Place('Beach House', 'A nice house by the beach', 'invalid-uuid')
        with self.assertRaises(TypeError, msg="Host ID must be a valid UUID"):
            place = Place('Beach House', 'A nice house by the beach', '')

class TestPlace_DataManager(unittest.TestCase):

    def setUp(self):
        DataManager.data = {}  # Reset DataManager data for each test

    def test_save_place(self):
        place = Place('Beach House', 'A nice house by the beach', uuid4())
        DataManager.save(place)
        retrieved_place = DataManager.get(place.id, 'Place')
        self.assertEqual(place, retrieved_place)

    def test_update_place(self):
        place = Place('Beach House', 'A nice house by the beach', uuid4())
        DataManager.save(place)
        old_updated_at = place.updated_at
        place.name = 'Updated Beach House'
        DataManager.update(place)
        updated_place = DataManager.get(place.id, 'Place')
        self.assertNotEqual(old_updated_at, updated_place.updated_at)
        self.assertEqual(updated_place.name, 'Updated Beach House')

    def test_delete_place(self):
        place = Place('Beach House', 'A nice house by the beach', uuid4())
        DataManager.save(place)
        DataManager.delete(place.id, 'Place')
        retrieved_place = DataManager.get(place.id, 'Place')
        self.assertIsNone(retrieved_place)

    def test_get_all_places(self):
        place1 = Place('Beach House', 'A nice house by the beach', uuid4())
        place2 = Place('Mountain Cabin', 'A cozy cabin in the mountains', uuid4())
        places = {place1.id: place1, place2.id: place2}
        DataManager.save(place1)
        DataManager.save(place2)
        all_places_saved = DataManager.get_all_class("Place")
        self.assertEqual(all_places_saved, places)

class TestPlace_Storage(unittest.TestCase):
    def setUp(self):
        # limpiar data
        DataManager.data = {}

    def cleaner(self):
        # borrar json si existe
        if os.path.exists(Storage.file_path):
            os.remove(Storage.file_path) 
    
    def test_storage_serialization(self):
        place = Place('Beach House', 'A nice house by the beach', uuid4())
        DataManager.save(place)
        Storage.save()
        self.assertTrue(os.path.exists(Storage.file_path))

    def test_storage_deserialization(self):
        place = Place('Beach House', 'A nice house by the beach', uuid4())
        DataManager.save(place)
        Storage.save()
        self.setUp()
        Storage.load()
        load_place = DataManager.get(place.id, 'Place')
        self.assertEqual(place.name, load_place.name)
        self.assertEqual(place.description, load_place.description)
        self.assertEqual(place.host_id, load_place.host_id)

class TestPlace_API(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        DataManager.data = {}  

    def cleaner(self):
        if os.path.exists(Storage.file_path):
            os.remove(Storage.file_path)

    def test_add_place(self):
        place_data = {
            "name": "Test Place",
            "description": "A place for testing",
            "host_id": str(uuid4())
        }
        response = self.app.post('/places', json=place_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.get_json())

    def test_get_all_places(self):
        place1 = Place("Beach House", "A nice house by the beach", uuid4())
        place1.add_place()
        place2 = Place("Mountain Cabin", "A cozy cabin in the mountains", uuid4())
        place2.add_place()
        response = self.app.get('/places')
        self.assertEqual(response.status_code, 200)
        places = response.get_json()
        self.assertEqual(len(places), 2)

    def test_get_place(self):
        place = Place("Beach House", "A nice house by the beach", uuid4())
        place.add_place()
        response = self.app.get(f'/places/{place.id}')
        self.assertEqual(response.status_code, 200)
        place_data = response.get_json()
        self.assertEqual(place_data["name"], place.name)

    def test_update_place(self):
        place = Place("Beach House", "A nice house by the beach", uuid4())
        place.add_place()
        update_data = {
            "name": "Updated Beach House"
        }
        response = self.app.put(f'/places/{place.id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_place = Place.get(place.id)
        self.assertEqual(updated_place.name, "Updated Beach House")

    def test_delete_place(self):
        place = Place("Beach House", "A nice house by the beach", uuid4())
        place.add_place()
        response = self.app.delete(f'/places/{place.id}')
        self.assertEqual(response.status_code, 204)
        deleted_place = Place.get(place.id)
        self.assertIsNone(deleted_place)

    def test_add_place_invalid_name(self):
        place_data = {
            "name": "",
            "description": "A place for testing",
            "host_id": str(uuid4())
        }
        response = self.app.post('/places', json=place_data)
        self.assertEqual(response.status_code, 400)

    def test_add_place_invalid_description(self):
        place_data = {
            "name": "Test Place",
            "description": "",
            "host_id": str(uuid4())
        }
        response = self.app.post('/places', json=place_data)
        self.assertEqual(response.status_code, 400)

    def test_add_place_invalid_host_id(self):
        place_data = {
            "name": "Test Place",
            "description": "A place for testing",
            "host_id": "invalid-uuid"
        }
        response = self.app.post('/places', json=place_data)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
