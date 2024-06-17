#!/usr/bin/python3

import unittest
import os
from uuid import uuid4
from review_total import review
from review_total import Review, DataManager, Storage
from api import app

class TestReview_Logical(unittest.TestCase):

    def test_review_title(self):
        review = Review('Great product!', 'This product exceeded my expectations.', 5)
        self.assertEqual(review.title, 'Great product!')

        with self.assertRaises(ValueError, msg="Title must be a non-empty string."):
            review = Review('', 'Good product', 4)
        with self.assertRaises(ValueError, msg="Title must be a non-empty string."):
            review = Review(None, 'Good product', 4)

    def test_review_content(self):
        review = Review('Great product!', 'This product exceeded my expectations.', 5)
        self.assertEqual(review.content, 'This product exceeded my expectations.')

        with self.assertRaises(ValueError, msg="Content must be a non-empty string."):
            review = Review('Good product', '', 4)
        with self.assertRaises(ValueError, msg="Content must be a non-empty string."):
            review = Review('Good product', None, 4)

    def test_review_rating(self):
        review = Review('Great product!', 'This product exceeded my expectations.', 5)
        self.assertEqual(review.rating, 5)

        with self.assertRaises(ValueError, msg="Rating must be an integer between 1 and 5."):
            review = Review('Good product', 'This is a good product', 6)
        with self.assertRaises(ValueError, msg="Rating must be an integer between 1 and 5."):
            review = Review('Good product', 'This is a good product', 0)
        with self.assertRaises(ValueError, msg="Rating must be an integer between 1 and 5."):
            review = Review('Good product', 'This is a good product', '5')

class TestReview_DataManager(unittest.TestCase):

    def setUp(self):
        DataManager.data = {}  # Reset DataManager data for each test

    def test_save_review(self):
        review = Review('Great product!', 'This product exceeded my expectations.', 5)
        DataManager.save(review)
        retrieved_review = DataManager.get(review.id, 'Review')
        self.assertEqual(review, retrieved_review)

    def test_update_review(self):
        review = Review('Great product!', 'This product exceeded my expectations.', 5)
        DataManager.save(review)
        old_updated_at = review.updated_at
        review.title = 'Excellent product!'
        DataManager.update(review)
        updated_review = DataManager.get(review.id, 'Review')
        self.assertNotEqual(old_updated_at, updated_review.updated_at)
        self.assertEqual(updated_review.title, 'Excellent product!')

    def test_delete_review(self):
        review = Review('Great product!', 'This product exceeded my expectations.', 5)
        DataManager.save(review)
        DataManager.delete(review.id, 'Review')
        retrieved_review = DataManager.get(review.id, 'Review')
        self.assertIsNone(retrieved_review)

    def test_get_all_reviews(self):
        review1 = Review('Great product!', 'This product exceeded my expectations.', 5)
        review2 = Review('Good product!', 'This is a good product.', 4)
        reviews = {review1.id: review1, review2.id: review2}
        DataManager.save(review1)
        DataManager.save(review2)
        all_reviews_saved = DataManager.get_all_class("Review")
        self.assertEqual(all_reviews_saved, reviews)

class TestReview_Storage(unittest.TestCase):

    def setUp(self):
        DataManager.data = {}

    def cleaner(self):
        if os.path.exists(Storage.file_path):
            os.remove(Storage.file_path)

    def test_storage_serialization(self):
        review = Review('Great product!', 'This product exceeded my expectations.', 5)
        DataManager.save(review)
        Storage.save()
        self.assertTrue(os.path.exists(Storage.file_path))

    def test_storage_deserialization(self):
        review = Review('Great product!', 'This product exceeded my expectations.', 5)
        DataManager.save(review)
        Storage.save()
        self.setUp()
        Storage.load()
        loaded_review = DataManager.get(review.id, 'Review')
        self.assertEqual(review.title, loaded_review.title)
        self.assertEqual(review.content, loaded_review.content)
        self.assertEqual(review.rating, loaded_review.rating)

class TestReview_API(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        DataManager.data = {}

    def cleaner(self):
        if os.path.exists(Storage.file_path):
            os.remove(Storage.file_path)

    def test_add_review(self):
        review_data = {
            "title": "Great product!",
            "content": "This product exceeded my expectations.",
            "rating": 5
        }
        response = self.app.post('/reviews', json=review_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.get_json())

    """def test_get_all_reviews(self):
        review1 = Review("Great product!", "This product exceeded my expectations.", 5)
        review1.add_review()
        review2 = Review("Good product!", "This is a good product.", 4)
        review2.add_review()
        response = self.app.get('/reviews')
        self.assertEqual(response.status_code, 200)
        reviews = response.get_json()
        self.assertEqual(len(reviews), 2)

    def test_get_review(self):
        review = Review("Great product!", "This product exceeded my expectations.", 5)
        review.add_review()
        response = self.app.get(f'/reviews/{review.id}')
        self.assertEqual(response.status_code, 200)
        review_data = response.get_json()
        self.assertEqual(review_data["title"], review.title)

    def test_update_review(self):
        review = Review("Great product!", "This product exceeded my expectations.", 5)
        review.add_review()
        update_data = {
            "title": "Updated product"
        }
        response = self.app.put(f'/reviews/{review.id}', json=update_data)
        self.assertEqual(response.status_code, 200)
        updated_review = Review.get(review.id)
        self.assertEqual(updated_review.title, "Updated product")

    def test_delete_review(self):
        review = Review("Great product!", "This product exceeded my expectations.", 5)
        review.add_review()
        response = self.app.delete(f'/reviews/{review.id}')
        self.assertEqual(response.status_code, 204)
        deleted_review = Review.get(review.id)
        self.assertIsNone(deleted_review)

    def test_add_review_invalid_title(self):
        review_data = {
            "title": "",
            "content": "This product exceeded my expectations.",
            "rating": 5
        }
        response = self.app.post('/reviews', json=review_data)
        self.assertEqual(response.status_code, 400)

    def test_add_review_invalid_content(self):
        review_data = {
            "title": "Great product!",
            "content": "",
            "rating": 5
        }
        response = self.app.post('/reviews', json=review_data)
        self.assertEqual(response.status_code, 400)

    def test_add_review_invalid_rating(self):
        review_data = {
            "title": "Great product!",
            "content": "This product exceeded my expectations.",
            "rating": 6
        }
        response = self.app.post('/reviews', json=review_data)
        self.assertEqual(response.status_code, 400)"""

if __name__ == '__main__':
    unittest.main()
