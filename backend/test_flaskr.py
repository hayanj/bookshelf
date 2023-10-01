import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Book


class BookTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "bookshelf_test"
        self.database_path = "postgresql://{}@{}/{}".format(
            "hayaaljuraysi", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        self.new_book = {"title": "Anansi Boys", "author": "Neil Gaiman", "rating": 5}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass


# @TODO: Write at least two tests for each endpoint - one each for success and error behavior.
#        You can feel free to write additional tests for nuanced functionality,
#        Such as adding a book without a rating, etc.
#        Since there are four routes currently, you should have at least eight tests.
# Optional: Update the book information in setUp to make the test database your own!

# Test paginated books
    def test_paginated_books(self):
        res = self.client.get('/books')
        data = json.load(res)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['books'])
        self.assertTrue(data['total_books'])

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/books?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# Test update rating
    def test_update_rating(self):
        res = self.client.patch('/books/3', json={"rating": 1})
        data = json.load(res)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

    def test_400_failed_update(self):
        res = self.client().patch('/books/3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

# Test delete book
    def test_delete_book(self):
        res = self.client.delete('/books/3')
        data = json.load(res)
        book = Book.query.filter(Book.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        self.assertTrue(data['books'])
        self.assertTrue(data['total_books'])
        self.assertEqual(book, None)

    def test_422_delete_unavailable_book(self):
        res = self.client().delete('/books/3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource unprocessable')

# Test create book
    def test_create_book(self):
        res = self.client.post('/books', json=self.new_book)
        data = json.load(res)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['books'])
        self.assertTrue(data['total_books'])

    def test_405_book_creation_not_allowed(self):
        res = self.client().post('/books/3', json=self.new_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()