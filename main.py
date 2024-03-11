from flask import Flask, render_template
from config import LocalDevelopmentConfig
from database import db
from models import User

app = Flask(__name__)
app.config.from_object(LocalDevelopmentConfig)
# initialize the app with the extension
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/my/first/app")
def my_first_app():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)