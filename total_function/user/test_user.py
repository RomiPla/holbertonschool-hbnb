#!/usr/bin/python3

import unittest
import datetime
import json
import os
from uuid import uuid4
from abc import ABC, abstractmethod
from user_total import User
from user_total import DataManager, IPersistenceManager, Storage
from api import app

class TestUser_Logical(unittest.TestCase):

    def test_user_first_name(self):
        user = User('pepe@pepe.com', 'Pedro', 'pe')
        self.assertEqual(user.first_name, 'Pedro')

        with self.assertRaises(TypeError, msg="First name must be a non-empty string with only alphabetic characters"):
            user = User('pepe@pepe.com', 'Pedro123', 'Pacheco')
        with self.assertRaises(TypeError, msg="First name must be a non-empty string with only alphabetic characters"):
            user = User('pepe@pepe.com', 'Pedro!', 'Pacheco')
        with self.assertRaises(TypeError, msg="First name must be a non-empty string with only alphabetic characters"):
            user = User('pepe@pepe.com', '', 'Pacheco')
        with self.assertRaises(TypeError, msg="First name must be a non-empty string with only alphabetic characters"):
            user = User('pepe@pepe.com', None, 'Pacheco')

    def test_user_last_name(self):
        user = User('pepe@pepe.com', 'pedro', 'Pacheco')
        self.assertEqual(user.last_name, 'Pacheco')

        with self.assertRaises(TypeError, msg="Last name must be a non-empty string with only alphabetic characters"):
            user = User('pepe@pepe.com', 'Pedro', 'Pacheco123')
        with self.assertRaises(TypeError, msg="Last name must be a non-empty string with only alphabetic characters"):
            user = User('pepe@pepe.com', 'Pedro', 'Pacheco!')
        with self.assertRaises(TypeError, msg="Last name must be a non-empty string with only alphabetic characters"):
            user = User('pepe@pepe.com', 'Pedro', '')
        with self.assertRaises(TypeError, msg="Last name must be a non-empty string with only alphabetic characters"):
            user = User('pepe@pepe.com', 'Pedro', None)

    def test_user_valid_email(self):
        user = User('pepe@pepe.com', 'pedro', 'pe')
        self.assertEqual(user.email, 'pepe@pepe.com')
        user = User('pe_e@pepe.com', 'Pedro', 'Pacheco')
        self.assertEqual(user.email, 'pe_e@pepe.com')
        user = User('pe.e@pepe.com', 'Pedro', 'Pacheco')
        self.assertEqual(user.email, 'pe.e@pepe.com')

    def test_user_not_valid_email(self):
        with self.assertRaises(TypeError, msg="Email must be a non-empty string in a valid email format"):
            user = User('pepepepe.com', 'Pedro', 'Pacheco')
        with self.assertRaises(TypeError, msg="Email must be a non-empty string in a valid email format"):
            user = User('pepepepecom', 'Pedro', 'Pacheco')
        with self.assertRaises(TypeError, msg="Email must be a non-empty string in a valid email format"):
            user = User('@pepepepe.com', 'Pedro', 'Pacheco')
        with self.assertRaises(TypeError, msg="Email must be a non-empty string in a valid email format"):
            user = User('pepe@pepecom', 'Pedro', 'Pacheco')
        with self.assertRaises(TypeError, msg="Email must be a non-empty string in a valid email format"):
            user = User('', 'Pedro', 'Pacheco')
        with self.assertRaises(TypeError, msg="Email must be a non-empty string in a valid email format"):
            user = User(None, 'Pedro', 'Pacheco')

