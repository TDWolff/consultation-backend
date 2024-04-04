from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.Lacrossemodel import LacrosseScoreModel  # Ensure the import path matches your project structure

Lacrosse_api = Blueprint('Lacrosse_api', __name__, url_prefix='/api/Lacrosse')
api = Api(Lacrosse_api)

class Predict(Resource):
    def post(self):
        # Get the team data from the request
        data = request.get_json()
        # Get the team names from the data
        team1 = data.get('team1')
        team2 = data.get('team2')
        # Get the singleton instance of the LacrosseScoreModel
        lacrosse_model = LacrosseScoreModel.get_instance()
        # Predict the winner likelihood of the lacrosse game
        prediction = lacrosse_model.predict_winner(team1, team2)
        return jsonify(prediction)

# Add the Predict resource to the API with the /predict endpoint
api.add_resource(Predict, '/predict')