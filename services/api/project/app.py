from flask import Flask, jsonify, request
from project.common.database import db
from project.control.backend import shuffle_app
from project.control import views

"""
Todo write docstring
"""
 
db.init_app(shuffle_app)
