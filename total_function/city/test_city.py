#!/usr/bin/python3

import unittest
import datetime
import json
import os
from uuid import uuid4
from abc import ABC, abstractmethod
from city import City
from city_total import DataManager, Storage, IPersistenceManager
from api import app

class TestCityLogical(unittest.TestCase):

    def test_city_name(self):
        city = City('New York', 'USA')
        self.assertEqual(city.name, 'New York')

        with self.assertRaises(TypeError, msg="City name must be a non-empty string"):
            city = City(123, 'USA')
        with self.assertRaises(TypeError, msg="City name must be a non-empty string"):
            city = City('', 'USA')
        with self.assertRaises(TypeError, msg="City name must be a non-empty string"):
            city = City(None, 'USA')

    def test_city_country(self):
        city = City('New York', 'USA')
        self.assertEqual(city.country, 'USA')

        with self.assertRaises(TypeError, msg="Country name must be a non-empty string"):
            city = City('New York', 123)
        with self.assertRaises(TypeError, msg="Country name must be a non-empty string"):
            city = City('New York', '')
        with self.assertRaises(TypeError, msg="Country name must be a non-empty string"):
            city = City('New York', None)

class TestCityDataManager(unittest.TestCase):

    def setUp(self):
        DataManager.data = {}  # Reset DataManager data for each test

    def test_save_city(self):
        city = City('New York', 'USA')
        DataManager.save(city)
        retrieved_city = DataManager.get(city.id, 'City')
        self.assertEqual(city, retrieved_city)

    def test_update_city(self):
        city = City('New York', 'USA')
        DataManager.save(city)
        old_updated_at = city.updated_at
        city.name = 'Los Angeles'
        DataManager.update(city)
        updated_city = DataManager.get(city.id, 'City')
        self.assertNotEqual(old_updated_at, updated_city.updated_at)
        self.assertEqual(updated_city.name, 'Los Angeles')

    def test_delete_city(self):
        city = City('New York', 'USA')
        DataManager.save(city)
        DataManager.delete(city.id, 'City')
        retrieved_city = DataManager.get(city.id, 'City')
        self.assertIsNone(retrieved_city)

    def test_get_all_cities(self):
        city1 = City('New York', 'USA')
        city2 = City('Los Angeles', 'USA')
        cities = {city1.id: city1, city2.id: city2}
        DataManager.save(city1)
        DataManager.save(city2)
        all_cities_saved = DataManager.get_all_class("City")
        self.assertEqual(all_cities_saved, cities)

class TestCityStorage(unittest.TestCase):
    def setUp(self):
        # limpiar data
        DataManager.data = {}

    def cleaner(self):
        # borrar json si existe
        if os.path.exists(Storage.file_path):
            os.remove(Storage.file_path) 
    
    def test_storage_serialization(self):
        city = City('New York', 'USA')
        DataManager.save(city)
        Storage.save()
        self.assertTrue(os.path.exists(Storage.file_path))

    def test_storage_deserialization(self):
        city = City('New York', 'USA')
        DataManager.save(city)
        Storage.save()
        self.setUp()
        Storage.load()
        load_city = DataManager.get(city.id, 'City')
        self.assertEqual(city.name, load_city.name)
        self.assertEqual(city.country, load_city.country)

class TestCityAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        DataManager.data = {}

    def cleaner(self):
        if os.path.exists(Storage.file_path):
            os.remove(Storage.file_path)

    def test_add_city(self):
        city_data = {
            "name": "Test City",
            "country": "Test Country"
        }
        response = self.app.post('/cities', json=city_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.get_json())

    def test_get_all_cities(self):
        city1 = City("Test City 1", "Test Country")
        city2 = City("Test City 2", "Test Country")
        DataManager.save(city1)
        DataManager.save(city2)
        response = self.app.get('/cities')
        self.assertEqual(response.status_code, 200)
        cities = response.get_json()
        self.assertEqual(len(cities), 2)

    def test_get_city(self):
        city = City("Test City", "Test Country")
        DataManager.save(city)
        response = self.app.get(f'/cities/{city.id}')
        self.assertEqual(response.status_code, 200)
        city_data = response.get_json()
        self.assertEqual(city_data["name"], city.name)

    def test_update_city(self):
        city = City("Test City", "Test Country")
        DataManager.save(city)
        update_data = {
            "name": "Updated City"
        }
        response = self.app.put(f'/cities/{city.id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_city = DataManager.get(city.id, 'City')
        self.assertEqual(updated_city.name, "Updated City")

    def test_delete_city(self):
        city = City("Test City", "Test Country")
        DataManager.save(city)
        response = self.app.delete(f'/cities/{city.id}')
        self.assertEqual(response.status_code, 204)
        deleted_city = DataManager.get(city.id, 'City')
        self.assertIsNone(deleted_city)

    def test_add_city_invalid_name(self):
        city_data = {
            "name": "",
            "country": "Test Country"
        }
        response = self.app.post('/cities', json=city_data)
        self.assertEqual(response.status_code, 400)

    def test_add_city_invalid_country(self):
        city_data = {
            "name": "Test City",
            "country": ""
        }
        response = self.app.post('/cities', json=city_data)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
