import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
import joblib

# Load and preprocess the dataset

def preprocess_data(filepath):
    df = pd.read_csv(filepath)
    X, y, encoder = preprocess_data('model/medical_students_dataset.csv')

    
    # Assuming the target is the last column
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    
    # Assuming categorical encoding is needed
    encoder = OneHotEncoder(handle_unknown='ignore')
    X_encoded = encoder.fit_transform(X.select_dtypes(include=['object']))
    X = pd.concat([X.select_dtypes(exclude=['object']), pd.DataFrame(X_encoded.toarray(), columns=encoder.get_feature_names_out())], axis=1)

    return X, y, encoder

# Train the model
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    return model

if __name__ == "__main__":
    X, y, encoder = preprocess_data('medical_data.csv')
    model = train_model(X, y)
    # Save the model and encoder
    joblib.dump(model, 'medical_model.pkl') 
