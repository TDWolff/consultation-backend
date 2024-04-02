from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource

# Import the FootballScoreModel class
from model.NFLmodel import FootballScoreModel

NFL_api = Blueprint('NFL_api', __name__, url_prefix='/api/NFL')
api = Api(NFL_api)

class Predict(Resource):
    def post(self):
        # Get the team data from the request
        data = request.get_json()

        # Get the team names from the data
        team1 = data.get('team1')
        team2 = data.get('team2')

        # Get the singleton instance of the FootballScoreModel
        football_model = FootballScoreModel.get_instance()

        # Predict the winner of the football game
        likelihood = football_model.predict_winner_likelihood(team1, team2)

        return jsonify(likelihood)

# Add the Predict resource to the API with the /predict endpoint
api.add_resource(Predict, '/predict')
