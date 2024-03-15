from flask import render_template, url_for, flash
from flask import redirect
from flask import current_app as app
from application.database import db
from application.models import Register
from flask_login import login_required
import datetime


@app.route("/admin/requests", methods=['GET', 'POST'])
def get_all_requests():
    all_requests = Register.query.all()
    active_page = 'request'
    return render_template('requests.html', active_page=active_page,
                           all_requests=all_requests)


@app.route('/reject/book/<int:id>')
@login_required
def reject_book(id):
    # Query the database for the register entry with the given ID
    register = Register.query.filter_by(id=id).first()

    if register:
        # Update the request status to 'rejected'
        register.status = 'rejected'
        db.session.commit()
        flash("Book rejected successfully", category='success')
        return redirect(url_for(''))

    flash("Request not found", category='error')
    return redirect(url_for('get_all_requests'))


@app.route('/grant/book/<int:id>')
@login_required
def grant_book(id):
    # Query the database for the register entry with the given ID
    register = Register.query.filter_by(id=id).first()

    # Checking the number of issued books
    num_registers = Register.query.filter(
        Register.user_id == register.user_id,
        Register.status == 'granted').count()
    if num_registers > 5:
        flash("Already issued 5 books", category='danger')
        return redirect(url_for('get_all_requests'))

    if register:
        # Update the request status to 'granted' and record the issuance date
        register.status = 'granted'
        register.approve_date = datetime.datetime.now().strftime("%Y-%m-%d")
        db.session.commit()
        flash("Book granted successfully", category='success')
        return redirect(url_for('get_all_requests'))

    flash("Request not found", category='error')
    return redirect(url_for('get_all_requests'))


@app.route('/revoke/book/<int:id>')
@login_required
def revoke_book(id):
    # Query the database for the register entry with the given ID
    register = Register.query.filter_by(id=id).first()

    if register:
        # Update the request status to 'revoked'
        register.status = 'revoked'
        db.session.commit()
        flash("Book revoked successfully", category='success')
        return redirect(url_for('get_all_requests'))

    flash("Request not found", category='error')
    return redirect(url_for('get_all_requests'))
