import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
import random

from models import setup_db, Book

BOOKS_PER_SHELF = 8

def paginate_books(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * BOOKS_PER_SHELF
    end = start + BOOKS_PER_SHELF
    formatted_books = [book.format() for book in selection]

    return formatted_books[start:end]



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route('/books')
    def get_books():
        books = Book.query.order_by(Book.id).all()
        paginated_books = paginate_books(request, books)
        if (len(paginated_books) == 0):
            abort(404)

        return jsonify({
            'success': True,
            'books': paginated_books,
            'total_books':len(books)
            })

    @app.route('/books/<int:book_id>', methods=['PATCH'])
    def update_book(book_id):
        body = request.get_json()
        try: 
            book = Book.query.filter(Book.id==book_id).one_or_none()
            if (book is None):
                abort(404)
            if ('rating' in body):
                rating = int(body.get('rating'))
                book.rating = rating

            book.update()
            return jsonify({
                'success': True,
                'id': book.id
                })
        except:
            abort(400)

    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        try:
            book = Book.query.filter(Book.id==book_id).one_or_none()
            if (book is None):
                abort(404)

            book.delete()
            books = Book.query.order_by(Book.id).all()
            paginated_books = paginate_books(request, books)
            return jsonify({
                'success': True,
                'deleted': book_id,
                'books': paginated_books,
                'total_books': len(books)
                })
        except:
            abort(400)

    @app.route('/books', methods=['POST'])
    def create_book():
        body = request.get_json()
        title = body.get('title', None)
        author = body.get('author', None)
        rating = body.get('rating', None)
        try:
            book = Book(title=title, author=author, rating=rating)
            book.insert()

            books = Book.query.order_by(id).all()
            paginated_books = paginate_books(request, books)

            return jsonify({
                'success': True,
                'created': book.id,
                'books': paginated_books,
                'total_books': len(books)
                })
        except:
            abort(422)
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'resource not found',
            'error': 404
        }), 404
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'message': 'resource unprocessable',
            'error': 422
        }), 422
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'message': 'Bad request',
            'error': 400
        }), 400
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'message': 'method not allowed',
            'error': 405
        }), 405

    return app