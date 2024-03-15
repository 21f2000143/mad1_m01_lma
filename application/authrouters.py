from flask import render_template, url_for, flash
from flask import redirect, request
from flask import current_app as app
from application.database import db
import base64
from application.models import User, Section, Book, Register
from flask_login import login_user, logout_user, current_user
from flask_login import login_required
from sqlalchemy import or_


@app.route("/", methods=['GET', 'POST'])
def home():
    searchby = request.args.get('searchby', None)
    sections = None
    books = None
    if searchby and (searchby != 'All Categories'):
        sections = Section.query.filter(or_(
            Section.title.ilike(f'%{searchby}%')
        )).all()
        books = Book.query.filter(or_(
            Book.title.ilike(f'%{searchby}%'),
            Book.author.ilike(f'%{searchby}%'),
            Book.section.has(Section.title.ilike(f'%{searchby}%'))
        )).all()
    else:
        sections = Section.query.all()
        books = Book.query.all()
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
    active_page = 'home'
    filter_sections = Section.query.all()
    return render_template('index.html', active_page=active_page,
                           books=book_data, sections=sections,
                           filter_sections=filter_sections)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                login_user(user)
                flash(f'Welcome {user.username}', 'success')
                return redirect(url_for('home'))
            else:
                flash(f'incorrect password', 'warning')
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    active_page = 'login'
    return render_template('login.html', active_page=active_page)


@app.route("/admin/login", methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            if user.role == 'admin':
                if user.password == password:
                    login_user(user)
                    flash(f'Welcome admin {user.username}', 'success')
                    return redirect(url_for('home'))
                else:
                    return redirect(url_for('admin_login'))
            else:
                return redirect(url_for('admin_login'))
        else:
            return redirect(url_for('admin_login'))
    active_page = 'adminlogin'
    return render_template('adminlogin.html', active_page=active_page)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email, role="user",
                    password=password)
        db.session.add(user)
        db.session.commit()
        flash(f'Registered successfully', 'success')
        return redirect(url_for('login'))
    active_page = 'register'
    return render_template('register.html', active_page=active_page)


@app.route("/requests", methods=['GET', 'POST'])
def get_requests():
    all_requests = Register.query.filter_by(user_id=current_user.id).all()
    active_page = 'request'
    return render_template('requests.html', active_page=active_page, all_requests=all_requests)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
