import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
class LacrosseScoreModel:
    _instance = None
    def __init__(self):
        self.model = None
        self.dt = None
        self.features = ['wins', 'losses', 'score_differential', 'two_point_goals', 'assists', 'shots']
        self.target = 'wins'
        self.lacrosse_data = None
        self._load_data()
        self._clean()
        self._train()
    def _clean(self):
        self.lacrosse_data.dropna(subset=self.features + [self.target], inplace=True)
    def _train(self):
        X = self.lacrosse_data[self.features]
        y = self.lacrosse_data[self.target]
        # Splitting the data for training and testing
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)
        self.dt = DecisionTreeRegressor()
        self.dt.fit(X_train, y_train)
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    def _load_data(self):
        # Make sure to replace 'lacrosse.csv' with the actual path to your CSV
        self.lacrosse_data = pd.read_csv('lacrosse.csv')
        self.lacrosse_data['wins'] = (self.lacrosse_data['score_differential'] > 0).astype(int)  # Assuming win based on positive score differential
    def predict_winner(self, team1, team2):
        team1_data = self.lacrosse_data[self.lacrosse_data['team'] == team1][self.features].mean()
        team2_data = self.lacrosse_data[self.lacrosse_data['team'] == team2][self.features].mean()
        team1_pred = self.model.predict([team1_data])[0]
        team2_pred = self.model.predict([team2_data])[0]
        total_pred = team1_pred + team2_pred
        team1_chance = (team1_pred / total_pred) * 100
        team2_chance = (team2_pred / total_pred) * 100
        return {
            team1: f"{team1_chance:.2f}%",
            team2: f"{team2_chance:.2f}%"
        }
    def feature_weights(self):
        return {feature: importance for feature, importance in zip(self.features, self.dt.feature_importances_)}