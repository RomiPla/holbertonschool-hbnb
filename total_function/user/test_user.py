#!/usr/bin/python3

import unittest
import datetime
import json
import os
from uuid import uuid4
from abc import ABC, abstractmethod
from user_total import User
from user_total import DataManager, IPersistenceManager, Storage

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


    def test_storage_serialization(self):
        storage = Storage()
        user = User('pepe@pepe.com', 'pedro', 'pe')
        storage.new(user)
        storage.save()
        self.assertTrue(os.path.exists(Storage._Storage__file_path))

    """def test_storage_deserialization(self):
        storage = Storage()
        user = User('pepe@pepe.com', 'pedro', 'pe')
        storage.new(user)
        storage.save()
        storage.reload()
        retrieved_user = DataManager.get(user.id, 'User')
        self.assertEqual(user.email, retrieved_user.email)
        self.assertEqual(user.first_name, retrieved_user.first_name)
        self.assertEqual(user.last_name, retrieved_user.last_name)"""

if __name__ == '__main__':
    unittest.main()