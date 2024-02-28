from flask import Flask, render_template, Blueprint, jsonify, request
import requests
from flask_cors import CORS
import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
import sqlite3
from __init__ import app, db, cors, dbURI
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend
from matplotlib import pyplot as plt
from io import BytesIO
import base64
import _sqlite3
from __init__ import db
from sqlalchemy.exc import IntegrityError

from model.users import Stocks,User,Stock_Transactions

search_api = Blueprint('search_api', __name__,
                   url_prefix='/api/stock')
api = Api(search_api)

class MissingStock(Resource):
    _tablename_ = 'stocks'
    
    id = db.Column(db.Integer, primary_key=True)

    _symbol = db.Column(db.String(255), nullable=False)
    _company = db.Column(db.String(255), nullable=False)
    _quantity = db.Column(db.Integer, nullable=False)
    _sheesh = db.Column(db.Integer, nullable=False)

    def __init__(self, symbol, company, quantity, sheesh):
        self._symbol = symbol
        self._company = company
        self._quantity = quantity
        self._sheesh = sheesh

    @property
    def symbol(self):
        return self._symbol
    
    @property
    def company(self):
        return self._company
    
    @property
    def quantity(self):
        return self._quantity
    
    @property
    def sheesh(self):
        return self._sheesh
    
    @symbol.setter
    def symbol(self, symbol):
        self._symbol = symbol

    @company.setter
    def company(self, company):
        self._company = company
    
    @quantity.setter
    def quantity(self, quantity):
        self._quantity = quantity
    
    @sheesh.setter
    def sheesh(self, sheesh):
        self._sheesh = sheesh


    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None
            
     # CRUD update: updates user name, password, phone
    # returns self
    def update(self, symbol, company, quantity, sheesh):
        # Check if value is blank and replace with defaults
        if symbol != "":
            self._symbol = symbol
        if company != "":
            self._company = company
        if quantity != "":
            self._quantity = quantity
        if sheesh != "":
            self._sheesh = sheesh
        db.session.commit()
        return self


class SearchAPI(Resource):
    def __init__(self, name, import_name, **kwargs):
        super().__init__(name, import_name, **kwargs)

        self.route('/search', methods=['POST'])(self.search_stock)


    class stock(Resource):
        def put(self):
            try:
                body = request.get_json()
                symbol = body.get('symbol')
                company = body.get('company')
                quantity = body.get('quantity')
                sheesh = body.get('sheesh')
                stocks = Stocks.query.all()
                for stock in stocks:
                    if stock.symbol == symbol:
                        stock.update(company = company if company else "", quantity = quantity if quantity else "", sheesh = sheesh if sheesh else "")
                        return f"Updated {symbol}"
                return f"Stock not found"
            except Exception as e:
                return jsonify('Error Occured'),500
    
    class search_stock(Resource):
        def post(self):
            try: 
                data = request.get_json()
                symbol = data['symbol']

                # Make a request to the FMP API to get stock information
                api_key = '034ce1b9ccc7ac857fc59ec5665cfc5e'  # Replace with your FMP API key
                url = f'https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={api_key}'
                response = requests.get(url)
                stock_data = response.json()

                # if response.status_code != 200:
                #     return {'error': 'Error Occured'}
                
                stock_info = {
                    'symbol': stock_data[0]['symbol'],
                    'name': stock_data[0]['name'],
                    'price': stock_data[0]['price'],
                    'changesPercentage': stock_data[0]['changesPercentage'],
                    'change': stock_data[0]['change'],
                    'dayLow': stock_data[0]['dayLow'],
                    'dayHigh': stock_data[0]['dayHigh'],
                    'yearHigh': stock_data[0]['yearHigh'],
                    'yearLow': stock_data[0]['yearLow'],
                    'marketCap': stock_data[0]['marketCap'],
                    'priceAvg50': stock_data[0]['priceAvg50'],
                    'priceAvg200': stock_data[0]['priceAvg200'],
                    'volume': stock_data[0]['volume'],
                    'avgVolume': stock_data[0]['avgVolume'],
                    'exchange': stock_data[0]['exchange'],
                    'open': stock_data[0]['open'],
                    'previousClose': stock_data[0]['previousClose'],
                    'eps': stock_data[0]['eps'],
                    'pe': stock_data[0]['pe'],
                    'earningsAnnouncement': stock_data[0]['earningsAnnouncement'],
                    'sharesOutstanding': stock_data[0]['sharesOutstanding'],
                    'timestamp': stock_data[0]['timestamp']
                }

                print(stock_info)

                return jsonify(stock_info)
            except Exception as e:
                return jsonify('Error Occured')
            
    api.add_resource(search_stock, '/search')

    class HistoricalData(Resource):
        def post(self):
            try: 
                data = request.get_json()
                symbol = data['symbol']

                # Make a request to the FMP API to get historical data
                api_key = '034ce1b9ccc7ac857fc59ec5665cfc5e'  # Replace with your FMP API key
                url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={api_key}'
                response = requests.get(url)
                historical_data = response.json()

                # Extract the dates and prices from the historical data
                dates = [item['date'] for item in historical_data['historical']]
                prices = [item['close'] for item in historical_data['historical']]

                # Create a plot
                plt.figure(figsize=(10,5))
                plt.plot(dates, prices)
                plt.title(f'Historical Data for {symbol}')
                plt.xlabel('Date')
                plt.ylabel('Close Price')
                plt.grid(True)
                plt.tight_layout()

                # Save it to a BytesIO object
                buf = BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)

                # Convert plot to a base64 string
                image_base64 = base64.b64encode(buf.read()).decode('utf-8')
                buf.close()

                print(image_base64)

                return jsonify({'image': image_base64})
            except Exception as e:
                return jsonify('Error Occured')

    api.add_resource(HistoricalData, '/historical')    