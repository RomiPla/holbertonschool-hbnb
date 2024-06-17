#!/usr/bin/python3
import unittest
import os
from country_total import Country, DataManager, Storage
from api import app

class TestCountry_Logical(unittest.TestCase):

    def test_country_name(self):
        country = Country('USA', 'Washington D.C.', 328000000)
        self.assertEqual(country.name, 'USA')

        with self.assertRaises(ValueError, msg="Name must be a non-empty string."):
            country = Country('', 'Washington D.C.', 328000000)
        with self.assertRaises(ValueError, msg="Name must be a non-empty string."):
            country = Country(None, 'Washington D.C.', 328000000)
    
    def test_country_capital(self):
        country = Country('USA', 'Washington D.C.', 328000000)
        self.assertEqual(country.capital, 'Washington D.C.')

        with self.assertRaises(ValueError, msg="Capital must be a non-empty string."):
            country = Country('USA', '', 328000000)
        with self.assertRaises(ValueError, msg="Capital must be a non-empty string."):
            country = Country('USA', None, 328000000)

    def test_country_population(self):
        country = Country('USA', 'Washington D.C.', 328000000)
        self.assertEqual(country.population, 328000000)

        with self.assertRaises(ValueError, msg="Population must be a non-negative integer."):
            country = Country('USA', 'Washington D.C.', -100)
        with self.assertRaises(ValueError, msg="Population must be a non-negative integer."):
            country = Country('USA', 'Washington D.C.', 'abc')
        with self.assertRaises(ValueError, msg="Population must be a non-negative integer."):
            country = Country('USA', 'Washington D.C.', None)

class TestCountry_DataManager(unittest.TestCase):

    def setUp(self):
        DataManager.data = {}  # Restablecer los datos del DataManager antes de cada prueba

    def test_save_country(self):
        country = Country('USA', 'Washington D.C.', 328000000)
        DataManager.save(country)
        retrieved_country = DataManager.get(country.id, 'Country')
        self.assertEqual(country, retrieved_country)

    def test_update_country(self):
        country = Country('USA', 'Washington D.C.', 328000000)
        DataManager.save(country)
        old_updated_at = country.updated_at
        country.population = 330000000
        DataManager.update(country)
        updated_country = DataManager.get(country.id, 'Country')
        self.assertNotEqual(old_updated_at, updated_country.updated_at)
        self.assertEqual(updated_country.population, 330000000)

    def test_delete_country(self):
        country = Country('USA', 'Washington D.C.', 328000000)
        DataManager.save(country)
        DataManager.delete(country.id, 'Country')
        retrieved_country = DataManager.get(country.id, 'Country')
        self.assertIsNone(retrieved_country)

    def test_get_all_countries(self):
        country1 = Country('USA', 'Washington D.C.', 328000000)
        country2 = Country('China', 'Beijing', 1400000000)
        countries = {country1.id: country1, country2.id: country2}
        DataManager.save(country1)
        DataManager.save(country2)
        all_countries_saved = DataManager.get_all_class("Country")
        self.assertEqual(all_countries_saved, countries)

class TestCountry_Storage(unittest.TestCase):

    def setUp(self):
        DataManager.data = {}  # Restablecer los datos del DataManager antes de cada prueba

    def cleaner(self):
        if os.path.exists(Storage.file_path):
            os.remove(Storage.file_path)

    def test_storage_serialization(self):
        country = Country('USA', 'Washington D.C.', 328000000)
        DataManager.save(country)
        Storage.save()
        self.assertTrue(os.path.exists(Storage.file_path))

    def test_storage_deserialization(self):
        country = Country('USA', 'Washington D.C.', 328000000)
        DataManager.save(country)
        Storage.save()
        self.setUp()
        Storage.load()
        loaded_country = DataManager.get(country.id, 'Country')
        self.assertEqual(country.name, loaded_country.name)
        self.assertEqual(country.capital, loaded_country.capital)
        self.assertEqual(country.population, loaded_country.population)

class TestCountry_API(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        DataManager.data = {}  

    def cleaner(self):
        if os.path.exists(Storage.file_path):
            os.remove(Storage.file_path)

    def test_add_country(self):
        country_data = {
            "name": "Germany",
            "capital": "Berlin",
            "population": 83000000
        }
        response = self.app.post('/countries', json=country_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.get_json())

    """def test_get_all_countries(self):
        country1 = Country("USA", "Washington D.C.", 328000000)
        country1.add_country()
        country2 = Country("China", "Beijing", 1400000000)
        country2.add_country()
        response = self.app.get('/countries')
        self.assertEqual(response.status_code, 200)
        countries = response.get_json()
        self.assertEqual(len(countries), 2)

    def test_get_country(self):
        country = Country("Germany", "Berlin", 83000000)
        country.add_country()
        response = self.app.get(f'/countries/{country.id}')
        self.assertEqual(response.status_code, 200)
        country_data = response.get_json()
        self.assertEqual(country_data["name"], country.name)

    def test_update_country(self):
        country = Country("Germany", "Berlin", 83000000)
        country.add_country()
        update_data = {
            "population": 84000000
        }
        response = self.app.put(f'/countries/{country.id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_country = Country.get(country.id)
        self.assertEqual(updated_country.population, 84000000)

    def test_delete_country(self):
        country = Country("Germany", "Berlin", 83000000)
        country.add_country()
        response = self.app.delete(f'/countries/{country.id}')
        self.assertEqual(response.status_code, 204)
        deleted_country = Country.get(country.id)
        self.assertIsNone(deleted_country)"""

    def test_add_country_invalid_name(self):
        country_data = {
            "name": "",
            "capital": "Berlin",
            "population": 83000000
        }
        response = self.app.post('/countries', json=country_data)
        self.assertEqual(response.status_code, 400)

    def test_add_country_invalid_population(self):
        country_data = {
            "name": "Germany",
            "capital": "Berlin",
            "population": "abc"
        }
        response = self.app.post('/countries', json=country_data)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
