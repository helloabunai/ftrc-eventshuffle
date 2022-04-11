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
    WHEN:: GET request to specific event ID <integer>
    THEN:: get all event info + all relational event info/votes + 200
    """    

    ## choose a random event from the 3 events
    ## that are added by seed_db
    random_choice = random.choice([1,2,3])
    response = test_client.get(
        '/api/v1/event/{}'.format(random_choice)
    )

    if random_choice == 1:
        assert response.json['name'] == "Jake's secret party"
        assert response.json['id'] == 1
        assert len(response.json['dates']) == 3
        assert len(response.json['votes']) == 3
        assert response.status_code == 200

    if random_choice == 2:
        assert response.json['name'] == "Bowling night"
        assert response.json['id'] == 2
        assert len(response.json['dates']) == 3
        assert len(response.json['votes']) == 2
        assert response.status_code == 200

    if random_choice == 3:
        assert response.json['name'] == 'Tabletop gaming'
        assert response.json['id'] == 3
        assert len(response.json['dates']) == 2
        assert len(response.json['votes']) == 1
        assert response.status_code == 200

def test_event_vote(test_client):
    """
    GIVEN:: Instantiated flask app / db
    WHEN:: we send a JSON payload via POST
    THEN:: create new event, get ID, get response body confirmation + 200
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

    print(response.json)

    