from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password_hash = db.Column(db.String)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    