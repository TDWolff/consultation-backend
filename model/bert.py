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

def bertinit(self):
    return("BERT API Initialized")

with open('model/ml/label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)
# Load your model
model = tf.keras.models.load_model('model/ml/cocomodel.h5')

GOOGLE_API_KEY = "AIzaSyBlvtWW_aWn7OTsuSJZXNrqJlR-QP0sqH4"
genai.configure(api_key=GOOGLE_API_KEY)

g_model = genai.GenerativeModel('gemini-1.0-pro-latest')
chat = g_model.start_chat(history=[])

def process_image(image_file):
    image = Image.open(io.BytesIO(image_file)).convert('RGB')  # ensure the image has 3 channels
    image = image.resize((64, 64))
    image = np.array(image) / 255.0  # normalize the RGB values
    image = np.expand_dims(image, axis=0)  # add an extra dimension for batch size
    prediction = model.predict(image)
    label_index = np.argmax(prediction)
    label = label_encoder.inverse_transform([label_index])
    return label[0]

def generate_text_image(image_file):
    try:
        object_label = process_image(image_file)
        response = chat.send_message(f"In one short, response, what is this an image of? {object_label}. Respond like so, This is a picture of a input_object here.",
                                     safety_settings={'HARASSMENT':'block_none'})
        return response.text
    except Exception as e:
        return f"An Error Occurred in Image Text Gen"

def generate_text(input_text):
    try:
        response = chat.send_message("In one brief sentence, " + input_text, safety_settings={'HARASSMENT':'block_none', 'HATE_SPEECH':'block_none'})
        return response.text
    except Exception as e:
        return f"I can't provide information about this topic, lets move on and start a new conversation."
