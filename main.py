from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import *
from flask_login import LoginManager


login_manager = LoginManager()


app = Flask(__name__)
app.config.from_object(LocalDevelopmentConfig)
# initialize the app with the extension
db.init_app(app)

with app.app_context():
    db.create_all()
    lib = User.query.filter_by(username="sachin123").first()
    if not lib:
        lib = User(username="sachin123", email="sachin@gmail.com", role="admin", password='password')
        db.session.add(lib)
        db.session.commit()
login_manager.init_app(app)
app.app_context().push()


from application.routers import *


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

if __name__ == "__main__":
    app.run(debug=True)
