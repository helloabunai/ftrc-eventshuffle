import random
import datetime

from project.common import database
from project.control import models
from project.control import views

def test_root_endpoint(test_client):
    """
    GIVEN:: Instantiated flask app / db
    WHEN:: we send a GET to endpoint /
    THEN:: should get innocent reply back + 200
    """
   
    response = test_client.get(
        '/',
        headers = {'Content-Type': 'application/json'}
    )

    validated_response = {
        'URLNotInUse': 'JustSayingHi'
    }

    response_info = response.json
    assert response_info['URLNotInUse'] == 'JustSayingHi'
    assert response.status_code == 200
    
def test_allevent_endpoint(test_client):
    """
    GIVEN:: Instantiated flask app / db
    WHEN:: we send a GET to endpoint /api/v1/events/list
    THEN:: should get all events back + 200
    """

    response = test_client.get(
        '/api/v1/event/list',
        headers = {'Content-Type': 'application/json'}
    )

    assert len(response.json['events']) == 3
    assert response.status_code == 200

def test_create_event(test_client):
    """
    GIVEN:: Instantiated flask app / db
    WHEN:: we send a JSON payload via POST
    THEN:: create new event, get ID, get response body confirmation + 200
    """ 

    payload = {
        "name": "Jake's other secret party",
        "dates": [
            "2014-11-01",
            "2014-11-05",
            "2014-11-12"
        ]
    }

    response = test_client.post(
        '/api/v1/event',
        json = payload
    )

    assert 'id' in response.json.keys()
    assert response.json['id'] > 3 ## db-seed only creates 3 events
    assert response.json['id'] == 4 ## so this new test one should == 4
    assert response.status_code == 200

def test_single_detailed_event(test_client):
    """
    GIVEN:: Instantiated flask app / db
    WHEN:: GET request to specific event ID <integer> (BigInteger i.e. long)
    THEN:: get all event info + all relational event info/votes + 200
    """    

    ## choose a random event from the 3 events
    ## that are added by seed_db
    random_choice = random.choice([1,2,3])
    response = test_client.get(
        '/api/v1/event/{}'.format(random_choice)
    )

    assert response.status_code == 200
    if random_choice == 1:
        assert response.json['name'] == "Jake's secret party"
        assert response.json['id'] == 1
        assert len(response.json['dates']) == 3
        assert len(response.json['votes']) == 3

    if random_choice == 2:
        assert response.json['name'] == "Bowling night"
        assert response.json['id'] == 2
        assert len(response.json['dates']) == 3
        assert len(response.json['votes']) == 2

    if random_choice == 3:
        assert response.json['name'] == 'Tabletop gaming'
        assert response.json['id'] == 3
        assert len(response.json['dates']) == 2
        assert len(response.json['votes']) == 1
        
def test_event_vote(test_client):
    """
    GIVEN:: Instantiated flask app / db
    WHEN:: we send a JSON payload via POST
    THEN:: create new event, get ID, get response body confirmation + 200

    NOTE !! This test is launched BEFORE test_get_result()
    NOTE !! As the test suite wipes the database and re-seeds with dummy data
    NOTE !! There will not be, for Event 1, a date with all people available
    NOTE !! Until Dick votes for the votes below
    """ 

    payload = {
        "name": "Dick",
        "votes": [
            '2014-01-01',
            '2014-01-05'
        ]
    }

    response = test_client.post(
        '/api/v1/event/1/vote',
        json = payload
    )

    assert response.status_code == 200
    ## check dick (i really want to change this name in all references) is added to:
    ## first date they voted for, 2014-01-01
    first_date = [{k: v for k, v in x.items() if x['date'] == '2014-01-01'} for x in response.json['votes']]
    first_date_pop = list(filter(None,first_date))[0] ## remove empty dicts
    assert 'Dick' in first_date_pop['people']
   
    ## second date they voted for, 2014-01-05
    second_date = [{k: v for k, v in x.items() if x['date'] == '2014-01-05'} for x in response.json['votes']]
    second_date_pop = list(filter(None,second_date))[0] ## remove empty dicts
    assert 'Dick' in second_date_pop['people']

