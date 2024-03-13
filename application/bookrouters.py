from flask import render_template, url_for, flash, make_response
from flask import redirect, request
from flask import current_app as app
from application.database import db
from application.models import User, Section, Book
from flask_login import login_user, logout_user
from flask_login import login_required


@app.route("/book", methods=['GET', 'POST'])
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
    active_page = 'mybook'
    return render_template('mybooks.html', sections=sections,
                           active_page=active_page)


@app.route('/docs/<id>')
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
