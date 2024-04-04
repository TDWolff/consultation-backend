import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

class LacrosseScoreModel:
    _instance = None
    
    def __init__(self):
        self.features = ['wins', 'losses', 'score_differential', 'two_point_goals', 'assists', 
                         'shots', 'shots_on_goal_percentage', 'turnovers', 'caused_turnovers', 
                         'groundballs', 'faceoff_percentage', 'saves', 'save_percentage', 
                         'power_play_percentage', 'penalty_kill_percentage']
        self.target = 'wins'
        self.lacrosse_data = None
        self.model = None
        self._load_data()
        self._clean()
        self._train()
    
    def _clean(self):
        # Assuming all features are numeric. Adjust preprocessing as needed.
        self.lacrosse_data.dropna(subset=self.features + [self.target], inplace=True)
    
    def _train(self):
        X = self.lacrosse_data[self.features]
        y = self.lacrosse_data[self.target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Using a pipeline to standardize features and train a model
        self.model = make_pipeline(StandardScaler(), RandomForestRegressor(n_estimators=100))
        self.model.fit(X_train, y_train)
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def _load_data(self):
        self.lacrosse_data = pd.read_csv('lacrosse.csv')
        # Convert categorical data and handle missing values as needed.
    
    def predict_winner(self, team1, team2):
        team1_data = self._get_team_data(team1)
        team2_data = self._get_team_data(team2)
        
        team1_pred = self.model.predict([team1_data])[0]
        team2_pred = self.model.predict([team2_data])[0]
        
        total_pred = team1_pred + team2_pred
        team1_chance = (team1_pred / total_pred) * 100
        team2_chance = (team2_pred / total_pred) * 100

        return {
            team1: f"{team1_chance:.2f}%",
            team2: f"{team2_chance:.2f}%"
        }
    
    def _get_team_data(self, team_name):
        # Compute average stats for the team across seasons.
        team_stats = self.lacrosse_data[self.lacrosse_data['team'] == team_name][self.features].mean().tolist()
        return team_stats

    def feature_weights(self):
        # This method will need adjustment for the RandomForestRegressor.
        pass
