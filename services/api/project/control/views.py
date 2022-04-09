from flask import jsonify
from project.control.models import Person

#APP.ROUTE("/")
def hello_world():
    return jsonify(hello="world")

#APP.ROUTE("/api/v1/event")
def love_you():
    test = Person.query.all()[0].as_dict()
    return jsonify(test)