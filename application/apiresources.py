from flask_restful import Resource, reqparse
from application.models import Book
from sqlalchemy import BLOB
from flask_restful import Api
from flask import current_app as app

api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('title', type=str, help='Rate to charge for this resource')
parser.add_argument('author', type=str,
                    help='Rate to charge for this resource')
parser.add_argument('stock', type=int, help='Rate to charge for this resource')
parser.add_argument('image', type=BLOB, help='Rate to charge for this resource')
parser.add_argument('content', type=BLOB,
                    help='Rate to charge for this resource')
parser.add_argument('section_id', type=int,
                    help='Rate to charge for this resource')

args = parser.parse_args()


class BookResource(Resource):
    def get(self, book_id):
        book = Book.query.get(book_id)
        if book:
            book_dic = {}
            book_dic['id'] = book.id
            book_dic['title'] = book.title
            book_dic['author'] = book.author
            book_dic['stock'] = book.stock
            book_dic['section_id'] = book.section_id
            return book_dic, 200
        else:
            return {'message': 'Book not found'}, 404

    def put(self, book_id):
        args = parser.parse_args()
        book = Book.query.get(book_id)
        if book:
            book.title = args['title']
            book.author = args['author']
            book.stock = args['stock']
            book.content = args['content'].decode('utf-8')
            book.image = args['image'].decode('utf-8')
            book.section_id = args['section_id']
            book.save()
            return {'message': 'Book updated'}, 200
        else:
            return {'message': 'Book not found'}, 404

    def delete(self, book_id):
        book = Book.query.get(book_id)
        if book:
            book.delete()
            return {'message': 'Book deleted'}, 200
        else:
            return {'message': 'Book not found'}, 404

    def post(self):
        args = parser.parse_args()
        book = Book(
            title=args['title'],
            author=args['author'],
            stock=args['stock'],
            section_id=args['section_id'],
            content=args['content'].decode('utf-8'),
            image=args['image'].decode('utf-8')
        )
        book.save()
        return {'message': 'Book created'}, 201


api.add_resource(BookResource, '/api/book/<int:book_id>', '/api/book')
