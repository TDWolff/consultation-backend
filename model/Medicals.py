import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
class MedicalModel:
    def __init__(self, data_file):
        self.data_file = data_file
        self.model = None
        self.encoder = OneHotEncoder(handle_unknown='ignore')
        self.label_encoders = {}
        self.features = ['Age', 'Gender', 'Height', 'Weight', 'BMI', 'Temperature', 'Heart Rate', 'Blood Pressure', 'Cholesterol', 'Diabetes', 'Smoking']
        self._load_data()
        self._preprocess_data()
        self._train_model()
    def _load_data(self):
        self.medical_data = pd.read_csv(self.data_file)
        self.medical_data.dropna(inplace=True)
    def _preprocess_data(self):
        # Apply label encoding to categorical variables
        for feature in ['Gender', 'Blood Type', 'Diabetes', 'Smoking']:
            le = LabelEncoder()
            self.medical_data[feature] = le.fit_transform(self.medical_data[feature])
            self.label_encoders[feature] = le
        # Apply one-hot encoding to encoded categorical variables
        self.medical_data = pd.get_dummies(self.medical_data, columns=['Blood Type'])
        self.X = self.medical_data[self.features]
    def _train_model(self):
        self.model = KMeans(n_clusters=3, random_state=42)
        self.model.fit(self.X)
    def predict(self, student_info):
        student_df = pd.DataFrame(student_info, index=[0])
        # Apply label encoding using pre-fitted label encoders
        for feature, le in self.label_encoders.items():
            student_df[feature] = le.transform([student_df[feature].iloc[0]])
        # Apply one-hot encoding
        student_df = pd.get_dummies(student_df, columns=['Blood Type'])
        prediction = self.model.predict(student_df)[0]
        return prediction