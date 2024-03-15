from flask import render_template, url_for
from flask import redirect, request
from flask import current_app as app
from application.database import db
from application.models import User, Section
from flask_login import login_user, logout_user
from flask_login import login_required


@app.route("/section", methods=['GET', 'POST'])
@login_required
def add_section():
    if request.method == 'POST':
        title = request.form['title']
        section = Section(title=title)
        db.session.add(section)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('section.html')
