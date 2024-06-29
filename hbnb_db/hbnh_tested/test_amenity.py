#!/usr/bin/python3
import unittest
from amenity import Amenity
from datamanager import DataManager
import os
from storage import Storage
from api import app

print("AMENITY")

class TestAmenity_Logical(unittest.TestCase):

    def test_amenity_name(self):
        pool = Amenity("Pool", "cool")
        self.assertEqual(pool.name, "Pool")

        with self.assertRaises(TypeError, msg="Amenity name must be a non-empty string"):
            pool = Amenity('')
        with self.assertRaises(TypeError, msg="Amenity name must be a non-empty string"):
            pool = Amenity(None)

class TestAmenity_DataManager(unittest.TestCase):

    def setUp(self):
        DataManager.data = {}

    def test_save_amenity(self):
        pool = Amenity("Pool", "cool")
        Amenity.add(pool)
        retrieved_amenity = Amenity.get(pool.id)
        self.assertEqual(pool, retrieved_amenity)

    def test_update_amenity(self):
        pool = Amenity("Pool", "cool")
        Amenity.add(pool)
        old_updated_at = pool.updated_at
        pool.name = 'Gym'
        Amenity.update(pool)
        updated_amenity = Amenity.get(pool.id)
        self.assertNotEqual(old_updated_at, updated_amenity.updated_at)
        self.assertEqual(updated_amenity.name, 'Gym')

    def test_delete_amenity(self):
        pool = Amenity("Pool", "cool")
        Amenity.add(pool)
        Amenity.delete(pool)
        retrieved_amenity = Amenity.get(pool.id)
        self.assertIsNone(retrieved_amenity)

    def test_get_all_amenities(self):
        pool = Amenity("Pool", "cool")
        gym = Amenity("Gym", "Yuka")
        amenities = {pool.id: pool, gym.id: gym}
        Amenity.add(pool)
        Amenity.add(gym)
        all_amenities_saved = DataManager.get_all_class("Amenity")
        self.assertEqual(all_amenities_saved, amenities)

class TestAmenity_Storage(unittest.TestCase):
    def setUp(self):
        DataManager.data = {}

    def cleaner(self):
        if os.path.exists(Storage.file_path):
            os.remove(Storage.file_path) 
    
    def test_storage_serialization(self):
        pool = Amenity("Pool", "cool")
        Amenity.add(pool)
        Storage.save()
        self.assertTrue(os.path.exists(Storage.file_path))

    def test_storage_deserialization(self):
        pool = Amenity("Pool", "cool")
        Amenity.add(pool)
        Storage.save()
        self.setUp()
        Storage.load()
        load_amenity = Amenity.get(pool.id)
        self.assertEqual(pool.name, load_amenity.name)

class TestAmenity_API(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        DataManager.data = {}  

    def cleaner(self):
        if os.path.exists(Storage.file_path):
            os.remove(Storage.file_path)

    def test_get_all_amenities(self):
        pool = Amenity("Pool", "cool")
        Amenity.add(pool)
        gym = Amenity("Gym", "Yuka")
        Amenity.add(gym)
        response = self.app.get('/amenities')
        self.assertEqual(response.status_code, 200)
        amenities = response.get_json()
        self.assertEqual(len(amenities), 2)

    def test_get_amenity(self):
        pool = Amenity("Pool", "cool")
        Amenity.add(pool)
        response = self.app.get(f'/amenities/{pool.id}')
        self.assertEqual(response.status_code, 200)
        amenity_data = response.get_json()
        self.assertEqual(amenity_data["name"], pool.name)

    def test_add_amenity(self):
        amenity_data = {
            "name": "Gym",
            "description": "Yuka"
        }
        response = self.app.post('/amenities', json=amenity_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.get_json())

    def test_update_amenity(self):
        pool = Amenity("Pool", "cool")
        Amenity.add(pool)
        update_data = {
            "name": "Updated to Gym"
        }
        response = self.app.put(f'/amenities/{pool.id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_amenity = Amenity.get(pool.id)
        self.assertEqual(updated_amenity.name, "Updated to Gym")

    def test_delete_amenity(self):
        pool = Amenity("Pool", "cool")
        Amenity.add(pool)
        response = self.app.delete(f'/amenities/{pool.id}')
        self.assertEqual(response.status_code, 204)
        deleted_amenity = Amenity.get(pool.id)
        self.assertIsNone(deleted_amenity)    


if __name__ == '__main__':
    unittest.main()