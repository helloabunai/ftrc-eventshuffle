import pytest
import datetime
from flask import Flask
from project.control import models
from project.control import backend
from project.control import views
from project.common import database


@pytest.fixture(scope='module')
def test_new_event():
    """
    GIVEN:: Event model
    WHEN:: A new Event is created
    THEN:: Event.name field is set properly
    """
    test_event = models.Event(name='FlaskTestEventName')
    return test_event

@pytest.fixture(scope='module')
def test_new_date():
    """
    GIVEN:: Date model
    WHEN:: A new Date is created
    THEN:: Date.date_value field is set properly
    """
    test_date = models.Date(date_value = datetime.date(1996,2,12), parent_event=1)
    return test_date

@pytest.fixture(scope='module')
def test_new_person():
    """
    GIVEN:: Person model
    WHEN:: A new Person is created
    THEN:: Person fields are set properly
    """
    test_person = models.Person(
        name = 'TestName',
        email = 'test@email.com',
        phone_number = '+358111119999'
    )
    return test_person

#####################################################
#####################################################
## The TEST app! 
## These yield/return objects will be used in test scripts as parameters
## Allows for testing more complicated flask app functions
@pytest.fixture()
def test_app(request):
    """
    Create new application.
    Establish a context so all application parts
    are properly functioning.
    """

    test_app = Flask(__name__)
    test_app.config['TESTING'] = True
    test_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:securepassword@db:5432/futurice_shuffledb_prod'
    test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    test_app.config['SQLALCHEMY_ECHO'] = False
    test_app.config['DATABASE_URL'] = 'postgresql://postgres:securepassword@db:5432/futurice_shuffledb_prod'
    test_app.config['SQL_HOST'] = 'db'
    test_app.config['SQL_PORT'] = 5432
    test_app.config['DATABASE'] = 'futurice_shuffledb_prod'

    database.db.init_app(test_app)
    with test_app.app_context():
        backend.seed_db()

    yield test_app

#####################################################
#####################################################
## The TEST CLIENT! 
## isolate this app from the DB test app.
## Just being super careful.
app = backend.shuffle_app
@pytest.fixture
def test_client():
    test_client = app.test_client()
    return test_client