from flask import render_template, url_for, flash, make_response
from flask import redirect, request
from flask import current_app as app
from application.database import db
from application.models import User, Section, Book, Register
from flask_login import login_required, current_user
from sqlalchemy import or_
import datetime
import base64


@app.route("/book", methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        stock = request.form.get('stock')
        content = request.files['content'].read()
        image = request.files['image'].read()
        section_id = request.form.get('section_id')
        # verifying if the book already exists
        if Book.query.filter_by(title=title).first():
            flash("Book already exists", 'error')
            return redirect(url_for('home'))
        # add the book to the database
        book = Book(title=title, author=author, content=content,
                    section_id=section_id, stock=stock,
                    image=image)
        db.session.add(book)
        db.session.commit()
        flash("Book added successfully", 'success')
        return redirect(url_for('home'))
    sections = Section.query.all()
    active_page = 'book'
    return render_template('book.html', sections=sections,
                           active_page=active_page)


@app.route("/my/books", methods=['GET', 'POST'])
def my_books():
    # managing 7 days auto return policy!!
    registers = Register.query.filter(
            Register.user_id == current_user.id,
            Register.status == 'granted').all()
    for register in registers:
        dateobj = datetime.datetime.strptime(register.approve_date,
                                             '%Y-%m-%d')
        print(dateobj.strftime('%Y-%m-%d'))
        print(datetime.datetime.now().strftime('%Y-%m-%d'))
        difference = (datetime.datetime.now() - datetime.timedelta(days=7))
        if dateobj < difference:
            register.return_date = datetime.datetime.now().strftime('%Y-%m-%d')
            register.status = 'returned'
            db.session.commit()
    print(registers, "sachin")
    books = []
    for req in current_user.requests:
        if req.status == 'granted':
            book = Book.query.filter_by(id=req.book_id).first()
            books.append(book)
    book_data = [
        {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'stock': book.stock,
            'section_id': book.section_id,
            'image': base64.b64encode(book.image).decode('utf-8'),
        } for book in books
    ]
    active_page = 'mybook'
    return render_template('mybooks.html', books=book_data,
                           active_page=active_page)


@app.route('/docs/<id>')
@login_required
def get_pdf(id=None):
    if id is not None:
        book = Book.query.filter_by(id=id).first()
        if book is None:
            flash("Book not found", 'error')
            return redirect(url_for('home'))
        binary_pdf = book.content
        response = make_response(binary_pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = \
            'inline; filename=%s.pdf' % 'yourfilename'
        return response


@app.route('/reuested/book/<int:id>')
@login_required
def reuested_book(id):
    # Query the database for the book with the given ID
    book = Book.query.filter_by(id=id).first()
    if book:
        # Create a new register entry for the requested book
        no_of_requests = Register.query.filter(
            Register.user_id == current_user.id,
            or_(Register.status == 'pending', Register.status == 'granted')
        ).all()
        if len(no_of_requests) >= 5:
            flash("Already having access or requests for 5 resources",'danger')
            return redirect(url_for('home'))
        already_issued = Register.query.filter(
            Register.user_id == current_user.id,
            Register.book_id == book.id,
            Register.status == 'granted'
        ).first()
        if already_issued:
            flash("Already issued this book", 'warning')
            return redirect(url_for('home'))
        register = Register(request_date=datetime.datetime.now()
                            .strftime('%Y-%m-%d'),
                            book_name=book.title,
                            request_type='read',
                            status='pending',
                            user_id=current_user.id, book_id=book.id)
        db.session.add(register)
        db.session.commit()
        flash("Book requested successfully",'success')
        return redirect(url_for('home'))

    flash("Book not found",'error')
    return redirect(url_for('home'))
