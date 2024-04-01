from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask import Blueprint
import pandas as pd
import joblib

Medical_api = Blueprint('Medical_api', __name__, url_prefix='/api/Medical/predict')
api = Api(Medical_api)

app = Flask(__name__)
api = Api(app)

class MedicalAPI(Resource):
    def __init__(self):
        self.model = joblib.load('medical_model.pkl')
        self.encoder = joblib.load('encoder.pkl')

    def predict_outcome(self, data):
        data_df = pd.DataFrame([data])
        data_encoded = self.encoder.transform(data_df.select_dtypes(include=['object']))
        data_df = pd.concat([data_df.select_dtypes(exclude=['object']), pd.DataFrame(data_encoded.toarray(), columns=self.encoder.get_feature_names_out())], axis=1)

        prediction = self.model.predict(data_df)[0]
        probability = self.model.predict_proba(data_df)[0][1]  # Probability of class 1
        return {'prediction': int(prediction), 'probability': f'{probability:.2%}'}

    def post(self):
        try:
            data = request.json
            result = self.predict_outcome(data)
            return jsonify(result)
        except Exception as e:
            return {'error': str(e)}

api.add_resource(MedicalAPI, '/predict')

if __name__ == '__main__':
    app.run(debug=True)
