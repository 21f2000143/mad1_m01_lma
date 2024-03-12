from flask import render_template, url_for
from flask import redirect, request
from flask import current_app as app
from application.database import db
from application.models import User
from flask_login import login_user, logout_user
from flask_login import login_required


@app.route("/")
def home():
    active_page = 'home'
    return render_template('index.html', active_page=active_page)


@app.route("/sections")
@login_required
def sections():
    active_page = 'sections'
    return render_template('sections.html', active_page=active_page)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                login_user(user)
                return redirect(url_for('home'))
            else:
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
            if user.password == password:
                login_user(user)
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    active_page = 'login'
    return render_template('adminlogin.html', active_page=active_page)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']
        user = User(username=username, email=email, role=role,
                    password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    active_page = 'register'
    return render_template('register.html', active_page=active_page)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))