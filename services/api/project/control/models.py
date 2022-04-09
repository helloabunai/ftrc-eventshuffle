from dataclasses import dataclass
from sqlalchemy import ForeignKey
from project.common.database import db

@dataclass
class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    event_name = db.Column(db.String(128), nullable=False)
    event_date = db.Column(db.Integer, ForeignKey('dates.id'))

    def __init__(self, event_name):
        self.event_name = event_name

@dataclass
class Date(db.Model):
    __tablename__ = "dates"

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    date_value = db.Column(db.Date, nullable=False)
    voters = db.Column(db.Integer, ForeignKey('person.id'))

    def __init__(self, date_value):
        self.date_value = date_value

@dataclass
class Person(db.Model):
    __tablename__ = "person"

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    phone_number = db.Column(db.String(30), unique=True)

    def __init__(self, name, email, phone_number):
        self.name = name
        self.email = email
        self.phone_number = phone_number
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

