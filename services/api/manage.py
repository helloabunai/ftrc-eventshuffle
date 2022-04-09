from flask.cli import FlaskGroup

from project.app import shuffle_app
from project.common.database import db
from project.control.models import Event, Date, Person

cli = FlaskGroup(shuffle_app)

@cli.command("create_db")
def create_db():
    db.drop_all() #remove after development
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(
        Person(
        name="joe bloggs",
        email="joe@bloggs.com",
        phone_number="+358453259999",
        )
    )
    db.session.commit()


if __name__ == "__main__":
    cli()
