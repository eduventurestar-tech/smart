from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from passlib.hash import bcrypt
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    theme = db.Column(db.String(10), default='light')

    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)  # YYYY-MM-DD
    number = db.Column(db.String(50), nullable=False)
    client_name = db.Column(db.String(120), nullable=False)
    client_email = db.Column(db.String(120))
    amount = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(20), default='Draft')
    currency = db.Column(db.String(10), default='USD')
    notes = db.Column(db.String(255), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    method = db.Column(db.String(50), default='Cash')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    currency = db.Column(db.String(10), default='USD')
    tax = db.Column(db.Float, default=0.0)