def test_get_result(test_client):
    """
    GIVEN:: Instantiated flask app / db
    WHEN:: we send a GET request with <integer> (BigInteger i.e. long)
    THEN:: create new event, get ID, get response body confirmation + 200

    NOTE !! As per note in test_event_vote(), this must be called after test_event_vote
    NOTE !! otherwise, event 1 will not have a date that is suitable for all people attending
    NOTE !! this highlights the function works as intended and is fault tolerant
    """ 

    ## choose event 1, as that is the event which will, from seed data
    ## end up producing a "suitableDates" for all people at event 1.
    response = test_client.get(
        '/api/v1/event/1/results'
    )

    assert response.status_code == 200
    ## check that event 1 has a suitableDates entry
    suitable_dates = response.json['suitableDates']
    assert len(suitable_dates) > 0
    ## check that the date is 2014-01-01 and 5 people are present
    assert suitable_dates[0]['date'] == '2014-01-01'
    assert len(suitable_dates[0]['people']) == 5

def test_invalid_event_fails(test_client):
    """
    GIVEN:: Instantiated flask app / db
    WHEN:: send a POST to add votes to an event.
    THEN:: handle non-unique constraint error

    NOTE !! Testing for an event that does not exist in DB
    NOTE !! attempt to access event by ID that doesnt exist
    NOTE !! then assert for that error
    """   

    response = test_client.get(
        '/api/v1/event/x12a88'
    )

    assert response.status_code == 404

def test_invalid_vote_fails(test_client):
    """
    GIVEN:: Instantiated flask app / db
    WHEN:: send a POST to add votes to an event.
    THEN:: handle non-unique constraint error

    NOTE !! Testing for a name that does not exist in the DB
    NOTE !! Since names were given as the only identifier for adding votes
    NOTE !! names (and not people.id) need to be unique...
    NOTE !! so if someone tries to add a vote with a Person.name that does not exist
    NOTE !! then assert for that error
    """   

    payload = {
        "name": "Sean",
        "votes": [
            '2014-01-01',
            '2014-01-05'
        ]
    }

    response = test_client.post(
        '/api/v1/event/1/vote',
        json = payload
    )

    assert response.status_code == 500

def test_invalid_event_vote_fails(test_client):
    """
    GIVEN:: Instantiated flask app / db
    WHEN:: send a POST to add votes to an event.
    THEN:: handle non-unique constraint error

    NOTE !! Testing for adding a vote to an event that does not exist
    NOTE !! so if someone tries to add a vote with an Event.id that does not exist
    NOTE !! then assert for that error
    """   

    payload = {
        "name": "Dick",
        "votes": [
            '2014-01-01',
            '2014-01-05'
        ]
    }

    response = test_client.post(
        '/api/v1/event/x12a88/vote',
        json = payload
    )

    assert response.status_code == 404  

def test_double_vote_fails(test_client):
    """
    GIVEN:: Instantiated flask app / db
    WHEN:: send a POST to add votes to an event.
    THEN:: handle non-unique constraint error

    NOTE !! VOTE (PersonDate) SHOULD ALREADY EXIST
    NOTE !! we are asserting for an ERROR here to ensure
    NOTE !! the database PersonDate unique vote property is upheld
    """ 
    
    payload = {
        "name": "Dick",
        "votes": [
            '2014-01-01',
            '2014-01-05'
        ]
    }

    response = test_client.post(
        '/api/v1/event/1/vote',
        json = payload
    )

    ## CHECK THAT 409 CONFLICT WAS RAISED
    assert response.status_code == 409
    
def test_missingevent_result_fails(test_client):
    """
    GIVEN:: Instantiated flask app / db
    WHEN:: we send a GET request with <integer> (BigInteger i.e. long)
    THEN:: create new event, get ID, get response body confirmation + 200

    NOTE !! As per note in test_event_vote(), this must be called after test_event_vote
    NOTE !! otherwise, event 1 will not have a date that is suitable for all people attending
    NOTE !! this highlights the function works as intended and is fault tolerant
    """ 

    ## choose event 1, as that is the event which will, from seed data
    ## end up producing a "suitableDates" for all people at event 1.
    response = test_client.get(
        '/api/v1/event/x12a88/results'
    )

    assert response.status_code == 404
