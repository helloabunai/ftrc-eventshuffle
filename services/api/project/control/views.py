from flask import jsonify, request, abort
from project.control.models import Event, Date, Person

#APP.ROUTE("/")
def testing_stage():
    
    """
    Bad sense of humour
    """
    return jsonify(SendJobOffersTo="my email address")

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
        raw_psql_response = [x.as_dict() for x in all_events]
        filtered_data = [{ k: v for k,v in x.items() if k in ['id', 'name']} for x in raw_psql_response]
        return jsonify(events=filtered_data), 200

def add_new_event():

    """
    @app.route("/api/v1/event/")
    :param: None
    :request: POST
    :return: int Event.id
    """

    print(request)
    ## TODO take name, make Event of that name
    ## TODO take dates, create Date object
    ## TODO interface Event entry <- to -> Date object(S)
    ## TODO get the new Event's ID, return to 'frontend'

    return jsonify(request.get_json(force=True))

def view_single_event(event_id):

    """
    @app.route("/api/v1/event/<int:id>")
    :param: int Event.id
    :request: GET
    :return: JSON Serialised PSQL ORM Object
    """

    requested_object = Event.query.get(event_id)
    if not requested_object:
        return abort(404)
    else:
        serialised_data = requested_object.as_dict()
        ## TODO proper data required (fix database tables)
        return jsonify(serialised_data), 200

def vote_event_date(event_id):

    """
    @app.route("/api/v1/event/<int:id>/vote")
    :param: int Event.id
    :request: POST
    :return: todo
    """

    requested_object = Event.query.get(event_id)
    if not requested_object:
        return abort(404)
    else:
        return jsonify(request.get_json(force=True))

def determine_best_date(event_id):

    """
    @app.route("/api/v1/even/<int:id>/results")
    :param: int Event.id
    :request: GET
    :return: JSON Serialised PSQL ORM Object
    :return: Calculated date(s) suitable for all people at Event.id
    """

    return jsonify(best="date")


