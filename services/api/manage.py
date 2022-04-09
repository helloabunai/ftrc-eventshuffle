from flask.cli import FlaskGroup
from project.app import shuffle_app
from project.control import backend

cli = FlaskGroup(shuffle_app)

@cli.command("create_db")
def create_db():
    backend.create_db()


@cli.command("seed_db")
def seed_db():
    backend.seed_db()


if __name__ == "__main__":
    cli()
