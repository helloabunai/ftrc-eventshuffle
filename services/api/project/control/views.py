from project.common.validator import schema
from flask import jsonify, request, abort, Blueprint

from project.control.models import Event, Date, Person
from project.control.backend import shuffle_app as app
from project.common.database import db

from project.control.backend import handle_new_event
from project.control.backend import get_event_subsidiaries
from project.control.backend import add_event_votes
from project.control.backend import calculate_best_date

#######################################################
#######################################################

@app.route('/', methods=['GET'])
def testing_stage():
    
    """
    haha
    """

    return jsonify(URLNotInUse="JustSayingHi"), 200, {'Content-Type': 'application/json'}

#######################################################
#######################################################

@app.route('/api/v1/event/list', methods=['GET'])
def get_all_events():

    """
    @app.route("/api/v1/event/list")
    :param: None
    :request: GET
    :return: JSON Serialised PSQL ORM Objects
    """

    all_events = Event.query.all()

    if not all_events:
        return abort(404)
    else:
        raw_psql_response = [x.__dict__ for x in all_events]
        filtered_data = [{ k: v for k,v in x.items() if k in ['id', 'name']} for x in raw_psql_response]
        return jsonify(events=filtered_data), 200, {'Content-Type': 'application/json'}

#######################################################
#######################################################

@app.route('/api/v1/event', methods=['POST'])
@schema('event.json')
def add_new_event():

    """
    @app.route("/api/v1/event")
    :param: None
    :request: POST
    :return: int Event.id
    """

    reponse = handle_new_event(request.json)
    return jsonify(reponse), 200, {'Content-Type': 'application/json'}

#######################################################
#######################################################

@app.route('/api/v1/event/<int:event_id>', methods=['GET'])
def view_single_event(event_id):

    """
    @app.route("/api/v1/event/<int:event_id>")
    :param: int Event.id
    :request: GET
    :return: JSON Serialised PSQL ORM Object
    """

    requested_object = Event.query.get(event_id)
    if not requested_object:
        return abort(404)
    else:
        parsed_data = get_event_subsidiaries(event_id)
        return parsed_data, 200, {'Content-Type': 'application/json'}

#######################################################
#######################################################

@app.route('/api/v1/event/<int:event_id>/vote', methods=['POST'])
@schema('event_vote.json')
def vote_event_date(event_id):

    """
    @app.route("/api/v1/event/<int:event_id>/vote")
    :param: int Event.id
    :request: POST
    :return: todo
    """

    request_json = request.json
    requested_object = Event.query.get(event_id)
    if not requested_object:
        return abort(404)
    else:
        processed_vote = add_event_votes(event_id, request_json)
        return processed_vote, 200, {'Content-Type': 'application/json'}

#######################################################
#######################################################

@app.route("/api/v1/event/<int:event_id>/results", methods=['GET'])
def determine_best_date(event_id):

    """
    @app.route("/api/v1/event/<int:id>/results")
    :param: int Event.id
    :request: GET
    :return: JSON Serialised PSQL ORM Object
    :return: Calculated date(s) suitable for all people at Event.id
    """

    requested_object = Event.query.get(event_id)
    if not requested_object:
        return abort(404)
    else:
        parsed_data = calculate_best_date(event_id) 
        return parsed_data, 200, {'Content-Type': 'application/json'}


