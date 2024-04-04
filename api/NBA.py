from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.NBAmodel import BasketBallScoreModel  # Import the NBA model class

NBA_api = Blueprint('NBA_api', __name__, url_prefix='/api/NBA')
api = Api(NBA_api)

class Predict(Resource):
    def post(self):
        # Get the team data from the request
        data = request.get_json()

        # Get the team IDs from the data
        team1_id = data.get('team1_id')
        team2_id = data.get('team2_id')

        # Get the singleton instance of the BasketBallScoreModel (adapted for NBA)
        basketball_model = BasketBallScoreModel.get_instance()

        # Predict the winner likelihood of the NBA game
        likelihood = basketball_model.predict_winner_likelihood(team1_id, team2_id)

        return jsonify(likelihood)

# Add the Predict resource to the API with the /predict endpoint
api.add_resource(Predict, '/predict')