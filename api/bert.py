# ***///Flask API Testing Section///***

from flask import Flask, render_template, Blueprint, jsonify, request
import requests
from flask_cors import CORS
import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_restful import Api, Resource # used for REST API building
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend


import tensorflow as tf
from PIL import Image
import numpy as np
import google.generativeai as genai
import pickle
from PIL import Image
import io

from flask_restful import Api, Resource
from model.bert import process_image, generate_text, generate_text_image, label_encoder

bert = Blueprint('bert', __name__, url_prefix='/api/bert')
api = Api(bert)

with open('model/ml/label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

# Load your model
model = tf.keras.models.load_model('model/ml/cocomodel.h5')

GOOGLE_API_KEY = "AIzaSyBlvtWW_aWn7OTsuSJZXNrqJlR-QP0sqH4"
genai.configure(api_key=GOOGLE_API_KEY)

g_model = genai.GenerativeModel('gemini-1.0-pro-latest')
chat = g_model.start_chat(history=[])


class genai(Resource):
    class Gentext(Resource):
        def post(self):
            try:
                data = request.get_json()
                response_text = generate_text(data['text'])
                return {'response': response_text}, 200
            except Exception as e:
                return {'error': str(e)}, 500

    api.add_resource(Gentext, '/gen')

    class Genimage(Resource):
        def post(self):
            try:
                image_file = request.files['image'].read()
                response_text = generate_text_image(image_file)
                return {'response': response_text}, 200
            except Exception as e:
                return {'error': str(e)}, 500

    api.add_resource(Genimage, '/genimage')

