import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
import seaborn as sb
from flask import Blueprint, request
from flask_restful import Api, Resource


titanic_api = Blueprint('titanic_api', __name__,
                   url_prefix='/api/titanic')
api = Api(titanic_api)

class TitanicAPI:     
    class _CRUD(Resource):
        def post(self):
            body = request.get_json()
            name = body.get("name")
            pclass = body.get("pclass")
            sex = body.get("sex")
            age = body.get("age")
            sibsp = body.get("sibsp")
            parch = body.get("parch")
            fare = body.get("fare")
            embarked = body.get("embarked")
            alone = body.get("alone")
            ti = [name, pclass, sex, age, sibsp, parch, fare, embarked, alone]
            print(ti)
            final = Titanic(name, pclass, sex, age, sibsp, parch, fare, embarked, alone)
            return {'message': final}, 200

    api.add_resource(_CRUD, '/')

def Titanic(name, pclass, sex, age, sibsp, parch, fare, embarked, alone):
    titanic_data = sb.load_dataset('titanic')
    td = titanic_data

    # Define a new passenger
    passenger = pd.DataFrame({
        'name': [name],
        'pclass': [pclass], # 2nd class picked as it was median, bargains are my preference, but I don't want to have poor accomodations
        'sex': [sex],
        'age': [age],
        'sibsp': [sibsp], # I usually travel with my wife
        'parch': [parch], # currenly I have 1 child at home
        'fare': [str(fare)], # convert fare to string before concatenating
        'embarked': [embarked], # majority of passengers embarked in Southampton
        'alone': [alone] # travelling with family (spouse and child))
    })

    print(passenger)

    new_passenger = passenger.copy()

    # Preprocess the new passenger data
    new_passenger['sex'] = new_passenger['sex'].apply(lambda x: 1 if x == 'male' else 0) # Convert 'male' to 1 and 'female' to 0
    new_passenger['alone'] = new_passenger['alone'].apply(lambda x: 1 if x == True else 0)

    # Check for missing values in 'embarked' column
    if new_passenger['embarked'].isnull().values.any():
        new_passenger['embarked'].fillna('Unknown', inplace=True)

    # Fit and encode 'embarked' variable
    enc = OneHotEncoder()
    enc.fit(td[['embarked']])
    onehot = enc.transform(new_passenger[['embarked']]).toarray()
    cols = ['embarked_' + str(val) for val in enc.categories_[0]]  # Convert 'val' to string before concatenating
    new_passenger[cols] = pd.DataFrame(onehot, index=new_passenger.index)
    new_passenger.drop(['name'], axis=1, inplace=True)
    new_passenger.drop(['embarked'], axis=1, inplace=True)


    td = titanic_data
    td.drop(['alive', 'who', 'adult_male', 'class', 'embark_town', 'deck'], axis=1, inplace=True)
    td.dropna(inplace=True) # drop rows with at least one missing value, after dropping unuseful columns
    td['sex'] = td['sex'].apply(lambda x: 1 if x == 'male' else 0)
    td['alone'] = td['alone'].apply(lambda x: 1 if x == True else 0)

    # Encode categorical variables
    enc = OneHotEncoder(handle_unknown='ignore')
    enc.fit(td[['embarked']])
    onehot = enc.transform(td[['embarked']]).toarray()
    cols = ['embarked_' + val for val in enc.categories_[0]]
    td[cols] = pd.DataFrame(onehot)
    td.drop(['embarked'], axis=1, inplace=True)
    td.dropna(inplace=True) # drop rows with at least one missing value, after preparing the data
    new_passenger.drop(['embarked_nan'], axis=1, inplace=True)

    # Predict the survival probability for the new passenger
    logreg = LogisticRegression()
    logreg.fit(td.drop('survived', axis=1), td['survived'])
    dead_proba, alive_proba = np.squeeze(logreg.predict_proba(new_passenger))

    # Print the survival probability
    print('Death probability: {:.2%}'.format(dead_proba))  
    print('Survival probability: {:.2%}'.format(alive_proba))
    if dead_proba > alive_proba:
        return f"Death probability: {dead_proba:.2%}"
    else:
        return f"Survival probability: {alive_proba:.2%}"