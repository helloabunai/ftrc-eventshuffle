from flask import Flask, jsonify, request
from project.common.database import db
from project.control import views

shuffle_app = Flask(__name__)
shuffle_app.config.from_object("project.config.Config")

shuffle_app.add_url_rule('/', view_func=views.hello_world)
shuffle_app.add_url_rule('/api/v1/event', view_func=views.love_you)

db.init_app(shuffle_app)