class TestUser_DataManager(unittest.TestCase):

    def setUp(self):
        DataManager.data = {}  # Reset DataManager data for each test

    def test_save_user(self):
        user = User('pepe@pepe.com', 'pedro', 'pe')
        DataManager.save(user)
        retrieved_user = DataManager.get(user.id, 'User')
        self.assertEqual(user, retrieved_user)

    def test_update_user(self):
        user = User('pepe@pepe.com', 'pedro', 'pe')
        DataManager.save(user)
        old_updated_at = user.updated_at
        user.email = 'new_email@pepe.com'
        DataManager.update(user)
        updated_user = DataManager.get(user.id, 'User')
        self.assertNotEqual(old_updated_at, updated_user.updated_at)
        self.assertEqual(updated_user.email, 'new_email@pepe.com')

    def test_delete_user(self):
        user = User('pepe@pepe.com', 'pedro', 'pe')
        DataManager.save(user)
        DataManager.delete(user.id, 'User')
        retrieved_user = DataManager.get(user.id, 'User')
        self.assertIsNone(retrieved_user)

    def test_get_all_users(self):
        user = User('pepe@pepe.com', 'pedro', 'pe')
        user2 = User('gg@izi.com', 'salch', 'ichon')
        users = {user.id: user, user2.id: user2}
        DataManager.save(user)
        DataManager.save(user2)
        all_users_saved = DataManager.get_all_class("User")
        self.assertEqual(all_users_saved, users)

class TestUser_Storage(unittest.TestCase):
    def setUp(self):
        # limpiar data
        DataManager.data = {}

    def cleaner(self):
        # borrar json si existe
        if os.path.exists(Storage.file_path):
            os.remove(Storage.file_path) 
    
    def test_storage_serialization(self):
        user = User('pepe@pepe.com', 'PEDRO', 'pe')
        DataManager.save(user)
        Storage.save()
        self.assertTrue(os.path.exists(Storage.file_path))

    def test_storage_deserialization(self):
        user = User('pepe@pepe.com', 'pedro', 'Pe')
        DataManager.save(user)
        Storage.save()
        self.setUp()
        Storage.load()
        load_user = DataManager.get(user.id, 'User')
        self.assertEqual(user.email, load_user.email)
        self.assertEqual(user.first_name, load_user.first_name)
        self.assertEqual(user.last_name, load_user.last_name)

class TestUser_API(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        DataManager.data = {}  

    def cleaner(self):
        if os.path.exists(Storage.file_path):
            os.remove(Storage.file_path)

    def test_add_user(self):
        user_data = {
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "User"
        }
        response = self.app.post('/users', json=user_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.get_json())

    def test_get_all_users(self):
        user1 = User("test1@test.com", "ramon", "cri")
        user1.add_user()
        user2 = User("test2@test.com", "jonh", "wick")
        user2.add_user()
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        users = response.get_json()
        self.assertEqual(len(users), 2)

    def test_get_user(self):
        user = User("test@test.com", "Test", "User")
        user.add_user()
        response = self.app.get(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        user_data = response.get_json()
        self.assertEqual(user_data["email"], user.email)

    def test_update_user(self):
        user = User("test@test.com", "Test", "User")
        user.add_user()
        update_data = {
            "first_name": "UpdatedTest"
        }
        response = self.app.put(f'/users/{user.id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_user = User.get(user.id)
        self.assertEqual(updated_user.first_name, "UpdatedTest")

    def test_delete_user(self):
        user = User("test@test.com", "Test", "User")
        user.add_user()
        response = self.app.delete(f'/users/{user.id}')
        self.assertEqual(response.status_code, 204)
        deleted_user = User.get(user.id)
        self.assertIsNone(deleted_user)

    def test_add_user_invalid_email(self):
        user_data = {
            "email": "invalid_email",
            "first_name": "Test",
            "last_name": "User"
        }
        response = self.app.post('/users', json=user_data)
        self.assertEqual(response.status_code, 400)

    def test_add_user_duplicate_email(self):
        user_data = {
            "email": "duplicate@test.com",
            "first_name": "Test",
            "last_name": "User"
        }
        self.app.post('/users', json=user_data)
        response = self.app.post('/users', json=user_data)
        self.assertEqual(response.status_code, 409)

    def test_add_user_invalid_first_name(self):
        user_data = {
            "email": "test@test.com",
            "first_name": "gg!",
            "last_name": "User"
        }
        response = self.app.post('/users', json=user_data)
        self.assertEqual(response.status_code, 400)

    def test_add_user_invalid_last_name(self):
        user_data = {
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "Usez#"
        }
        response = self.app.post('/users', json=user_data)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()