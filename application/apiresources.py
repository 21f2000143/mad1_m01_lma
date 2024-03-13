from flask_restful import Resource, reqparse
from application.models import Book
from sqlalchemy import BLOB
from application.models import Section, db

class BookResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('author', type=str, help='Rate to charge for this resource')
        self.parser.add_argument('stock', type=int, help='Rate to charge for this resource')
        self.parser.add_argument('image', type=BLOB, help='Rate to charge for this resource')
        self.parser.add_argument('content', type=BLOB, help='Rate to charge for this resource')
        self.parser.add_argument('section_id', type=int, help='Rate to charge for this resource')
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


class SectionResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title', type=str,
                                 help='Title of the section')

    def get(self, section_id):
        section = Section.query.get(section_id)
        if section:
            section_dict = {
                'id': section.id,
                'title': section.title,
                # Optionally, you may include other properties of the section
            }
            return section_dict, 200
        else:
            return {'message': 'Section not found'}, 404

    def put(self, section_id):
        args = self.parser.parse_args()
        section = Section.query.get(section_id)
        if section:
            section.title = args['title']
            db.session.commit()
            return {'message': 'Section updated'}, 200
        else:
            return {'message': 'Section not found'}, 404

    def delete(self, section_id):
        section = Section.query.get(section_id)
        if section:
            db.session.delete(section)
            db.session.commit()
            return {'message': 'Section deleted'}, 200
        else:
            return {'message': 'Section not found'}, 404

    def post(self):
        args = self.parser.parse_args()
        section = Section(title=args['title'])
        db.session.add(section)
        db.session.commit()
        return {'message': 'Section created'}, 201
