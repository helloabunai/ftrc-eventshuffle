from dataclasses import dataclass
from sqlalchemy import ForeignKey, UniqueConstraint
from project.common.database import db
from sqlalchemy.orm import relationship

@dataclass
class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    
    def __init__(self, name):
        self.name = name

@dataclass
class Date(db.Model):
    __tablename__ = "dates"
    ## ensures that DATE_VALUE is unique ONLY FOR each PARENT_EVENT
    ## i.e. multiple events can have the same date value
    ## but ONE INDIVIDUAL event cannot have the same date more than once
    __table_args__ = (UniqueConstraint('date_value', 'parent_event', name='_datevalue_parentevent_uc'),)

    id = db.Column(db.BigInteger, primary_key=True)
    date_value = db.Column(db.Date, nullable=False)
    parent_event = db.Column(db.Integer, ForeignKey('events.id'), nullable=True)

    def __init__(self, date_value, parent_event):
        self.date_value = date_value,
        self.parent_event = parent_event

@dataclass
class PersonDate(db.Model):
    __tablename__ = "people_dates"
    ## ensures that DATE_ID is unique ONLY FOR each PERSON_ID
    ## i.e. for ONE event, ONE person cannot vote for the same date multiple times
    __table_args__ = (UniqueConstraint('date_id', 'person_id', name='_datevalue_personvalue_uc'),)

    id = db.Column(db.BigInteger, primary_key=True)
    date_id = db.Column(db.BigInteger, ForeignKey('dates.id'))
    person_id = db.Column(db.BigInteger, ForeignKey('people.id'))

    def __init__(self, date_id, person_id):
        self.date_id = date_id
        self.person_id = person_id

@dataclass
class Person(db.Model):
    __tablename__ = "people"

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    phone_number = db.Column(db.String(30), unique=True, nullable=True)

    def __init__(self, name, email, phone_number):
        self.name = name
        self.email = email
        self.phone_number = phone_number
    
    def __str__(self):
        return f"Person: {self.name}"


