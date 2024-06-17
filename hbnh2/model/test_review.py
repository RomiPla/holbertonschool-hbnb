#!/usr/bin/python3
import unittest
from review import Review
from basemodel import Basemodel
from place import Place
from user import User
from datamanager import DataManager

class TestReview(unittest.TestCase):
    
    def setUp(self):
        """Setup the necessary objects for testing"""
        Place.place_storage = {'place_1': Place()}
        User.user_emails = {'user_1': 'user1@example.com'}
        
        # Mock DataManager.save method
        DataManager.save = lambda self: None
    
    def test_review_creation_success(self):
        """Test that a review is created successfully"""
        review = Review(user_id='user_1', place_id='place_1', rating=5, comment='Great place!')
        self.assertEqual(review.user_id, 'user_1')
        self.assertEqual(review.place_id, 'place_1')
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Great place!')
    
    def test_review_missing_user_id(self):
        """Test that a ValueError is raised if user_id is missing"""
        with self.assertRaises(ValueError) as cm:
            Review(user_id=None, place_id='place_1', rating=5, comment='Great place!')
        self.assertEqual(str(cm.exception), "User ID, Place ID, and Rating must be provided.")
    
    def test_review_invalid_rating(self):
        """Test that a ValueError is raised if rating is invalid"""
        with self.assertRaises(ValueError) as cm:
            Review(user_id='user_1', place_id='place_1', rating=6, comment='Great place!')
        self.assertEqual(str(cm.exception), "Rating must be a number between 1 and 5.")
    
    def test_review_long_comment(self):
        """Test that a ValueError is raised if comment is too long"""
        with self.assertRaises(ValueError) as cm:
            Review(user_id='user_1', place_id='place_1', rating=5, comment='A' * 501)
        self.assertEqual(str(cm.exception), "Comment cannot be longer than 500 characters.")
    
    def test_place_does_not_exist(self):
        """Test that a ValueError is raised if place does not exist"""
        with self.assertRaises(ValueError) as cm:
            Review(user_id='user_1', place_id='invalid_place', rating=5, comment='Great place!')
        self.assertEqual(str(cm.exception), "Place with id invalid_place does not exist.")
    
    def test_user_does_not_exist(self):
        """Test that a ValueError is raised if user does not exist"""
        with self.assertRaises(ValueError) as cm:
            Review(user_id='invalid_user', place_id='place_1', rating=5, comment='Great place!')
        self.assertEqual(str(cm.exception), "User with id invalid_user does not exist.")

if __name__ == '__main__':
    unittest.main()
