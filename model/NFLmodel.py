import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


class FootballScoreModel:
    """A class used to represent the Football Score Prediction Model."""
    _instance = None
    
    def __init__(self):
        self.model = None
        self.features = ['score_away', 'spread_favorite', 'over_under_line']
        self.target = 'score_home'
        self.football_data = None
    
    def _clean(self):
        self.football_data.dropna(subset=['score_home', 'score_away', 'spread_favorite', 'over_under_line'], inplace=True)
        current_year = pd.Timestamp.now().year
        self.football_data = self.football_data[self.football_data['schedule_season'] >= current_year - 1]
        
    def _train(self):
        X = self.football_data[self.features]
        y = self.football_data[self.target]
        self.model = LinearRegression()
        self.model.fit(X, y)
        
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance._load_data()
            cls._instance._clean()
            cls._instance._train()
        return cls._instance

    def _load_data(self):
        self.football_data = pd.read_csv('spreadspoke_scores.csv', header=0)
    
    def get_team_id(team_name):
        team_mapping = {
            'Arizona Cardinals': 'ARI',
            'Atlanta Falcons': 'ATL',
            'Baltimore Ravens': 'BAL',
            'Buffalo Bills':'BUF',
            'Carolina Panthers':'CAR',
            'Chicago Bears':'CHI',
            'Cincinnati Bengals':'CIN',
            'Clevland Browns':'CLE',
            'Dallas Cowboys':'DAL',
            'Denver Broncos':'DEN',
        }
        return team_mapping.get(team_name, None)
    
    def predict_winner_likelihood(self, team1, team2):
        # Filter past data for matches involving the two teams
        team1_matches = self.football_data[(self.football_data['team_home'] == team1) | (self.football_data['team_away'] == team1)]
        team2_matches = self.football_data[(self.football_data['team_home'] == team2) | (self.football_data['team_away'] == team2)]

        # Concatenate the filtered data to get all matches involving both teams
        matches = pd.concat([team1_matches, team2_matches])

        # Calculate the average score of each team in past matches
        team1_avg_score = matches[matches['team_home'] == team1]['score_home'].mean() + matches[matches['team_away'] == team1]['score_away'].mean()
        team2_avg_score = matches[matches['team_home'] == team2]['score_home'].mean() + matches[matches['team_away'] == team2]['score_away'].mean()

        # Calculate the total points scored in past matches involving both teams
        total_score = team1_avg_score + team2_avg_score

        # Calculate the percentage likelihood for each team to win
        team1_likelihood = (team1_avg_score / total_score) * 100
        team2_likelihood = (team2_avg_score / total_score) * 100


        #try:
        #    matches['over_under_line'] = pd.to_numeric(matches['over_under_line'])
        #    over_under_diff = matches['over_under_line'].mean()  # Mean over/under difference
        #except ValueError:
        #    over_under_diff = 0

        # Consider spread favorite and over/under line in prediction
        #spread_diff = matches['spread_favorite'].mean()  # Mean spread difference
        #over_under_diff = matches['over_under_line'].mean()  # Mean over/under difference

        # Adjust likelihood based on spread and over/under
        #if spread_diff > 0:  # Home team is favorite
        #    team1_likelihood += spread_diff
        #else:  # Away team is favorite
        #    team2_likelihood += abs(spread_diff)

        #if over_under_diff > total_score:  # Expect high-scoring game
        #    team1_likelihood += over_under_diff - total_score
        #    team2_likelihood += over_under_diff - total_score
        #elif over_under_diff < total_score:  # Expect low-scoring game
        #    team1_likelihood -= total_score - over_under_diff
        #    team2_likelihood -= total_score - over_under_diff

        # Calculate win percentage for the current year for both teams
        #current_year = pd.Timestamp.now().year
        #current_year_matches = matches[matches['schedule_season'] == current_year]
        #team1_wins = ((current_year_matches['team_home'] == team1) & (current_year_matches['score_home'] > current_year_matches['score_away'])).sum() + \
        #            ((current_year_matches['team_away'] == team1) & (current_year_matches['score_away'] > current_year_matches['score_home'])).sum()
        #team2_wins = ((current_year_matches['team_home'] == team2) & (current_year_matches['score_home'] > current_year_matches['score_away'])).sum() + \
        #            ((current_year_matches['team_away'] == team2) & (current_year_matches['score_away'] > current_year_matches['score_home'])).sum()

        #team1_win_percentage = (team1_wins / len(current_year_matches)) * 100 if len(current_year_matches) > 0 else 0
        #team2_win_percentage = (team2_wins / len(current_year_matches)) * 100 if len(current_year_matches) > 0 else 0

        # Adjust likelihood based on current year's performance
        #team1_likelihood += team1_win_percentage
        #team2_likelihood += team2_win_percentage

        return {team1: team1_likelihood, team2: team2_likelihood}

# Example usage
model = FootballScoreModel.get_instance()
#print(model.predict_winner_likelihood('Seattle Seahawks', 'Baltimore Ravens'))
