from flask import Flask, jsonify, request
from project.common.database import db
from project.control import views

shuffle_app = Flask(__name__)
shuffle_app.config.from_object("project.config.Config")

shuffle_app.add_url_rule('/', view_func=views.testing_stage, methods = ['GET'])
shuffle_app.add_url_rule('/api/v1/event/list', view_func=views.get_all_events, methods = ['GET'])
shuffle_app.add_url_rule('/api/v1/event', view_func=views.add_new_event, methods = ['POST'])
shuffle_app.add_url_rule('/api/v1/event/<int:event_id>', view_func=views.view_single_event, methods = ['GET'])
shuffle_app.add_url_rule('/api/v1/event/<int:event_id>/vote', view_func=views.vote_event_date, methods = ['POST'])
shuffle_app.add_url_rule('/api/v1/event/<int:event_id>/results', view_func=views.determine_best_date, methods = ['GET'])

db.init_app(shuffle_app)
