import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression

class SoccerScoreModel:
    """A class used to represent the Soccer Score Prediction Model."""
    
    _instance = None
    
    def __init__(self):
        self.model = None
        self.dt = None
        # Initial features list, will be updated after cleaning the data
        self.features = ['home_score', 'neutral']  # Note: This will be updated dynamically after one-hot encoding
        self.target = None
        self.soccer_data = None
    
    def _clean(self):
        # Drop rows with missing values in the initial features list
        self.soccer_data.dropna(subset=['home_score', 'tournament', 'city', 'country', 'neutral'], inplace=True)
        
        # Convert 'neutral' to numeric if it's not already
        if self.soccer_data['neutral'].dtype != 'int64':
            self.soccer_data['neutral'] = self.soccer_data['neutral'].astype(int)
        
        # Apply One-Hot Encoding to categorical columns
        categorical_features = ['tournament', 'city', 'country']
        self.soccer_data = pd.get_dummies(self.soccer_data, columns=categorical_features, drop_first=True)
        
        # Update the features list to include the new one-hot encoded columns
        self.features += [col for col in self.soccer_data.columns if col.startswith(tuple(categorical_features)) and col not in self.features]
    
    def _train(self):
        X = self.soccer_data[self.features]
        y = self.soccer_data[self.target]
        self.model = LinearRegression()
        self.model.fit(X, y)
        self.dt = DecisionTreeRegressor()
        self.dt.fit(X, y)
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._load_data()
            cls._instance._clean()
            cls._instance._set_target()
            cls._instance._train()
        return cls._instance
    
    def _load_data(self):
        self.soccer_data = pd.read_csv('results.csv')
    
    def _set_target(self):
        self.soccer_data['home_wins'] = (self.soccer_data['home_score'] > self.soccer_data['away_score']).astype(int)
        self.target = 'home_wins'
    
    def predict_winner_likelihood(self, team1, team2):
        team1_matches = self.soccer_data[(self.soccer_data['home_team'] == team1) | (self.soccer_data['away_team'] == team1)]
        team2_matches = self.soccer_data[(self.soccer_data['home_team'] == team2) | (self.soccer_data['away_team'] == team2)]
        matches = pd.concat([team1_matches, team2_matches])
        if matches.empty:
            return {"error": "No past matches found for the given teams."}
        team1_avg_score = (matches[matches['home_team'] == team1]['home_score'].mean() or 0) + (matches[matches['away_team'] == team1]['away_score'].mean() or 0)
        team2_avg_score = (matches[matches['home_team'] == team2]['home_score'].mean() or 0) + (matches[matches['away_team'] == team2]['away_score'].mean() or 0)
        total_score = team1_avg_score + team2_avg_score
        team1_likelihood = (team1_avg_score / total_score) * 100
        team2_likelihood = (team2_avg_score / total_score) * 100
        return {team1: team1_likelihood, team2: team2_likelihood}
    
    def feature_weights(self):
        return {feature: importance for feature, importance in zip(self.features, self.dt.feature_importances_)}

