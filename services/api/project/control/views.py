from flask import jsonify, request
from project.control.models import Event, Date, Person

#APP.ROUTE("/")
def testing_stage():
    all_events = Event.query.all()
    temp = [x.as_dict() for x in all_events]

    return jsonify(temp)











#APP.ROUTE("/api/v1/event/list")
def get_all_events():
    return jsonify(getall="events")

#APP.ROUTE("/api/v1/event")
def add_new_event():
    return request, 200

#APP.ROUTE("/api/v1/event/<id>")
def view_single_event():
    # request.args.id
    return jsonify(getone="single_event")

#APP.ROUTE("/api/v1/event/<id>/vote")
def vote_event_date():
    return request, 200

#APP.ROUTE("/api/v1/event/<id>/results")
def determine_best_date():
    return jsonify(best="date")


