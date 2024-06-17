#!/usr/bin/python3

import unittest
import datetime
import json
import os
from uuid import uuid4
from abc import ABC, abstractmethod
from amenity_total import Amenity
from amenity_total import DataManager, IPersistenceManager, Storage
from api import app

class TestAmenity_Logical(unittest.TestCase):

    def test_amenity_name(self):
        amenity = Amenity('Swimming Pool')
        self.assertEqual(amenity.name, 'Swimming Pool')

        with self.assertRaises(TypeError, msg="Amenity name must be a non-empty string"):
            amenity = Amenity('')
        with self.assertRaises(TypeError, msg="Amenity name must be a non-empty string"):
            amenity = Amenity(None)

class TestAmenity_DataManager(unittest.TestCase):

    def setUp(self):
        DataManager.data = {}  # Reset DataManager data for each test

    def test_save_amenity(self):
        amenity = Amenity('Swimming Pool')
        DataManager.save(amenity)
        retrieved_amenity = DataManager.get(amenity.id, 'Amenity')
        self.assertEqual(amenity, retrieved_amenity)

    def test_update_amenity(self):
        amenity = Amenity('Swimming Pool')
        DataManager.save(amenity)
        old_updated_at = amenity.updated_at
        amenity.name = 'Gym'
        DataManager.update(amenity)
        updated_amenity = DataManager.get(amenity.id, 'Amenity')
        self.assertNotEqual(old_updated_at, updated_amenity.updated_at)
        self.assertEqual(updated_amenity.name, 'Gym')

    def test_delete_amenity(self):
        amenity = Amenity('Swimming Pool')
        DataManager.save(amenity)
        DataManager.delete(amenity.id, 'Amenity')
        retrieved_amenity = DataManager.get(amenity.id, 'Amenity')
        self.assertIsNone(retrieved_amenity)

    def test_get_all_amenities(self):
        amenity = Amenity('Swimming Pool')
        amenity2 = Amenity('Gym')
        amenities = {amenity.id: amenity, amenity2.id: amenity2}
        DataManager.save(amenity)
        DataManager.save(amenity2)
        all_amenities_saved = DataManager.get_all_class("Amenity")
        self.assertEqual(all_amenities_saved, amenities)

class TestAmenity_Storage(unittest.TestCase):
    def setUp(self):
        # limpiar data
        DataManager.data = {}

    def cleaner(self):
        # borrar json si existe
        if os.path.exists(Storage.file_path):
            os.remove(Storage.file_path) 
    
    def test_storage_serialization(self):
        amenity = Amenity('Swimming Pool')
        DataManager.save(amenity)
        Storage.save()
        self.assertTrue(os.path.exists(Storage.file_path))

    def test_storage_deserialization(self):
        amenity = Amenity('Swimming Pool')
        DataManager.save(amenity)
        Storage.save()
        self.setUp()
        Storage.load()
        load_amenity = DataManager.get(amenity.id, 'Amenity')
        self.assertEqual(amenity.name, load_amenity.name)

class TestAmenity_API(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        DataManager.data = {}  

    def cleaner(self):
        if os.path.exists(Storage.file_path):
            os.remove(Storage.file_path)

    def test_add_amenity(self):
        amenity_data = {
            "name": "Gym"
        }
        response = self.app.post('/amenities', json=amenity_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.get_json())

    def test_get_all_amenities(self):
        amenity1 = Amenity("Swimming Pool")
        amenity1.add_amenity()
        amenity2 = Amenity("Gym")
        amenity2.add_amenity()
        response = self.app.get('/amenities')
        self.assertEqual(response.status_code, 200)
        amenities = response.get_json()
        self.assertEqual(len(amenities), 2)

    def test_get_amenity(self):
        amenity = Amenity("Swimming Pool")
        amenity.add_amenity()
        response = self.app.get(f'/amenities/{amenity.id}')
        self.assertEqual(response.status_code, 200)
        amenity_data = response.get_json()
        self.assertEqual(amenity_data["name"], amenity.name)

    def test_update_amenity(self):
        amenity = Amenity("Swimming Pool")
        amenity.add_amenity()
        update_data = {
            "name": "Updated Gym"
        }
        response = self.app.put(f'/amenities/{amenity.id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_amenity = Amenity.get(amenity.id)
        self.assertEqual(updated_amenity.name, "Updated Gym")

    def test_delete_amenity(self):
        amenity = Amenity("Swimming Pool")
        amenity.add_amenity()
        response = self.app.delete(f'/amenities/{amenity.id}')
        self.assertEqual(response.status_code, 204)
        deleted_amenity = Amenity.get(amenity.id)
        self.assertIsNone(deleted_amenity)

    def test_add_amenity_invalid_name(self):
        amenity_data = {
            "name": ""
        }
        response = self.app.post('/amenities', json=amenity_data)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
