import datetime
from project.common.database import db
from project.control.models import Event, Date, Person

def create_db():
    db.drop_all() #remove after dev
    db.create_all()
    db.session.commit()

def seed_db():

    ## TODO -- Take from a JSON file

    create_db() ## remove after dev

    people_to_add = [
        Person(name = "John", email="john@email.com", phone_number='+358453250000'),
        Person(name = "Julia", email="julia@email.com", phone_number='+358453250001'),
        Person(name = "Paul", email="paul@email.com", phone_number='+358453250002'),
        Person(name = "Daisy", email="daisy@email.com", phone_number='+358453250003'),
        Person(name = "Dick", email="dick@email.com", phone_number='+358453250004')
    ]
    db.session.bulk_save_objects(people_to_add)

    dates_to_add = [
        Date(date_value = datetime.date(2014, 1, 1)),
        Date(date_value = datetime.date(2014, 1, 5)),
        Date(date_value = datetime.date(2014, 1 , 12))
    ]
    db.session.bulk_save_objects(dates_to_add)

    events_to_add = [
        Event(name = "Jake's secret party"),
        Event(name = "Bowling night"),
        Event(name = "Tabletop gaming")
    ]
    db.session.bulk_save_objects(events_to_add)

    db.session.commit()
