#!/usr/bin/python3

import unittest
import datetime
import json
import os
from city import City
from country import Country
from datamanager import DataManager
from storage import Storage
from api import app

print("CITY")

class TestCityLogical(unittest.TestCase):
    def setUp(self):
        DataManager.data = {}

    def test_city_creation(self):
        city = City('Buenos Aires', 'AR')
        self.assertEqual(city.name, 'Buenos Aires')
        self.assertEqual(city.country_code, 'AR')

        with self.assertRaises(TypeError):
            City('', 'AR')
        with self.assertRaises(TypeError):
            City('Buenos Aires', '')
        with self.assertRaises(TypeError):
            City(123, 'AR')
        with self.assertRaises(TypeError):
            City('Buenos Aires', 123)

class TestCityDataManager(unittest.TestCase):
    def setUp(self):
        DataManager.data = {}

    def test_city_uniqueness(self):
        city1 = City('Buenos Aires', 'AR')
        DataManager.save(city1)
        with self.assertRaises(ValueError):
            City('Buenos Aires', 'AR')

    def test_save_city(self):
        city = City('Buenos Aires', 'AR')
        DataManager.save(city)
        retrieved_city = DataManager.get(city.id, 'City')
        self.assertEqual(city, retrieved_city)

    def test_get_all_cities(self):
        city1 = City('Buenos Aires', 'AR')
        city2 = City('Cordoba', 'AR')
        DataManager.save(city1)
        DataManager.save(city2)
        all_cities = City.get_all()
        self.assertEqual(len(all_cities), 2)

class TestCityAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        DataManager.data = {}
        Country.load_countries()

    def test_create_city(self):
        city_data = {
            "name": "Buenos Aires",
            "country_code": "AR"
        }
        response = self.app.post('/cities', json=city_data)
        self.assertEqual(response.status_code, 201)
        city = response.get_json()
        self.assertEqual(city["name"], "Buenos Aires")
        self.assertEqual(city["country_code"], "AR")

    def test_create_city_invalid_data(self):
        city_data = {
            "name": "",
            "country_code": "AR"
        }
        response = self.app.post('/cities', json=city_data)
        self.assertEqual(response.status_code, 400)

    def test_get_all_cities(self):
        DataManager.data = {}
        city1 = City('Buenos Aires', 'AR')
        city2 = City('Cordoba', 'AR')
        DataManager.save(city1)
        DataManager.save(city2)
        response = self.app.get('/cities')
        self.assertEqual(response.status_code, 200)
        cities = response.get_json()
        self.assertEqual(len(cities), 2)

    def test_get_city(self):
        city = City('Buenos Aires', 'AR')
        City.add(city)
        response = self.app.get(f'/cities/{city.id}')
        self.assertEqual(response.status_code, 200)
        city_data = response.get_json()
        self.assertEqual(city_data['name'], 'Buenos Aires')
        self.assertEqual(city_data['country_code'], 'AR')

    def test_get_city_not_valid_id(self):
        response = self.app.get('/cities/123')
        self.assertEqual(response.status_code, 400)

    def test_update_city(self):
        city = City('Buenos Aires', 'AR')
        City.add(city)

        update_data = {
            "name": "Montevideo",
            "country_code": "UY"
        }
        response = self.app.put(f'/cities/{city.id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_city = City.get(city.id)
        self.assertEqual(updated_city.name, "Montevideo")

    def test_update_city_invalid_data(self):
        city = City('Buenos Aires', 'AR')
        DataManager.save(city)
        update_data = {
            "name": 2
        }
        response = self.app.put(f'/cities/{city.id}', json=update_data)
        self.assertEqual(response.status_code, 400)

    def test_delete_city(self):
        city = City('Buenos Aires', 'AR')
        DataManager.save(city)
        response = self.app.delete(f'/cities/{city.id}')
        self.assertEqual(response.status_code, 204)
        deleted_city = City.get(city.id)
        self.assertIsNone(deleted_city)

if __name__ == '__main__':
    unittest.main()