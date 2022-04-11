import datetime

from project.common import database
from project.control import models
from project.control import backend
from project.control import views

##
## Hello!
## Instantiating app via conftest.py seeds the db with backend.seed_db
## So, dummy data from there will be all that is present in the non-prod DB server
## tests will go against this information to ensure functions
##

def test_get_person(test_app):
    """
    GIVEN:: Instantiated flask app / db
    WHEN:: via ORM, ask db for the first Person entry
    THEN:: app dummy data means JOHN will be first person. Ensure valid.
    """

    with test_app.app_context():
        initial_person = database.db.session.query(models.Person).get(1)
        assert initial_person.name == 'John'

def test_get_events(test_app):
    """
    GIVEN:: Instantiated flask app / db
    WHEN:: via ORM, ask db for all Event entries
    THEN:: app dummy data means 3 events present, ensure valid.
    """

    with test_app.app_context():
        all_events = database.db.session.query(models.Event).all()
        assert len(all_events) == 3
        assert all_events[0].name == "Jake's secret party"
        assert all_events[1].name == "Bowling night"
        assert all_events[2].name == "Tabletop gaming"

def test_get_date(test_app):
    """
    GIVEN:: Instantiated flask app / db
    WHEN:: via ORM, ask db for Event 2 (Bowling night) entries
    THEN:: app dummy data == 2014-01-01; 2022-12-24; 2022-07-31; ensure valid.
    """

    with test_app.app_context():
        dates_for_event = database.db.session.query(models.Date).filter(models.Date.parent_event == 2)
        dates_serialised = [x.__dict__ for x in dates_for_event]
        formatted_dates = [x['date_value'].strftime('%Y-%m-%d') for x in dates_serialised]
        assert formatted_dates[0] == '2014-01-01'
        assert formatted_dates[1] == '2022-12-24'
        assert formatted_dates[2] == '2022-07-31'

def test_get_voters(test_app):
    """
    GIVEN:: Instantiated flask app / db
    WHEN:: via ORM, ask db for Event 1 (Jake's party) entries
    THEN:: ensure all votes are in the correct dates for this event
    """

    with test_app.app_context():
        dates_for_event = database.db.session.query(models.Date).filter(models.Date.parent_event == 1)
        dates_serialised = [x.__dict__ for x in dates_for_event]

        validated_dates = {
            '2014-01-01': {
                'vote_ids': [1,2,3,4],
                'vote_names' : ['John', 'Julia', 'Paul', 'Daisy']
            },
            '2014-01-05': {
                'vote_ids': [1,4],
                'vote_names': ['John', 'Daisy']
            },
            '2014-01-12': {
                'vote_ids': [3,4,5],
                'vote_names': ['Paul', 'Daisy', 'Dick']
            }
        }
        for curr_date in dates_serialised:
            ## we got dates, already filtered with Date.parent_event == event_id, so don't need to check event
            date_person_relations = database.db.session.query(models.PersonDate).filter(models.PersonDate.date_id == curr_date['id'])
            relations_serialised = [x.__dict__ for x in date_person_relations]
            voter_ids = [x['person_id'] for x in relations_serialised]; voter_names = []
            if voter_ids:
                voter_names = [models.Person.query.get(x).name for x in voter_ids]

            test_this_date = curr_date['date_value'].strftime('%Y-%m-%d')

            assert validated_dates[test_this_date]['vote_ids'] == voter_ids
            assert validated_dates[test_this_date]['vote_names'] == voter_names