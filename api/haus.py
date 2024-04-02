import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from flask import Blueprint, request
from flask_restful import Api, Resource

haus_api = Blueprint('haus_api', __name__, url_prefix='/api/haus')
api = Api(haus_api)

class HouseAPI:
    class _CRUD(Resource):
        def post(self):
            body = request.get_json()
            square_feet = body.get("sqft")  # Corrected field name
            price = body.get("price")
            beds = body.get("beds")
            baths = body.get("baths")
            result = House(square_feet, price, beds, baths)
            return {'message': result}, 200

    api.add_resource(_CRUD, '/')

def House(sqft, price, beds, baths):
    houseData = pd.read_csv('housesdata.csv')

    newHouse = pd.DataFrame({
        'SQUARE FEET': [sqft],
        'PRICE': [price],
        'BEDS': [beds],
        'BATHS': [baths]
    })

    houseData['SQUARE FEET'] = pd.to_numeric(houseData['SQUARE FEET'], errors='coerce')
    houseData['PRICE'] = pd.to_numeric(houseData['PRICE'], errors='coerce')
    houseData['BEDS'] = pd.to_numeric(houseData['BEDS'], errors='coerce')
    houseData['BATHS'] = pd.to_numeric(houseData['BATHS'], errors='coerce')

    houseData = houseData.dropna(subset=['SQUARE FEET', 'PRICE', 'BEDS', 'BATHS'])

    scaler = StandardScaler()
    houseDataScaled = scaler.fit_transform(houseData[['SQUARE FEET', 'PRICE', 'BEDS', 'BATHS']])
    newHouseScaled = scaler.transform(newHouse)

    distances = np.sqrt(np.sum((houseDataScaled - newHouseScaled)**2, axis=1))
    top3_indices = np.argsort(distances)[:3]
    top3_distances = distances[top3_indices]

    mostSimilar = []
    max_distance = np.max(distances)
    for i in range(3):
        address = houseData.iloc[top3_indices[i]]['ADDRESS']
        closeness = 1 - (top3_distances[i] / max_distance)
        if np.isnan(closeness):
            probability = None
        else:
            probability = closeness  # Using closeness as probability
        mostSimilar.append({'address': address, 'probability': probability})

    return mostSimilar
