from flask import Blueprint, request, jsonify
from model.Medicals import MedicalModel
from flask_restful import Api, Resource
medical_api = Blueprint('medical_api', __name__, url_prefix='/api/medical')
medical_model = MedicalModel('model/medical_students_dataset.csv')
api = Api(medical_api)
@medical_api.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the data from the request's body
        student_info = request.json
        # Make prediction using the Medical model
        prediction = medical_model.predict(student_info)
        # Return the prediction as JSON response
        return jsonify({'prediction': prediction})
    except Exception as e:
        # Return error message if prediction fails
        return jsonify({'error': str(e)})
class MedicalAPI(Resource):
    def post(self):
        try:
            # Get the data from the request's body
            student_info = request.json
            # Make prediction using the Medical model
            prediction = medical_model.predict(student_info)
            # Return the prediction as JSON response
            return jsonify({'prediction': prediction})
        except Exception as e:
            # Return error message if prediction fails
            return jsonify({'error': str(e)})
# Add resource to the API
api.add_resource(MedicalAPI, '/predict')