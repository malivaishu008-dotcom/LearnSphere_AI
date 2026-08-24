import numpy as np
from sklearn.linear_model import LinearRegression

def train_performance_model(study_hours, past_scores):
    X = np.array(study_hours).reshape(-1, 1)
    y = np.array(past_scores)
    model = LinearRegression()
    model.fit(X, y)
    return model

def predict_score(model, hours):
    return model.predict(np.array([[hours]]))[0]