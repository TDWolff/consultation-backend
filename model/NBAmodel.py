import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression

class BasketBallScoreModel:
    _instance = None
    
    def __init__(self):
        self.model = None
        self.dt = None
        self.features = ['PTS_away', 'FG_PCT_away', 'FT_PCT_away', 'FG3_PCT_away', 'AST_away', 'REB_away',
                         'PTS_home', 'FG_PCT_home', 'FT_PCT_home', 'FG3_PCT_home', 'AST_home', 'REB_home']
        self.target = 'HOME_TEAM_WINS'
        self.basketball_data = None
    
    def _clean(self):
        # Drop rows with missing values in relevant columns
        self.basketball_data.dropna(subset=self.features + [self.target], inplace=True)
        
        # Convert categorical columns to appropriate data types
        self.basketball_data['HOME_TEAM_ID'] = self.basketball_data['HOME_TEAM_ID'].astype(int)
        self.basketball_data['VISITOR_TEAM_ID'] = self.basketball_data['VISITOR_TEAM_ID'].astype(int)

    def _train(self):
        X = self.basketball_data[self.features]
        y = self.basketball_data[self.target]
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
            cls._instance._train()
        return cls._instance

    def _load_data(self):
        self.basketball_data = pd.read_csv('nba_data.csv')

    def predict_winner_likelihood(self, team1_id, team2_id):
    # Filter past data for matches involving the two teams
        team1_matches = self.basketball_data[(self.basketball_data['HOME_TEAM_ID'] == team1_id) | (self.basketball_data['VISITOR_TEAM_ID'] == team1_id)]
        team2_matches = self.basketball_data[(self.basketball_data['HOME_TEAM_ID'] == team2_id) | (self.basketball_data['VISITOR_TEAM_ID'] == team2_id)]
    
    # Concatenate the filtered data to get all matches involving both teams
        matches = pd.concat([team1_matches, team2_matches])
    
    # Check if matches DataFrame is empty
        if matches.empty:
            return {"error": "No past matches found for the given teams."}
    
    # Calculate the average points scored by each team in past matches
        team1_avg_score = (matches[matches['HOME_TEAM_ID'] == team1_id]['PTS_home'].mean() or 0) + (matches[matches['VISITOR_TEAM_ID'] == team1_id]['PTS_away'].mean() or 0)
        team2_avg_score = (matches[matches['HOME_TEAM_ID'] == team2_id]['PTS_home'].mean() or 0) + (matches[matches['VISITOR_TEAM_ID'] == team2_id]['PTS_away'].mean() or 0)
    
    # Calculate the total points scored in past matches involving both teams
        total_score = team1_avg_score + team2_avg_score
    
    # Calculate the percentage likelihood for each team to win
        team1_likelihood = (team1_avg_score / total_score) * 100
        team2_likelihood = (team2_avg_score / total_score) * 100
    
        return {team1_id: team1_likelihood, team2_id: team2_likelihood}

    def feature_weights(self):
        return {feature: importance for feature, importance in zip(self.features, self.dt.feature_importances_)}