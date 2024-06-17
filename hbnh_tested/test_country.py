#!/usr/bin/python3
import unittest
import os
from country import Country, DataManager
from storage import Storage
from api import app
from city import City

print("COUNTRY")

class TestCountry_Logical(unittest.TestCase):

    def test_country_attributes(self):
        country = Country("Argentina", "AR")
        self.assertEqual(country.name, "Argentina")
        self.assertEqual(country.code, "AR")

        with self.assertRaises(AttributeError):
            country.name = "Brazil"
        with self.assertRaises(AttributeError):
            country.code = "BR"

    def test_to_dict(self):
        country = Country("Argentina", "AR")
        country_dict = country.to_dict()
        self.assertEqual(country_dict['name'], "Argentina")
        self.assertEqual(country_dict['code'], "AR")

class TestCountry_DataManager(unittest.TestCase):

    def setUp(self):
        DataManager.data = {}

    def test_load_countries(self):
        Country.load_countries()
        countries = DataManager.data.get("Country")
        self.assertIsNotNone(countries)
        self.assertIn("AR", countries)
        self.assertEqual(countries["AR"].name, "Argentina")
        self.assertEqual(countries["AR"].code, "AR")

    def test_save_country(self):
        Country.load_countries()
        country = Country("Argentina", "AR")
        retrieved_country = DataManager.get(country.code, 'Country')
        self.assertEqual(DataManager.data["Country"][country.code], retrieved_country)

    def test_delete_country(self):
        Country.load_countries()
        country = Country("Argentina", "AR")
        DataManager.delete(country.code, 'Country')
        retrieved_country = DataManager.get(country.code, 'Country')
        self.assertIsNone(retrieved_country)

    """def test_get_all_countries(self):
        countries = {}
        for country in pycountry.countries:
            country_obj = Country(country.name, country.alpha_2)
            countries = {country_obj.to_dict()}
        all_countries_saved = DataManager.get_all_class("Country")
        self.assertEqual(all_countries_saved, countries)"""

class TestCountry_Storage(unittest.TestCase):

    def setUp(self):
        DataManager.data = {}

    def cleaner(self):
        if os.path.exists(Storage.file_path):
            os.remove(Storage.file_path)

    def test_storage_serialization(self):
        Country.load_countries()
        Storage.save()
        self.assertTrue(os.path.exists(Storage.file_path))

    def test_storage_deserialization(self):
        Country.load_countries()
        Storage.save()
        self.setUp()
        Storage.load()
        country = Country("Argentina", "AR")
        load_country = DataManager.get(country.code, 'Country')
        self.assertEqual(country.name, load_country.name)
        self.assertEqual(country.code, load_country.code)

class TestCountry_API(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        DataManager.data = {}
        Country.load_countries()

    def test_get_all_countries(self):
        response = self.app.get('/countries')
        self.assertEqual(response.status_code, 200)
        countries = response.get_json()
        self.assertTrue(len(countries) > 0)
    
    def test_get_country(self):
        response = self.app.get('/countries/AR')
        self.assertEqual(response.status_code, 200)
        country = response.get_json()
        self.assertEqual(country['code'], 'AR')
        self.assertEqual(country['name'], 'Argentina')

    def test_get_country_not_found(self):
        response = self.app.get('/countries/ZZ')
        self.assertEqual(response.status_code, 404)
        error_msg = response.get_json()
        self.assertEqual(error_msg["error"], "Country not found")

    def test_invalid_country_code(self):
        response = self.app.get('/countries/123')
        self.assertEqual(response.status_code, 400)
        error_msg = response.get_json()
        self.assertEqual(error_msg["error"], "Country code must be a non-empty string with only two alphabetic characters.")

    def test_get_country_cities(self):
            city1 = City('Buenos Aires', 'AR')
            city2 = City('Cordoba', 'AR')
            city3 = City('Santiago', 'CL')
            DataManager.save(city1)
            DataManager.save(city2)
            DataManager.save(city3)

            response = self.app.get('/countries/AR/cities')
            self.assertEqual(response.status_code, 200)
            cities = response.get_json()
            self.assertEqual(len(cities), 2)
            self.assertEqual(cities[0]['name'], 'Buenos Aires')
            self.assertEqual(cities[1]['name'], 'Cordoba')

    def test_get_country_cities_not_found(self):
        response = self.app.get('/countries/ZZ/cities')
        self.assertEqual(response.status_code, 404)
        error_msg = response.get_json()
        self.assertEqual(error_msg["error"], "Country not found")


if __name__ == '__main__':
    unittest.main()
