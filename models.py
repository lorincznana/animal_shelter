from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

db = SQLAlchemy()

from flask_login import UserMixin

class Animal(db.Model):
    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    species = db.Column(db.String(50))
    breed = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.Enum('hím', 'kan', 'nőstény', 'szuka', name='gender_enum'))
    description = db.Column(db.String(500))
    image_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    medical_records = db.relationship('MedicalRecord', backref='animal', lazy=True)
    gallery = db.relationship('Gallery', backref='animal', lazy=True)

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'))
    vaccine = db.Column(db.String(100))
    vaccine_date = db.Column(db.Date)
    disease = db.Column(db.String(100))
    treatment = db.Column(db.String(200))
    vet_name = db.Column(db.String(100))
    updated_at = db.Column(db.DateTime)

class Gallery(db.Model):
    __tablename__ = 'gallery'
    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'))
    image_url = db.Column(db.String(200))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(200))
    role = db.Column(db.Enum('admin', 'staff', 'volunteer', 'user', name='user_roles'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ShelterInfo(db.Model):
    __tablename__ = 'shelter_info'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(100))
    description = db.Column(db.String(500))
    donation_text = db.Column(db.String(500))
    donation_account = db.Column(db.String(100))