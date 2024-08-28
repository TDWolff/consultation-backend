from flask import Blueprint, app, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from __init__ import app

consultation_api = Blueprint('consultation_api', __name__,
                   url_prefix='/consultation')

api = Api(consultation_api)

class Consultation(Resource):
    class Consultation_Server(Resource):
        def post(self):
            return jsonify({"message": "Consultation server connection established"})

    api.add_resource(Consultation_Server, '/connect')